from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import math

from database import VectorDatabase
from llm import Llm, Backend


app = Flask(__name__, static_folder="../frontend/dist", static_url_path="/")
CORS(app)
socketio = SocketIO(app)

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

    emit("loading", {"message": "Generating response..."})

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
    You are an expert debugging assistant tasked with analyzing terminal output and providing helpful insights and suggestions. Your goal is to identify errors, explain them clearly, and offer potential fixes.

Here is the terminal output you need to analyze:

{terminal_output}

For context, here is the relevant file information:

{file_context}

Please follow these steps to analyze the situation and provide assistance:

1. Carefully examine the terminal output and determine if it indicates an error.

2. If an error is present:
   a. Identify the most important lines related to the error.
   b. Annotate these lines with concise explanations. Each unique error should have a separate annotation.
   c. Provide a very brief one-sentence summary of the issue. Examples: "Missing source file.", "Unknown function used.", "Function 'myfunc' has incorrect argument types."
   d. Give a more detailed description of the problem.
   e. If possible, suggest a fix using a diff format. Use "+" to prefix additions and "-" to prefix removals. You may include surrounding text (prefixed with "  ") for clarity, but do not add additional diff formatting such as filenames.

3. If no error is present, simply state that no debugging is necessary.

Before providing your final response, wrap your debugging process inside <debugging_process> tags. This should include:
- Quoting relevant parts of the terminal output
- Identifying potential errors (count the number of errors identified)
- Analyzing the file context
- Formulating annotations and summary
- Developing a diff suggestion
- Reviewing the diff suggestion to ensure it's accurate and helpful

Your final output should be structured as given in the model schema.

Remember, do not use any markdown formatting in your response. Present everything in plain text.
    """

    llm_result = llm.query(prompt)

    if not llm_result:
        return error_response("Response could not be created")

    emit("response", {"message": llm_result.model_dump_json()})
    return llm_result.model_dump_json()


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    socketio.run(app)
