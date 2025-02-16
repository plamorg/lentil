open! Core

type t =
  { stdout : string
  ; stderr : string
  ; files : File.t list
  }
[@@deriving sexp, yojson]

let get cmd =
  let stdout, stderr = Process.run cmd in
  { stdout; stderr; files = File.get () }
;;
