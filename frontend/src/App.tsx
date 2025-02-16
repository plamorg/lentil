import Header from "./Header.tsx"
import ErrorMessage from "./ErrorMessage.tsx"

export default function App() {
  const errMsg = "You have an undefined variable";

  return (
    <>
      <div className="h-screen w-full max-w-2xl m-auto mt-8 flex flex-col gap-4">
        <Header />
        <ErrorMessage errMsg={errMsg} />
      </div>
    </>
  )
}
