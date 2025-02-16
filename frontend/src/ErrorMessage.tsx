export default function ErrorMessage({ errMsg }: { errMsg: string }) {
  return (
    <>
      <div className="text-5xl font-medium mt-16 mb-8">
        {errMsg}
      </div>
    </>
  )
}
