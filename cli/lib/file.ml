open! Core

type t =
  { path : string
  ; content : string
  }
[@@deriving sexp]

let get () =
  let rec f dir =
    Core_unix.ls_dir_detailed dir
    |> List.filter_map ~f:(fun { name; kind; _ } ->
      match kind with
      | Some UnixLabels.S_REG ->
        let path = Filename.concat dir name in
        let content = In_channel.read_all path in
        Some [ { path; content } ]
      | Some S_DIR ->
        (match name with
         | "." | ".." | "_build" -> None
         | dir' ->
           let path = Filename.concat dir dir' in
           Some (f path))
      | _ -> None)
    |> List.concat
  in
  let wd = Filename.current_dir_name in
  f wd
;;
