import { useCallback, useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import type { SubmitHandler } from "react-hook-form";
import { getAPIURL } from "../util/settings";
import { Asterisk, RefreshCcw } from "lucide-react";

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

export default function Editor() {
  const [models, setModels] = useState<string[]>([]);
  const {
    register,
    handleSubmit,
    setValue,
    formState: { errors },
  } = useForm<IFormInput>({
    defaultValues: { fileFormat: FileFormat.pdf, model: "" },
  });

  const onSubmit: SubmitHandler<IFormInput> = data => {
    alert(JSON.stringify(data));
  };

  const fetchModels = useCallback(async () => {
    const models = await fetch(getAPIURL() + "/models/active", {
      headers: { accept: "application/json" },
    })
      .then(res => res.json())
      .catch(() => []);

    const ids = models.map((model: Record<string, string>) => model.id);
    setModels(ids);

    if (ids.length && !ids.includes(errors.model?.message)) {
      setValue("model", ids[0]);
    }
  }, [setValue, errors.model]);

  useEffect(() => {
    fetchModels();
  }, [fetchModels]);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <fieldset className="fieldset">
        <FieldHeader name="File format" required />
        <div className="flex flex-row gap-4">
          {Object.values(FileFormat).map(format => (
            <label key={format} className="flex items-center gap-2">
              <input
                type="radio"
                value={format}
                {...register("fileFormat", {
                  required: "You must select a file format",
                })}
                className="radio"
              />
              {format.toUpperCase()}
            </label>
          ))}
        </div>
        <FormErrorMessage message={errors.fileFormat?.message} />
      </fieldset>

      <fieldset className="fieldset">
        <FieldHeader name="LMStudio model" required />
        <div className="flex flex-row gap-2">
          <select
            className="select"
            {...register("model", { required: "You must select a model" })}>
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
        <FormErrorMessage message={errors.model?.message} />
      </fieldset>

      <fieldset className="fieldset">
        <FieldHeader name="Source file" />
        <input
          type="file"
          {...register("existingFile")}
          className="file-input"
        />
      </fieldset>

      <fieldset className="fieldset">
        <FieldHeader name="Instructions" required />
        <textarea
          {...register("userContext", {
            required: "You must provide instructions",
            minLength: {
              value: 10,
              message: "Instructions must be at least 10 characters",
            },
          })}
          className="textarea min-h-[200px] "></textarea>
        <FormErrorMessage message={errors.userContext?.message} />
      </fieldset>

      <div className="divider"></div>
      <button className="btn btn-success" type="submit">
        Submit
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
        {required ? <Required /> : null}
        <span>{name}</span>
      </div>
    </legend>
  );
}

function Required() {
  return <Asterisk className="stroke-red-500 size-3" />;
}
