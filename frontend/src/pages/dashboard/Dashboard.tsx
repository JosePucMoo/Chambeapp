import { useState } from "react";
import MetricCard from "./components/MetricCard";
import ProjectsByStatusChart from "./components/ProjectsByStatusChart";
import DueSoonTasksDialog from "./components/DueSoonTasksDialog";
import {
  AlertCircle,
  CheckCircle2,
  CheckSquare,
  Clock,
  Inbox,
  RefreshCw,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { useDashboard, useDueSoonTasks } from "@/hooks/useDashboard";

const Dashboard = () => {
  const { metrics, isLoading, error, isEmpty, loadMetrics } = useDashboard();
  const [isDueSoonOpen, setIsDueSoonOpen] = useState(false);
  const {
    tasks: dueSoonTasks,
    isLoading: isDueSoonLoading,
    error: dueSoonError,
    loadTasks: loadDueSoonTasks,
  } = useDueSoonTasks();

  const handleDueSoonClick = () => {
    setIsDueSoonOpen(true);
    loadDueSoonTasks();
  };

  const showEmptyState = !isLoading && !error && isEmpty;

  return (
    <div className="p-8 bg-slate-50 min-h-screen space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard
          title="Total de Tareas"
          value={metrics.totalTasks}
          icon={<CheckSquare className="text-indigo-500 w-5 h-5" />}
          isLoading={isLoading}
        />
        <MetricCard
          title="Tareas Completadas"
          value={metrics.completedTasks}
          icon={<CheckCircle2 className="text-emerald-500 w-5 h-5" />}
          isLoading={isLoading}
        />
        <MetricCard
          title="Tareas Vencen Pronto"
          value={metrics.tasksDueSoon}
          icon={<Clock className="text-rose-500 w-5 h-5" />}
          isLoading={isLoading}
          onClick={handleDueSoonClick}
        />
      </div>

      {error && (
        <Card className="border-rose-200 bg-rose-50 shadow-sm">
          <CardContent className="p-6 flex flex-col sm:flex-row items-start sm:items-center gap-4 justify-between">
            <div className="flex items-start gap-3">
              <AlertCircle className="text-rose-500 w-5 h-5 mt-0.5 shrink-0" />
              <div>
                <p className="font-medium text-rose-900">
                  No pudimos cargar tus métricas
                </p>
                <p className="text-sm text-rose-700 mt-0.5">{error}</p>
              </div>
            </div>
            <Button variant="outline" size="sm" onClick={loadMetrics}>
              <RefreshCw className="w-4 h-4 mr-2" />
              Reintentar
            </Button>
          </CardContent>
        </Card>
      )}

      {showEmptyState && (
        <Card className="border-slate-200 shadow-sm">
          <CardContent className="p-10 flex flex-col items-center text-center gap-3">
            <div className="p-4 bg-slate-100 rounded-full">
              <Inbox className="text-slate-400 w-6 h-6" />
            </div>
            <div>
              <p className="font-medium text-slate-800">
                Aún no tienes nada por mostrar
              </p>
              <p className="text-sm text-slate-500 mt-1">
                Crea tu primer proyecto y agrega tareas para ver aquí tus
                métricas.
              </p>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={loadMetrics}
              className="mt-2"
            >
              <RefreshCw className="w-4 h-4 mr-2" />
              Actualizar
            </Button>
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <ProjectsByStatusChart
          projectsByStatus={metrics.projectsByStatus}
          totalProjects={metrics.totalProjects}
          isLoading={isLoading}
        />

        <Card className="lg:col-span-2 shadow-sm border-slate-200">
          <CardHeader className="pb-2">
            <CardTitle className="text-lg font-bold text-slate-800">
              Rendimiento Semanal
            </CardTitle>
            <CardDescription>
              Tareas completadas vs. nuevas en los últimos 7 días
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            {isLoading ? (
              <div className="h-75 w-full flex items-end gap-4 px-2">
                {Array.from({ length: 7 }).map((_, index) => (
                  <Skeleton key={index} className="flex-1 h-full" />
                ))}
              </div>
            ) : (
              <div className="h-75 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={metrics.weeklyPerformance}
                    margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
                  >
                    <CartesianGrid
                      strokeDasharray="3 3"
                      vertical={false}
                      stroke="#e2e8f0"
                    />
                    <XAxis
                      dataKey="name"
                      axisLine={false}
                      tickLine={false}
                      tick={{ fill: "#64748b", fontSize: 12 }}
                      dy={10}
                    />
                    <YAxis
                      axisLine={false}
                      tickLine={false}
                      tick={{ fill: "#64748b", fontSize: 12 }}
                      allowDecimals={false}
                    />
                    <Tooltip
                      cursor={{ fill: "#f1f5f9" }}
                      contentStyle={{
                        borderRadius: "8px",
                        border: "none",
                        boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                      }}
                    />
                    <Bar
                      dataKey="completed"
                      name="Completadas"
                      fill="#3b82f6"
                      radius={[4, 4, 0, 0]}
                      barSize={30}
                    />
                    <Bar
                      dataKey="created"
                      name="Nuevas"
                      fill="#cbd5e1"
                      radius={[4, 4, 0, 0]}
                      barSize={30}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <DueSoonTasksDialog
        open={isDueSoonOpen}
        onOpenChange={setIsDueSoonOpen}
        totalDueSoon={metrics.tasksDueSoon}
        tasks={dueSoonTasks}
        isLoading={isDueSoonLoading}
        error={dueSoonError}
        onRetry={loadDueSoonTasks}
      />
    </div>
  );
};

export default Dashboard;
