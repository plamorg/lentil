open! Core

type t =
  { path : string
  ; content : string
  }
[@@deriving sexp]

val get : unit -> t list
