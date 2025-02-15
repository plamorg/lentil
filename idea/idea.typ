#set par(justify: true)
#set text(
  font: "Helvetica",
)

#let lentil = {
  text(orange, box[*Lentil*])
}

= Lentil
== Bringing Error Messages into the 21st Century


=== Problem

Terminal output messages often vary significantly in clarity and usefulness. Many developers know the frustration of compiling a program only to be overwhelmed by hundreds of lines of cryptic or irrelevant messages. With recent advances in AI, we can now build a tool that filters through this clutter, highlights the most critical information, and even suggests potential fixes based on your project files.

That's why we are building #lentil.

=== The Solution

#lentil is a simple, AI-powered program designed to enhance command-line output. Imagine running:

```sh
$ gcc main.c
```

and seeing a flood of unclear compiler messages. Instead, you can pipe the output into Lentil:

```sh
$ gcc main.c | lentil
```

Lentil captures both stdout and stderr, then uses modern retrieval-augmented generation (RAG) techniques to contextualize these messages by examining the files in the current working directory (recursively). It produces a standardized international representation (IR), for example:

```json
{
    "quick-description": "You have an undefined function.",
    "diff": "", // <-- diff showing how to fix the issue
    "annotations": [
        {
            "command_output": ["line 1", "line 2"],
            "comment": "This relates to kernel/driver/tty.c, looking at lines 341–434..."
        },
        {
            "command_output": ["line 5", "line 6", "line 7"],
            "comment": "..."
        }
    ]
}
```

The above IR is tentative, but is currently based on JSON.

== Key Features

- *Live updates*: Lentil can be run in the background, continuously updating as you code.
- *Language agnostic*: Works with any language and editor.
- *Simple UX*: Lentil can be run as a standalone command or integrated into existing tools via the IR.

== Core

The core application essentially receives stdout, stderr, and context of the current working directory's files and produces the IR.
The core application needs to support the CLI and facilitate calling to the #lentil web server for RAG and web view for example (more details in the next section).
If #lentil is run without any arguments, it will take the IR and convert it into somewhat readable text.

The core application will be built with *OCaml*.

== Web Server

Lentil also has a web server component.
The web server's purpose is threefold:
1. Facilitating RAG (via chromadb vector database).
2. LLM inference (ollama or openai etc.).
3. Hosting web view.

For the third point (hosting web view), if `lentil --web` is run, it will generate the IR and additionally send it to the web server.
The web server will then render it.

The web server will be written in *Python* and can be run with

```sh
$ lentil serve
# Now serving at 127.0.0.1:4321
```
