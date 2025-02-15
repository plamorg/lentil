open! Core

type t =
  { stdout : string
  ; stderr : string
  ; files : File.t list
  }
[@@deriving sexp]

let get () = { stdout = "test stdout"; stderr = "test stderr"; files = File.get () }
