import { type Control, Controller } from "react-hook-form";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { TaskPriorityEnum } from "@/interfaces/constants/enums";
import type { CreateTask } from "@/interfaces/Task";
import { PRIORITY_CONFIG } from "@/interfaces/constants/taskMappings";

interface PrioritySelectProps {
  control: Control<CreateTask>;
}

export function PrioritySelect({ control }: PrioritySelectProps) {
  return (
    <Controller
      name="priority"
      control={control}
      rules={{ required: "Debes seleccionar una prioridad" }}
      render={({ field, fieldState }) => {
        const selectedConfig = field.value
          ? PRIORITY_CONFIG[field.value as TaskPriorityEnum]
          : null;

        return (
          <Field data-invalid={fieldState.invalid} className="w-full">
            <FieldLabel>Prioridad</FieldLabel>

            <Select onValueChange={field.onChange} value={field.value || ""}>
              <SelectTrigger aria-invalid={fieldState.invalid}>
                <SelectValue placeholder="Selecciona la prioridad">
                  {selectedConfig ? (
                    <div className="flex items-center gap-2">
                      <span
                        className={`w-2 h-2 rounded-full ${selectedConfig.colorClass.split(" ")[1]}`}
                      />
                      <span>{selectedConfig.label}</span>
                    </div>
                  ) : undefined}
                </SelectValue>
              </SelectTrigger>

              <SelectContent>
                {Object.values(TaskPriorityEnum).map((priorityValue) => {
                  const config = PRIORITY_CONFIG[priorityValue];

                  return (
                    <SelectItem key={priorityValue} value={priorityValue}>
                      <div className="flex items-center gap-2">
                        <span
                          className={`px-2 py-0.5 rounded text-xs font-medium ${config.colorClass}`}
                        >
                          {config.label}
                        </span>
                      </div>
                    </SelectItem>
                  );
                })}
              </SelectContent>
            </Select>

            {fieldState.error && (
              <FieldError>{fieldState.error.message}</FieldError>
            )}
          </Field>
        );
      }}
    />
  );
}
