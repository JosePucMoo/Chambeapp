export const ProjectStatusEnum = {
  NOT_STARTED: "No iniciado",
  ACTIVE: "Activo",
  COMPLETED: "Completado",
  DELAYED: "Retrasado",
} as const;

export const RoleEnum = {
  OWNER: "Propietario",
  GUEST: "Invitado",
} as const;

export const TaskPriorityEnum = {
  LOW: "Baja",
  MEDIUM: "Normal",
  HIGH: "Alta",
  URGENT: "Urgente",
} as const;

export type ProjectStatusEnum =
  (typeof ProjectStatusEnum)[keyof typeof ProjectStatusEnum];

export type RoleEnum = (typeof RoleEnum)[keyof typeof RoleEnum];

export type TaskPriorityEnum =
  (typeof TaskPriorityEnum)[keyof typeof TaskPriorityEnum];
