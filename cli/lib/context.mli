open! Core

type t =
  { stdout : string
  ; stderr : string
  ; files : File.t list
  }
[@@deriving sexp]

val get : string list -> t
