from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO

import math

from database import VectorDatabase
from llm import Llm, Backend


app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

vdb = VectorDatabase()
llm = Llm(backend=Backend.OPENAI)


def error_response(message: str, status_code: int = 400):
    return jsonify({"error": message}), status_code


@app.route("/")
def index():
    if app.static_folder:
        return send_from_directory(app.static_folder, "index.html")
    return error_response("Static folder not set")


@app.route("/hello")
def hello():
    return "Hello, World!"


@app.route("/generate", methods=["POST"])
def generate():
    """
    Take in

    {
        "stdout": "...",
        "stderr": "...",
        "files": [
            {"path": "...", "content": "..."},
            {"path": "...", "content": "..."},
            ...
        ]
    }

    and send back IR.
    """

    context = request.get_json()
    if not context:
        return error_response("No context provided")

    if "stdout" not in context or "stderr" not in context or "files" not in context:
        return error_response("Invalid context provided")

    stdout = context.get("stdout")
    stderr = context.get("stderr")
    files = [(f.get("path"), f.get("content")) for f in context.get("files", [])]

    socketio.emit("loading", {"message": "Generating response..."})

    vdb.clear()
    vdb.add_files(files)

    terminal_output = f"""
    The following is the terminal output:
    # Stdout:
    {stdout}
    # Stderr:
    {stderr}
    """

    # Get the top 20% most pertinent files based on terminal output
    num_files = len(files) if len(files) < 5 else math.ceil(0.2 * len(files))
    vdb_result = vdb.query(f"{terminal_output}", num_files)
    file_context = ""
    for path, content in zip(vdb_result["ids"], vdb_result["documents"]):
        file_context += f"""
        {path}:
        {content}
        """

    prompt = f"""
    You are an expert software developer and debugger. Your task is to analyze file context and terminal output to identify errors, provide annotations, and suggest fixes. Here's the information you need to work with:

{file_context}

{terminal_output}

Please follow these steps to complete your task:

1. Carefully analyze the terminal output to determine if there are any errors.

2. If you identify an error, proceed with the following steps. If no error is detected, simply state that no debugging is needed.

3. For each error identified:
   a. Locate the most important lines in the terminal output related to the error.
   b. Create an annotation for each unique error, explaining it concisely.
   c. Provide a one-sentence summary of the issue. Keep it extremely concise, e.g., "Missing source file", "Unknown function used", or "Incorrect argument types in 'myfunc'".
   d. Give a more detailed description of the error and its implications.
   e. Generate a diff suggesting a fix for the error. The diff should be in plain text format, with additions prefixed by "+ " and removals by "- ". You may include surrounding text (prefixed with "  ") for clarity, but do not add any additional diff formatting.

4. Format your response according to the specified output structure, which includes sections for description, diff, and annotations.

Before providing your final output, wrap your analysis inside <error_analysis> tags. In this analysis:
- Break down the terminal output and identify potential errors. List each error found.
- Examine the file context to understand the code structure and potential issues.
- Match each identified error with the relevant code in the file context.
- For each error, draft your annotation, summary, and detailed description.
- Brainstorm potential fixes for each error, considering different approaches.
- Carefully consider the diff you'll suggest, ensuring it directly addresses the identified issue and follows best practices for the programming language in question.
- Review your proposed diff to ensure it's clear, concise, and effective in resolving the error without introducing new problems.

Remember, the quality of the diff is crucial. Ensure that your suggested changes are precise, relevant, and likely to resolve the identified issue without introducing new problems.

After completing your analysis, provide your final output structured according to the specified format, including the description, diff, and annotations.
    """

    llm_result = llm.query(prompt)

    if not llm_result:
        return error_response("Response could not be created")

    socketio.emit("response", {"message": llm_result.model_dump_json()})
    return llm_result.model_dump_json()


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    socketio.run(app)
