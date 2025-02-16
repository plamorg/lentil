export default function ErrorMessage({ errMsg }: { errMsg: string }) {
  return (
    <>
      <div className="text-red-600 text-xl font-medium">
        {errMsg}
      </div>
    </>
  )
}
