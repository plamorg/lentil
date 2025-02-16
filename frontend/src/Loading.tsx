function LoadingBar() {
  return (
    <div className="w-full h-6 bg-gray-200 from-gray-100 to-gray-400 rounded duration-700 animate-pulse" />
  )
}

export default function Loading() {
  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-5xl ovo-regular mt-16 mb-8">Cooking your lentils...</h1>
      <LoadingBar />
      <LoadingBar />
      <LoadingBar />
    </div>
  )
}
