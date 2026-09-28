from enum import Enum

class TaskPriorityEnum(str, Enum):
    low = 'Baja'
    medium = 'Normal'
    high = 'Alta'
    urgent = 'Urgente'

class RoleEnum(str, Enum):
    owner = "Propietario"
    guest = "Invitado"

class ColumnDefaultEnum(str, Enum):
    to_do = "Por hacer"
    in_progress = "En progreso"
    completed = "Completado"

class ProjectStatusEnum(str, Enum):
    uninitiated = 'No iniciado'
    active = "Activo"
    risk = "En riesgo"
    completed = "Completado"