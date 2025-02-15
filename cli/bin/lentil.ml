open! Core
module Context = Lentil.Context
module File = Lentil.File

let start_server () = print_s [%message "hi starting webserver"]

let send_context () =
  (* testing for now *)
  let files = Context.get () in
  print_s [%message (files : Context.t)]
;;

let main cmd ~serve =
  print_s [%message (cmd : string list)];
  match serve with
  | true -> start_server ()
  | false -> send_context ()
;;

let command =
  Command.basic
    ~summary:"lentil"
    (let%map_open.Command serve = flag "--serve" no_arg ~doc:"start webserver"
     and cmd = anon (non_empty_sequence_as_list ("cmd" %: string)) in
     fun () -> main cmd ~serve)
;;

let () = Command_unix.run command
