import { useEffect, useState } from "react";
import ErrorMessage from "./ErrorMessage.tsx";
import SuggestedFix from "./SuggestedFix.tsx";
import { Annotations, Annotation } from "./Annotations.tsx";
import { socket } from "./socket.ts";

interface Response {
  summary: string;
  description: string;
  diff: string;
  annotations: Array<Annotation>;
}

export default function App() {
  const [response, setResponse] = useState<Response | null>(null);

  useEffect(() => {
    socket.on("response", (data: any) => {
      data = JSON.parse(data["message"]);
      setResponse(data as Response);
    });
  }, []);
  console.log(response);

  return (
    <>
      <div className="h-screen p-8 max-w-4xl m-auto mt-8 flex flex-col gap-4">
        {/* <Header /> */}
        {response ? (
          <div>
            <ErrorMessage errMsg={response.summary} />
            <SuggestedFix diff={response.diff} />
            <Annotations annotations={response.annotations} />
            <div>
              <h2 className="text-xl font-medium my-3">
                Here is a more detailed analysis...
              </h2>
              <p className="ovo-regular">{response.description}</p>
            </div>
          </div>
        ) : null}
      </div>
    </>
  );
}
