import SyntaxHighlighter from 'react-syntax-highlighter'

function SuggestedFixHeader() {
  return (
    <div className="flex flex-row justify-between">
      <h2 className="text-xl font-semibold">Suggested Fix</h2>
      <p className="text-sm text-gray-500">(diff)</p>
    </div>
  )
}

function SuggestedFixBody({ diff } : { diff: string }) {
  return (
    <div className="border rounded-lg bg-gray-50 p-4">
      <SyntaxHighlighter language="diff">
        {diff}
      </SyntaxHighlighter>
    </div>
  )
}

export default function SuggestedFix({ diff }: { diff: string }) {
  return (
    <div className="flex flex-col gap-2">
      <SuggestedFixHeader />
      <SuggestedFixBody diff={diff} />
    </div>
  )
}
