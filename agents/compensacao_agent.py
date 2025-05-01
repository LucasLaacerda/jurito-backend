from models import VooData
from common import chamar_openai

SYSTEM_MESSAGE = (
    "Você é especialista em compensações por problemas em voos. "
    "Retorne apenas valores em R$ no formato mínimo, médio e máximo."
)

PROMPT_TEMPLATE = '''
Valor mínimo: R$ X
Valor médio: R$ Y
Valor máximo: R$ Z

Dados:
Relato: {relato}
Oferecido: {oferecido}
Origem: {origem}
Destino: {destino}
Data: {data_voo}
Valor desejado: R$ {valor}
'''.strip()


def gerar_prompt(data: VooData) -> str:
    return PROMPT_TEMPLATE.format(
        relato=data.relato,
        oferecido=", ".join(data.oferecido),
        origem=data.origem,
        destino=data.destino,
        data_voo=data.data_voo,
        valor=data.valor or 'Não informado'
    )


async def run(data: VooData) -> str:
    prompt = gerar_prompt(data)
    return await chamar_openai(prompt, SYSTEM_MESSAGE)