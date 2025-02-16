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
    Identify whether the following terminal output indicates an error:
    {terminal_output}

    If debugging needs to happen, indicate the most important lines of the terminal output that relate to the error and annotate it with a concise explanation. Each unique error should be a different annotation.
    In addition, provide a very quick one-sentence summary of the issue. Keep the quick description extremely concise - for example: "You have a missing source file.", or "You are using an unknown function.", or "The function 'myfunc' has wrong argument types.". In addition, provide a more detailed description.
    Also provide a diff of a suggested change, if possible. For the diff DO NOT use markdown formatting, just plain text. Each addition should start with the prefix "+ ", and each removal should start with the prefix "- ".
    Do not use markdown formatting, just plain text.

    If no debugging needs to happen, no need to annotate anything and no description or diff is needed.

    The following is the file context:
    {file_context}
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
