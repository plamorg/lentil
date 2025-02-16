import Header from "./Header.tsx"
import ErrorMessage from "./ErrorMessage.tsx"
import SuggestedFix from "./SuggestedFix.tsx"

export default function App() {
  const errMsg = "You have an undefined variable";
  const diffLines = [
    "+ add this line",
    "- remove this line"
  ];
  const diff = diffLines.join("\n");

  return (
    <>
      <div className="h-screen w-full max-w-2xl m-auto mt-8 flex flex-col gap-4">
        <Header />
        <ErrorMessage errMsg={errMsg} />
        <SuggestedFix diff={diff} />
      </div>
    </>
  )
}
