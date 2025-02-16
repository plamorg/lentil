import { useEffect, useState } from "react";
import ErrorMessage from "./ErrorMessage.tsx";
import SuggestedFix from "./SuggestedFix.tsx";
import { Annotations, Annotation } from "./Annotations.tsx";
import Loading from "./Loading.tsx";
import { socket } from "./socket.ts";

interface Response {
  summary: string;
  description: string;
  diff: string;
  annotations: Array<Annotation>;
}

export default function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [response, setResponse] = useState<Response | null>(null);

  useEffect(() => {
    socket.on("loading", (_: any) => {
      setIsLoading(true);
    });
    socket.on("response", (data: any) => {
      data = JSON.parse(data["message"]);
      setResponse(data as Response);
      setIsLoading(false);
    });
  }, []);

  console.log(response);

  return (
    <>
      <div className="h-screen p-8 max-w-4xl m-auto mt-8 flex flex-col gap-4">
        {/* <Header /> */}
        {!isLoading && response ? (
          <div>
            <ErrorMessage errMsg={response.summary} />
            <SuggestedFix diff={response.diff} />
            <Annotations annotations={response.annotations} />
            <p className="font-serif mt-4 mb-8">{response.description}</p>
          </div>
        ) : (
          <Loading />
        )}
      </div>
    </>
  );
}
