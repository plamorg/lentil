import Annotation from "./Annotation.tsx"

type Annotation = {
  output: string;
  comment: string;
}

export default function Annotations({ annotations }: { annotations: Annotation[] }) {
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
