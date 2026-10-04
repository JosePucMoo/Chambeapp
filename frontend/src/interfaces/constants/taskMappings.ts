import { TaskPriorityEnum } from "./enums";

export interface PriorityUIConfig {
  label: string;
  colorClass: string;
}

export const PRIORITY_CONFIG: Record<TaskPriorityEnum, PriorityUIConfig> = {
  [TaskPriorityEnum.LOW]: {
    label: TaskPriorityEnum.LOW,
    colorClass: "text-blue-600 bg-blue-100",
  },
  [TaskPriorityEnum.MEDIUM]: {
    label: TaskPriorityEnum.MEDIUM,
    colorClass: "text-amber-600 bg-amber-100",
  },
  [TaskPriorityEnum.HIGH]: {
    label: TaskPriorityEnum.HIGH,
    colorClass: "text-orange-600 bg-orange-100",
  },
  [TaskPriorityEnum.URGENT]: {
    label: TaskPriorityEnum.URGENT,
    colorClass: "text-red-600 bg-red-100",
  },
};
