open! Core
open! Async
module Context = Lentil.Context
module File = Lentil.File
module Api = Lentil.Api
module Server = Lentil.Server

let send_context cmd =
  let ctx = Context.get cmd in
  Api.send ctx
;;

let main cmd ~serve =
  match serve with
  | true -> never_returns (Server.run ())
  | false ->
    (match cmd with
     | None -> error_s [%message "cmd empty liao"] |> ok_exn
     | Some cmd -> send_context cmd)
;;

let command =
  Command.async
    ~summary:"lentil"
    (let%map_open.Command serve = flag "--serve" no_arg ~doc:"start webserver"
     and cmd = anon (maybe (non_empty_sequence_as_list ("cmd" %: string))) in
     fun () -> main cmd ~serve)
;;

let () = Command_unix.run command
