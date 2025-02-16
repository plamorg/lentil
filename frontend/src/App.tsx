import Header from "./Header.tsx"
import ErrorMessage from "./ErrorMessage.tsx"
import SuggestedFix from "./SuggestedFix.tsx"
import Annotation from "./Annotation.tsx"

export default function App() {
  const errMsg = "You have an undefined variable";
  const diffLines = [
    "+ add this line",
    "- remove this line"
  ];
  const diff = diffLines.join("\n");
  const annotations = [
    {
      output: "Error: Cannot find module 'react'",
      comment: "Install React package by running: npm install react"
    },
    {
      output: "TypeError: Cannot read property 'map' of undefined",
      comment: "Initialize the array before using map function or add a null check"
    },
    {
      output: "Error: Maximum update depth exceeded",
      comment: "Check for infinite loops in useEffect or state updates that trigger rerenders"
    }
  ];

  return (
    <>
      <div className="h-screen w-full max-w-2xl m-auto mt-8 flex flex-col gap-4">
        <Header />
        <ErrorMessage errMsg={errMsg} />
        <SuggestedFix diff={diff} />
        <div className="flex flex-col gap-4">
        {annotations.map((annotation, index) => (
          <Annotation 
            key={index}
            output={annotation.output}
            comment={annotation.comment} />
        ))}
        </div>
      </div>
    </>
  )
}
