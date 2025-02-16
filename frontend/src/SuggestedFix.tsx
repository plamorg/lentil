export default function SuggestedFix({ diff }: { diff: string }) {
  return (
    <>
      <div className="flex flex-row justify-between">
        <h2 className="text-xl font-semibold mb-4">Suggested Fix</h2>
        <p className="text-sm text-gray-500">(diff)</p>
      </div>
      <div className="border rounded-lg bg-gray-50 p-4">
        <pre className="whitespace-pre-wrap font-mono text-sm">
          <code>
            {diff}
          </code>
        </pre>
      </div>
    </>
  )
}
