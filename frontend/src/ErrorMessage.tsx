export default function ErrorMessage({ errMsg }: { errMsg: string }) {
  return (
    <>
      <div className="text-5xl ovo-regular mt-16 mb-8">
        {errMsg}
      </div>
    </>
  )
}
