import { useState } from "react"
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/outline'

export default function Annotation({ output, comment }: { output: string; comment: string }) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div
      className="rounded-md border border-gray-300 p-4 cursor-pointer hover:bg-gray-50"
      onClick={() => setIsExpanded(!isExpanded)}
    >
      <div className="flex flex-row justify-between items-center">
        <pre className="font-mono text-sm select-none cursor-pointer">{output}</pre>
        {isExpanded ? (
          <ChevronUpIcon className="h-5 w-5 text-gray-500" />
        ) : (
          <ChevronDownIcon className="h-5 w-5 text-gray-500" />
        )}
      </div>
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
