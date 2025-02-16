open! Core
open! Async

let uri = Uri.of_string "http://127.0.0.1:5000/generate"

let send context =
  let body =
    Context.to_yojson context |> Yojson.Safe.to_string |> Cohttp_async.Body.of_string
  in
  let headers = Cohttp.Header.init () in
  let headers = Cohttp.Header.add headers "Content-Type" "application/json" in
  let%bind res, body = Cohttp_async.Client.post ~body ~headers uri in
  let%bind body = Cohttp_async.Body.to_string body in
  print_s [%message (res : Cohttp.Response.t) (body : string)];
  return ()
;;
