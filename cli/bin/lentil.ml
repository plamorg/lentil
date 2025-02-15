open! Core
module Context = Lentil.Context
module File = Lentil.File

let start_server () = print_s [%message "hi starting webserver"]

let send_context () =
  (* testing for now *)
  let files = Context.get () in
  print_s [%message (files : Context.t)]
;;

let main ~serve =
  match serve with
  | true -> start_server ()
  | false -> send_context ()
;;

let command =
  Command.basic
    ~summary:"lentil"
    (let%map_open.Command serve = flag "--serve" no_arg ~doc:"start webserver" in
     fun () -> main ~serve)
;;

let () = Command_unix.run command
