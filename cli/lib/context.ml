open! Core

type t =
  { stdout : string
  ; stderr : string
  ; files : File.t list
  }
[@@deriving sexp]

let get cmd =
  print_s [%message (cmd : string list)];
  let stdout, stderr = Process.run cmd in
  { stdout; stderr; files = File.get () }
;;
