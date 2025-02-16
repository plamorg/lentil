import Annotation from "./Annotation.tsx"

type Annotation = {
  output: string;
  comment: string;
}

function AnnotationsTable({ annotations }: { annotations: Annotation[] }) {
  return (
      <div className="flex flex-col">
        <h2 className="text-xl font-medium mt-4 mb-6">Here's why.</h2>
          <div className="flex flex-col gap-4">
            {annotations.map((annotation, index) => (
              <Annotation
                key={index}
                output={annotation.output}
                comment={annotation.comment}
              />
            ))}
          </div>
      </div>
  );
}

export default function Annotations({ annotations }: { annotations: Annotation[] }) {
  return (
    <div className="flex flex-col gap-2">
      <h2 className="text-xl font-semibold">Annotations</h2>
      <AnnotationsTable annotations={annotations} />
    </div>
  )
}
