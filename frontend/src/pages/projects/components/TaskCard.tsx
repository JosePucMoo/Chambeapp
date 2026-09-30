import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { Task } from "@/interfaces/Task";
import { formatDate } from "@/utils/dateFormatter";
import { useDraggable } from "@dnd-kit/react";
import { CalendarDays } from "lucide-react";

export function TaskCard({ task }: { task: Task }) {
  const { ref } = useDraggable({
    id: task.id,
  });

  return (
    <Card ref={ref} className="mx-auto w-full pt-0 ring-0">
      <CardAction className="pt-2 pl-2">
        <Badge variant="secondary">{task.priority}</Badge>
      </CardAction>
      <CardHeader className="">
        <CardTitle className="text-lg font-semibold">{task.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <CardDescription>{task.description}</CardDescription>
      </CardContent>
      <CardFooter className="flex justify-end bg-white">
        <div className="flex items-center text-gray-500 font-medium gap-2 text-sm">
          <CalendarDays className="w-4 h-4" />
          {formatDate(task.dueDate.toString())}
        </div>
      </CardFooter>
    </Card>
  );
}
