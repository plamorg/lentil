open! Core

type t =
  { path : string
  ; content : string
  }
[@@deriving sexp, yojson]

val get : unit -> t list
