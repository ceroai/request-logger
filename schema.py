from pydantic import BaseModel



class AgendamientoSchema(BaseModel):
    telefono: str
    rut_paciente: str | None = None
    intencion_flujo: str | None = None
    clinica: str | None = None