from models import VooData
from common import chamar_openai

SYSTEM_MESSAGE = (
    "Você é um advogado especialista em direito do consumidor e transporte aéreo. "
    "Forneça APENAS a chance de sucesso em porcentagem."
)

PROMPT_TEMPLATE = 'Chance de sucesso: X%'


def gerar_prompt(data: VooData) -> str:
    return (
        f"Chance de sucesso:"
        f"Dados do Caso:"
        f"Relato: {data.relato}"
        f"Companhia: {data.cia}"
        f"Voo: {data.voo} ({data.origem}->{data.destino} em {data.data_voo})"
        f"Oferecido: {', '.join(data.oferecido)}"
        f"Valor: R$ {data.valor or 'Não informado'}"
    )


async def run(data: VooData) -> str:
    prompt = gerar_prompt(data)
    return await chamar_openai(prompt, SYSTEM_MESSAGE)