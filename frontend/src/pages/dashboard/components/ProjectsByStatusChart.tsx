import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { ProjectStatusEnum } from "@/interfaces/constants/enums";
import type { ProjectStatusCount } from "@/interfaces/Dashboard";

const STATUS_COLORS: Record<string, string> = {
  [ProjectStatusEnum.NOT_STARTED]: "#94a3b8",
  [ProjectStatusEnum.ACTIVE]: "#3b82f6",
  [ProjectStatusEnum.DELAYED]: "#ef4444",
  [ProjectStatusEnum.COMPLETED]: "#10b981",
};

interface ProjectsByStatusChartProps {
  projectsByStatus: ProjectStatusCount[];
  totalProjects: number;
  isLoading?: boolean;
}

const ProjectsByStatusChart = ({
  projectsByStatus,
  totalProjects,
  isLoading = false,
}: ProjectsByStatusChartProps) => {
  const chartData = projectsByStatus.map((item) => ({
    name: item.status,
    value: item.total,
  }));

  return (
    <Card className="shadow-sm border-slate-200">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-bold text-slate-800">
          Proyectos por Estado
        </CardTitle>
        <CardDescription>
          Distribución de tus {totalProjects} proyecto
          {totalProjects === 1 ? "" : "s"}
        </CardDescription>
      </CardHeader>
      <CardContent className="pt-4">
        {isLoading ? (
          <Skeleton className="h-50 w-full" />
        ) : totalProjects === 0 ? (
          <div className="h-50 flex flex-col items-center justify-center gap-2 text-center">
            <p className="text-sm text-slate-500">
              Todavía no tienes proyectos registrados.
            </p>
          </div>
        ) : (
          <>
            <div className="h-50 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={chartData}
                    dataKey="value"
                    nameKey="name"
                    innerRadius="55%"
                    outerRadius="80%"
                    paddingAngle={2}
                    strokeWidth={0}
                  >
                    {chartData.map((entry) => (
                      <Cell
                        key={entry.name}
                        fill={STATUS_COLORS[entry.name] ?? "#cbd5e1"}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      borderRadius: "8px",
                      border: "none",
                      boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <ul className="mt-4 space-y-2">
              {chartData.map((entry) => (
                <li
                  key={entry.name}
                  className="flex items-center justify-between text-sm"
                >
                  <span className="flex items-center gap-2 text-slate-600">
                    <span
                      className="w-2.5 h-2.5 rounded-full shrink-0"
                      style={{
                        backgroundColor: STATUS_COLORS[entry.name] ?? "#cbd5e1",
                      }}
                    />
                    {entry.name}
                  </span>
                  <span className="font-semibold text-slate-800">
                    {entry.value}
                  </span>
                </li>
              ))}
            </ul>
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default ProjectsByStatusChart;
