from enum import Enum

class PriorityLevelEnum(str, Enum):
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