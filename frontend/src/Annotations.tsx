import Annotation from "./Annotation.tsx"

type Annotation = {
  output: string;
  comment: string;
}

function AnnotationsTable({ annotations }: { annotations: Annotation[] }) {
  return (
      <div className="flex flex-col gap-4">
          {annotations.map((annotation, index) => (
              <Annotation
                  key={index}
                  output={annotation.output}
                  comment={annotation.comment}
              />
          ))}
      </div>
  );
}

export default function Annotations({ annotations }: { annotations: Annotation[] }) {
  return (
    <div className="flex flex-col gap-2">
      <h2 className="text-xl font-medium my-3">Here's why.</h2>
      <AnnotationsTable annotations={annotations} />
    </div>
  )
}
