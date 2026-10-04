import { Controller, type Control } from "react-hook-form";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { ProjectMember } from "@/interfaces/Project";
import type { CreateTask } from "@/interfaces/Task";

interface AssigneSelectProps {
  control: Control<CreateTask>;
  members: ProjectMember[];
}

export function AssigneeSelect({ control, members }: AssigneSelectProps) {
  return (
    <Controller
      name="assigneeId"
      control={control}
      rules={{ required: "Debes asignar a un responsable" }}
      render={({ field, fieldState }) => {
        const selectedUser = members.find(
          (m) => m.id.toString() === field.value,
        );

        return (
          <Field data-invalid={fieldState.invalid} className="w-full">
            <FieldLabel
              className={`text-md font-medium" ${!!fieldState.error ? "" : "text-slate-700"}`}
            >
              Asignar a
            </FieldLabel>

            <Select onValueChange={field.onChange} value={field.value || ""}>
              <SelectTrigger aria-invalid={fieldState.invalid}>
                <SelectValue placeholder="Selecciona un miembro">
                  {selectedUser ? selectedUser.name : undefined}
                </SelectValue>
              </SelectTrigger>

              <SelectContent>
                {members.map((user) => (
                  <SelectItem key={user.id} value={user.id}>
                    <div className="flex flex-col text-left p-1">
                      <span className="font-medium text-slate-900 leading-none mb-1.5">
                        {user.name}
                      </span>
                      <span className="text-xs text-slate-500 leading-none">
                        {user.email}
                      </span>
                    </div>
                  </SelectItem>
                ))}
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
