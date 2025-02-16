# Lentil 🫘
AI-powered compiler feedback assistant

## Getting started
### Prerequisites
* [OCaml and `opam`](https://ocaml.org/install)
* [Dune](https://dune.build/install)
* [uv](https://github.com/astral-sh/uv)

After cloning the repository, you need to install the webserver by adding a symlink:
```sh
ln -s path/to/lentil/server ~/.lentil/server
```

### Usage
First launch the webserver:
```sh
cd cli
dune exec lentil -- --serve
```

...and run your compilation command through Lentil.
```sh
dune exec lentil -- gcc main.c
```
