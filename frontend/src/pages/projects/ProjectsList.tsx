import { useEffect, useState } from "react";
import { useOutletContext } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { Filter, FolderGit2 } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { LayoutContextType } from "@/interfaces/Context";
import { CreateProjectDialog } from "./components/CreateProjectDialog";
import { useProjects } from "@/hooks/useProjects";
import { ProjectTableRow } from "./components/ProjectTableRow";

function ProjectsList() {
  const { setPageTitle } = useOutletContext<LayoutContextType>();

  const [selectedProjects, setSelectedProjects] = useState<string[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(5);

  const { projects, isLoading, totalCount, totalPages, loadProjects } =
    useProjects(currentPage, itemsPerPage);

  useEffect(() => {
    setPageTitle("Proyectos");
  }, [setPageTitle]);

  const handleItemsPerPageChange = (value: string | null) => {
    if (!value) return;
    setItemsPerPage(Number(value));
    setCurrentPage(1);
  };

  const handlePageChange = (page: number, e: React.MouseEvent) => {
    e.preventDefault();
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  const toggleSelectAll = () => {
    if (selectedProjects.length === projects.length && projects.length > 0) {
      setSelectedProjects([]);
    } else {
      setSelectedProjects(projects.map((p) => p.id));
    }
  };

  const toggleSelectProject = (id: string) => {
    if (selectedProjects.includes(id)) {
      setSelectedProjects(
        selectedProjects.filter((projectId) => projectId !== id),
      );
    } else {
      setSelectedProjects([...selectedProjects, id]);
    }
  };

  const startIndex = (currentPage - 1) * itemsPerPage;

  return (
    <div className="flex flex-col space-y-6 w-full mx-auto p-6 md:p-8">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-100 text-blue-600 rounded-lg">
            <FolderGit2 className="w-12 h-12" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-700">Proyectos</h1>
            <p className="text-sm text-slate-500">
              Gestiona todos los portafolios activos
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          <Button
            variant="outline"
            className="text-slate-700 font-medium h-10 border-slate-300"
          >
            <Filter className="w-4 h-4 mr-2 text-slate-500" />
            Filtrar
          </Button>
          <CreateProjectDialog loadProyects={loadProjects} />
        </div>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden flex flex-col">
        <Table>
          <TableHeader>
            <TableRow className="hover:bg-slate-100 border-b-slate-100 last:border-0 group transition-colors">
              <TableHead className="w-12.5 pl-6">
                <Checkbox
                  checked={
                    selectedProjects.length === projects.length &&
                    projects.length > 0
                  }
                  onCheckedChange={toggleSelectAll}
                  className="border-slate-300 rounded-lg"
                />
              </TableHead>
              <TableHead className="font-semibold text-slate-700">
                Nombre del Proyecto
              </TableHead>
              <TableHead className="font-semibold text-slate-700">
                Rol
              </TableHead>
              <TableHead className="font-semibold text-slate-700">
                Fecha de Entrega
              </TableHead>
              <TableHead className="font-semibold text-slate-700">
                Estado
              </TableHead>
              <TableHead className="font-semibold text-slate-700 w-50">
                Progreso General
              </TableHead>
              <TableHead className="w-12.5"></TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell colSpan={7} className="h-24 text-center">
                  Cargando proyectos...
                </TableCell>
              </TableRow>
            ) : projects.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} className="h-24 text-center">
                  No se encontraron proyectos.
                </TableCell>
              </TableRow>
            ) : (
              projects.map((project) => (
                <ProjectTableRow
                  key={project.id}
                  project={project}
                  isSelected={selectedProjects.includes(project.id)}
                  onToggleSelect={toggleSelectProject}
                />
              ))
            )}
          </TableBody>
        </Table>

        <div className="border-t border-slate-200 py-4 px-6 bg-slate-50/30 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <p className="text-sm text-slate-500 font-medium">Mostrar</p>
            <Select
              value={itemsPerPage.toString()}
              onValueChange={handleItemsPerPageChange}
            >
              <SelectTrigger className="h-8 w-17.5 bg-white">
                <SelectValue placeholder={itemsPerPage} />
              </SelectTrigger>
              <SelectContent side="top">
                {[5, 10, 20, 50].map((pageSize) => (
                  <SelectItem key={pageSize} value={`${pageSize}`}>
                    {pageSize}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <p className="text-sm text-slate-500 font-medium">
              registros por página
            </p>
          </div>

          <div className="flex items-center gap-6">
            <p className="text-sm text-slate-500 font-medium hidden md:block">
              {startIndex + 1} -{" "}
              {Math.min(startIndex + itemsPerPage, totalCount)} de {totalCount}
            </p>

            <Pagination className="justify-end w-auto mx-0">
              <PaginationContent>
                <PaginationItem>
                  <PaginationPrevious
                    href="#"
                    onClick={(e) => handlePageChange(currentPage - 1, e)}
                    className={
                      currentPage === 1
                        ? "pointer-events-none opacity-50"
                        : "cursor-pointer"
                    }
                  />
                </PaginationItem>

                {Array.from({ length: totalPages }).map((_, i) => (
                  <PaginationItem key={i} className="hidden sm:inline-block">
                    <PaginationLink
                      href="#"
                      isActive={currentPage === i + 1}
                      onClick={(e) => handlePageChange(i + 1, e)}
                    >
                      {i + 1}
                    </PaginationLink>
                  </PaginationItem>
                ))}

                <PaginationItem>
                  <PaginationNext
                    href="#"
                    onClick={(e) => handlePageChange(currentPage + 1, e)}
                    className={
                      currentPage === totalPages || totalPages === 0
                        ? "pointer-events-none opacity-50"
                        : "cursor-pointer"
                    }
                  />
                </PaginationItem>
              </PaginationContent>
            </Pagination>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProjectsList;
