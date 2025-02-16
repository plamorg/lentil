import SyntaxHighlighter from 'react-syntax-highlighter'

function SuggestedFixHeader() {
  return (
    <div className="flex flex-row justify-between">
      <h2 className="text-xl font-medium mb-2">We suggest the following fixes:</h2>
      { /* <p className="text-sm text-gray-500">(diff)</p> */ }
    </div>
  )
}

function SuggestedFixBody({ diff } : { diff: string }) {
  return (
    <div className="rounded-lg bg-gray-50 p-4">
      <SyntaxHighlighter className="syntaxhighlighter" language="diff">
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
