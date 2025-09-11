import { useState } from "react";
import Editor from "./Editor";

function App() {
  const [objectURL, setObjectURL] = useState<string | null>(null);
  const [fileFormat, setFileFormat] = useState<string | null>(null);
  return (
    <div className="flex flex-row w-full max-[1350px]:flex-col">
      <div className="card outline-white outline w-fit m-4">
        <div className="card-body">
          <h2 className="card-title">LM PDF Editor</h2>
          <Editor
            onObjectCreation={(url, fileFormat) => {
              setObjectURL(url);
              setFileFormat(fileFormat);
            }}
          />
        </div>
      </div>

      {objectURL ? (
        <>
          <a
            href={objectURL}
            target="_blank"
            className="btn min-sm:hidden m-4"
            rel="noopener noreferrer"
            download={`document.${fileFormat}`}>
            Download PDF
          </a>
          <iframe
            src={objectURL}
            height={1000}
            className="h-[90vh] min-sm:flex-1 m-4"
            title={`Preview this ${fileFormat} document`}></iframe>
        </>
      ) : null}
    </div>
  );
}

export default App;
