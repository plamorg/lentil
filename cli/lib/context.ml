open! Core

type t =
  { stdout : string
  ; stderr : string
  ; files : File.t list
  }
[@@deriving sexp]

let get cmd =
  print_s [%message (cmd : string list)];
  { stdout = "test stdout"; stderr = "test stderr"; files = File.get () }
;;
