import Annotation from "./Annotation.tsx";

export type Annotation = {
  command_output: Array<string>;
  comment: string;
};

function AnnotationsTable({ annotations }: { annotations: Annotation[] }) {
  return (
    <div className="flex flex-col gap-4">
      {annotations.map((annotation, index) => (
        <Annotation
          key={index}
          output={annotation.command_output.join("\n")}
          comment={annotation.comment}
        />
      ))}
    </div>
  );
}

export function Annotations({ annotations }: { annotations: Annotation[] }) {
  return (
    <div className="flex flex-col gap-2">
      <h2 className="text-xl font-medium mb-3 mt-5">Here's why.</h2>
      <AnnotationsTable annotations={annotations} />
    </div>
  );
}
