import { useState } from "react"

export default function Annotation({ output, comment }: { output: string; comment: string }) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div
      className="rounded-md border border-gray-300 p-4 cursor-pointer hover:bg-gray-50"
      onClick={() => setIsExpanded(!isExpanded)}
    >
      <pre className="font-mono text-sm select-none cursor-pointer">{output}</pre>
      {isExpanded && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <p className="text-gray-600 text-sm">
            {comment}
          </p>
        </div>
      )}
    </div>
  );
}
