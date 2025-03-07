open! Core

type t =
  { stdout : string
  ; stderr : string
  ; cmd : string
  ; files : File.t list
  }
[@@deriving sexp, yojson]

val get : string list -> t
