open! Core

type t =
  { path : string
  ; content : string
  }
[@@deriving sexp]

(* let read_all_dir dir = *)
(*   let dir = Core_unix.opendir dir in *)
(*   let rec f () = *)
(*     match Core_unix.readdir_opt dir with *)
(*     | None -> [] *)
(*     | Some file -> file :: f () *)
(*   in *)
(*   let res = f () in *)
(*    Core_unix.closedir dir; *)
(*     res *)
(* ;; *)

(* let get () = *)
(*   let rec f dir = *)
(*     read_all_dir dir *)
(*     |> List.filter ~f:(fun name -> not ((String.equal name ".") || (String.equal name ".."))) *)
(*     |> List.map ~f:(fun name -> *)
(*       let path = Filename.concat dir name in *)
(*       Filename. *)
(*       if Core_unix.is_directory path *)
(*       then f path *)
(*       else ( *)
(*         let content = In_channel.read_all path in *)
(*         [ { path; content } ])) *)
(*     |> List.concat *)
(*   in *)
(*   let wd = Filename.current_dir_name in *)
(*   f wd *)
(* ;; *)

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
