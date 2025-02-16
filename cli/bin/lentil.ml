open Core
open Async
module Context = Lentil.Context
module File = Lentil.File
module Api = Lentil.Api
module Server = Lentil.Server

let send_context cmd =
  let ctx = Context.get cmd in
  (* TODO: colour *)
  print_string ctx.stdout;
  print_string ctx.stderr;
  Api.send ctx
;;

let main () =
  let args = Sys.get_argv () |> Array.to_list |> List.tl_exn in
  let serve, cmd_args =
    List.partition_tf args ~f:(fun arg -> String.equal arg "--serve")
  in
  if not (List.is_empty serve)
  then never_returns (Server.run ())
  else (
    match cmd_args with
    | [] ->
      print_endline "No command entered";
      exit 1
    | _ -> send_context cmd_args)
;;

let () =
  Thread_safe.block_on_async_exn (fun () ->
    let%bind () = main () in
    Writer.flushed (force Writer.stdout))
;;
