open! Core

let process_from_string (cmd : string list) : Core_unix.Process_info.t =
  let prog = List.hd_exn cmd in
  let args = List.tl_exn cmd in
  Core_unix.create_process ~prog ~args
;;

let extract_output (cmd_result : Core_unix.Process_info.t) : string * string =
  let stdout = Core_unix.in_channel_of_descr cmd_result.stdout in
  let stderr = Core_unix.in_channel_of_descr cmd_result.stderr in
  let stdout_output = In_channel.input_all stdout in
  let stderr_output = In_channel.input_all stderr in
  stdout_output, stderr_output
;;

let run cmd = process_from_string cmd |> extract_output
