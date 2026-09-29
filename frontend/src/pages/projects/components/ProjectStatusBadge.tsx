import { Badge } from "@/components/ui/badge";
import { ProjectStatusEnum } from "@/interfaces/constants/enums";

interface ProjectStatusBadgeProps {
  status: ProjectStatusEnum;
  className?: string;
}

const ProjectStatusBadge = ({
  status,
  className = "",
}: ProjectStatusBadgeProps) => {
  let baseClasses =
    "font-medium text-sm rounded-full px-3 py-4 shadow-none border-none";

  switch (status) {
    case ProjectStatusEnum.ACTIVE:
      baseClasses = `bg-blue-100 text-blue-700 hover:bg-blue-200 ${baseClasses} ${className}`;
      break;
    case ProjectStatusEnum.DELAYED:
      baseClasses = `bg-red-100 text-red-700 hover:bg-red-200 ${baseClasses} ${className}`;
      break;
    case ProjectStatusEnum.COMPLETED:
      baseClasses = `bg-emerald-100 text-emerald-700 hover:bg-emerald-200 ${baseClasses} ${className}`;
      break;
    case ProjectStatusEnum.NOT_STARTED:
      baseClasses = `bg-gray-100 text-gray-700 hover:bg-gray-200 ${baseClasses} ${className}`;
      break;
    default:
      baseClasses = `bg-gray-100 text-gray-700 hover:bg-gray-200 ${baseClasses} ${className}`;
      break;
  }

  return <Badge className={`bg-gray-100 ${baseClasses}`}>{status}</Badge>;
};

export default ProjectStatusBadge;
