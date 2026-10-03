import type { TaskPriorityEnum } from "./constants/enums";

export interface Task {
  id: string;
  title: string;
  description: string;
  priority: TaskPriorityEnum;
  dueDate: Date;
  columnId: string;
  assigneeId: string;
}

export interface CreateTask {
  title: string;
  description: string;
  priority: TaskPriorityEnum;
  dueDate: Date;
  assigneeId: string;
}
