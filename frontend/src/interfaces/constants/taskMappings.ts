import { ColumnDefaultEnum, TaskPriorityEnum } from "./enums";

export interface PriorityUIConfig {
  label: string;
  colorClass: string;
}

export interface ColumnStateUIConfig {
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

export const COLUMN_STATE_CONFIG: Record<
  ColumnDefaultEnum,
  ColumnStateUIConfig
> = {
  [ColumnDefaultEnum.TO_DO]: {
    label: ColumnDefaultEnum.TO_DO,
    colorClass: "bg-blue-500",
  },
  [ColumnDefaultEnum.IN_PROGRESS]: {
    label: ColumnDefaultEnum.IN_PROGRESS,
    colorClass: "bg-yellow-500",
  },
  [ColumnDefaultEnum.COMPLETED]: {
    label: ColumnDefaultEnum.COMPLETED,
    colorClass: "bg-emerald-500",
  },
};
