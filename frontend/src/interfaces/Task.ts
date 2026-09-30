export interface Task {
  id: string;
  title: string;
  description: string;
  priority: string;
  dueDate: Date;
  columnId: string;
  assigneeId?: string;
}
