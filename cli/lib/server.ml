open! Core
open! Async

let directory = Option.value_exn (Unix.getenv "HOME") ^ "/.lentil/server"

let exec () =
  Core_unix.exec
    ~prog:"uv"
    ~argv:[ "uv"; "--directory"; directory; "run"; directory ^ "/main.py" ]
    ()
;;

let run () = exec ()
