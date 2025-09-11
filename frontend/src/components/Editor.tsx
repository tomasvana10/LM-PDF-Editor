import { useCallback, useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import type { SubmitHandler } from "react-hook-form";
import { getAPIURL } from "../util/settings";
import { Asterisk, CircleX, RefreshCcw } from "lucide-react";

//@ts-expect-error works fine, disabling the option in tsconfig didn't work for some reason
enum FileFormat {
  html = "html",
  pdf = "pdf",
}

interface IFormInput {
  fileFormat: FileFormat;
  existingFile: FileList;
  userContext: string;
  model: string;
}

interface EditorProps {
  onObjectCreation: (url: string, fileFormat: FileFormat) => void;
}

export default function Editor({ onObjectCreation }: EditorProps) {
  const [models, setModels] = useState<string[]>([]);
  const rf = useForm<IFormInput>({
    defaultValues: { fileFormat: FileFormat.pdf },
  });

  const existingFile = rf.watch("existingFile");
  const fileFormat = rf.watch("fileFormat");

  const onSubmit: SubmitHandler<IFormInput> = async data => {
    const f = new FormData();
    f.append("user_context", data.userContext);
    f.append("model", data.model);
    if (data.existingFile?.[0]) {
      f.append("existing_file", data.existingFile[0]);
    }

    const res = await fetch(getAPIURL() + `/${data.fileFormat}`, {
      method: "POST",
      body: f,
    });

    const url = URL.createObjectURL(await res.blob());
    onObjectCreation(url, data.fileFormat);
    //window.open(url, "_blank");
  };

  const fetchModels = useCallback(async () => {
    const models = await fetch(getAPIURL() + "/models/active", {
      headers: { accept: "application/json" },
    })
      .then(res => res.json())
      .catch(() => []);

    const ids = models.map((model: Record<string, string>) => model.id);
    setModels(ids);

    if (ids.length) {
      rf.setValue("model", ids[0]);
    }
  }, [rf]);

  // fetch all modeels once on load
  useEffect(() => {
    fetchModels();
  }, [fetchModels]);

  // whenever fileFormat changes, trigger existing file to update the error message (if it exists)
  useEffect(() => {
    rf.trigger("existingFile");
  }, [rf, fileFormat]);

  return (
    <form onSubmit={rf.handleSubmit(onSubmit)}>
      <fieldset className="fieldset">
        <FieldHeader name="File format" required />
        <div className="flex flex-row gap-4">
          {Object.values(FileFormat).map(format => (
            <label key={format} className="flex items-center gap-2">
              <input
                type="radio"
                value={format}
                {...rf.register("fileFormat", {
                  required: "You must select a file format",
                })}
                className="radio"
              />
              {format.toUpperCase()}
            </label>
          ))}
        </div>
        <FormErrorMessage message={rf.formState.errors.fileFormat?.message} />
      </fieldset>

      <fieldset className="fieldset">
        <FieldHeader name="LMStudio model" required />
        <div className="flex flex-row gap-2">
          <select
            className="select"
            {...rf.register("model", { required: "You must select a model" })}>
            {models.map(model => (
              <option key={model} value={model}>
                {model}
              </option>
            ))}
          </select>
          <button
            type="button"
            className="btn btn-circle h-full"
            onClick={fetchModels}>
            <RefreshCcw className="size-4" />
          </button>
        </div>
        <FormErrorMessage message={rf.formState.errors.model?.message} />
      </fieldset>

      <fieldset className="fieldset">
        <FieldHeader name="Source file" />
        <div className="flex flex-row gap-2">
          <input
            type="file"
            multiple={false}
            {...rf.register("existingFile", {
              validate: (files: FileList) => {
                if (!files.length) return true;

                const extension = files[0].name.split(".").pop()?.toLowerCase();
                const fileFormat = rf.watch("fileFormat");
                return (
                  extension === fileFormat ||
                  `Invalid file extension (should end in .${fileFormat})`
                );
              },
            })}
            className="file-input"
          />
          <button
            type="button"
            className="btn btn-circle h-full"
            onClick={() => rf.resetField("existingFile")}>
            <CircleX className="size-4" />
          </button>
        </div>
        <FormErrorMessage message={rf.formState.errors.existingFile?.message} />
      </fieldset>

      <fieldset className="fieldset">
        <FieldHeader name="Instructions" required />
        <textarea
          {...rf.register("userContext", {
            required: "You must provide instructions",
            minLength: {
              value: 10,
              message: "Instructions must be at least 10 characters",
            },
          })}
          className="textarea min-h-[200px] "></textarea>
        <FormErrorMessage message={rf.formState.errors.userContext?.message} />
      </fieldset>

      <div className="divider"></div>
      <button className="btn btn-success" type="submit">
        {existingFile?.length ? "Edit" : "Create"}
      </button>
    </form>
  );
}

function FormErrorMessage({ message }: { message?: string }) {
  if (!message) return null;
  return <p className="text-red-500 text-sm">{message}</p>;
}

function FieldHeader({ name, required }: { name: string; required?: boolean }) {
  return (
    <legend className="fieldset-legend">
      <div className="flex items-center gap-1">
        {required ? <RequiredAsterisk /> : null}
        <span>{name}</span>
      </div>
    </legend>
  );
}

function RequiredAsterisk() {
  return <Asterisk className="stroke-red-500 size-3" />;
}
