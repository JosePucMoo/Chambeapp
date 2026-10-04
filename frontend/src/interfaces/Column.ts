import type { TaskCardSummary } from "./Task";

export interface ColumnBoard {
  id: string;
  title: string;
  position: number;
  tasks: TaskCardSummary[];
}
