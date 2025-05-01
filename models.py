from pydantic import BaseModel
from typing import Optional, Dict, Any

# Modelo de dados recebidos
class VooData(BaseModel):
    relato: str
    nome: str
    cpf: str
    email: str
    cia: str
    voo: str
    origem: str
    destino: str
    data_voo: str
    oferecido: list[str]
    valor: Optional[str] = None
    cidade_estado: str

# Modelo de resposta padronizada
class RespostaAgente(BaseModel):
    status: str
    dados: Dict[str, Any]
    mensagem: Optional[str] = None