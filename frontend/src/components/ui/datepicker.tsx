"use client";

import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Field } from "@/components/ui/field";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { formatDate } from "@/utils/dateFormatter";
import { es } from "date-fns/locale";

interface DatePickerProps {
  date?: Date;
  onChange: (date?: Date) => void;
  placeholder?: string;
}

export function DatePickerSimple({
  date,
  onChange,
  placeholder = "Seleccionar fecha",
}: DatePickerProps) {
  return (
    <Field className="mx-auto w-44">
      <Popover>
        <PopoverTrigger
          render={
            <Button
              variant="outline"
              id="date-picker-simple"
              className="justify-start font-normal text-gray-500"
            >
              {date ? formatDate(date.toString()) : <span>{placeholder}</span>}
            </Button>
          }
        />
        <PopoverContent className="w-auto p-0" align="start">
          <Calendar
            mode="single"
            selected={date}
            onSelect={onChange}
            defaultMonth={date}
            locale={es}
          />
        </PopoverContent>
      </Popover>
    </Field>
  );
}
