from flask import Flask, jsonify, request
from flask_cors import CORS
import chromadb

from database import VectorDatabase


app = Flask(__name__)
CORS(app)

vdb = VectorDatabase()


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

    stdout = context.get("stdout")
    stderr = context.get("stderr")
    files = [(f.get("path"), f.get("content")) for f in context.get("files", [])]

    if not stdout or not stderr or not files:
        return error_response("Invalid context provided")
    for path, content in files:
        if not path or not content:
            return error_response(
                f"Invalid file with path {path} and content {content}"
            )

    print("Generating IR...")

    return jsonify({"ir": "..."})


if __name__ == "__main__":
    import sys

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(debug=True, port=port)
