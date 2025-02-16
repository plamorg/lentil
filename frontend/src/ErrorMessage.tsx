export default function ErrorMessage({ errMsg }: { errMsg: string }) {
  return (
    <>
      <h1 className="text-5xl ovo-regular mt-16 mb-8">
        {errMsg}
      </h1>
    </>
  )
}
