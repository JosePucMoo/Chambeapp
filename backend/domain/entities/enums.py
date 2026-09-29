from enum import Enum

class TaskPriorityEnum(str, Enum):
    LOW = 'Baja'
    MEDIUM = 'Normal'
    HIGH = 'Alta'
    URGENT = 'Urgente'

class RoleEnum(str, Enum):
    OWNER = "Propietario"
    GUEST = "Invitado"

class ColumnDefaultEnum(str, Enum):
    TO_DO = "Por hacer"
    IN_PROGRESS = "En progreso"
    COMPLETED = "Completado"

class ProjectStatusEnum(str, Enum):
    NOT_STARTED = 'No iniciado'
    ACTIVE = "Activo"
    DELAYED = "Retrasado"
    COMPLETED = "Completado"