open! Core

type t =
  { stdout : string
  ; stderr : string
  ; files : File.t list
  }
