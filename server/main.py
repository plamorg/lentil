from flask import Flask, jsonify, request
from flask_cors import CORS
import math

from database import VectorDatabase
from llm import Llm, Backend


app = Flask(__name__)
CORS(app)

vdb = VectorDatabase()
llm = Llm(backend=Backend.OLLAMA)


def error_response(message: str, status_code: int = 400):
    return jsonify({"error": message}), status_code


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
    Identify whether the following terminal output indicates an error:
    {terminal_output}

    If debugging needs to happen, indicate the most important lines of the terminal output that relate to the error and annotate it with potential fixes.
    Also provide a quick description of how to fix the issue and provide a diff if possible.

    If no debugging needs to happen, no need to annotate anything.

    The following is the file context
    {file_context}
    """

    llm_result = llm.query(prompt)

    if not llm_result:
        return error_response("Response could not be created")

    return llm_result.model_dump_json()


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(debug=True, port=port)
