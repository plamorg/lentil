open! Core
module Context = Lentil.Context
module File = Lentil.File

let start_server () = print_s [%message "hi starting webserver"]

let send_context cmd =
  (* testing for now *)
  let files = Context.get cmd in
  print_s [%message (files : Context.t)]
;;

let main cmd ~serve =
  match serve with
  | true -> start_server ()
  | false ->
    (match cmd with
     | None -> error_s [%message "cmd empty liao"] |> ok_exn
     | Some cmd -> send_context cmd)
;;

let command =
  Command.basic
    ~summary:"lentil"
    (let%map_open.Command serve = flag "--serve" no_arg ~doc:"start webserver"
     and cmd = anon (maybe (non_empty_sequence_as_list ("cmd" %: string))) in
     fun () -> main cmd ~serve)
;;

let () = Command_unix.run command
