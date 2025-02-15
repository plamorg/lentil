open! Core

let run cmd =
  let cmd_strs = String.split cmd ~on:' ' in
  let prog = List.hd_exn cmd_strs in
  let args = List.tl_exn cmd_strs in
  let cmd_result = Core_unix.create_process ~prog ~args in
  let stdout = Core_unix.in_channel_of_descr cmd_result.stdout in
  let stderr = Core_unix.in_channel_of_descr cmd_result.stderr in
  let stdout_output = In_channel.input_all stdout in
  let stderr_output = In_channel.input_all stderr in
  stdout_output, stderr_output
