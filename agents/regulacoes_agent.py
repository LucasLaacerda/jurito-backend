from models import VooData
from common import chamar_openai

SYSTEM_MESSAGE = (
    "Você é um especialista em direitos do passageiro aéreo. "
    "Explique de forma simples e direta os direitos do passageiro."
)

PROMPT_TEMPLATE = '''
1. Direitos do passageiro:
   - [Lista principal]

2. O que a companhia deve fazer:
   - [Obrigações]

3. Documentos necessários:
   - [Essenciais]

Dados:
Relato: {relato}
Origem: {origem}
Destino: {destino}
Voo: {voo}
Data: {data_voo}
Companhia: {cia}
Oferecido: {oferecido}
'''.strip()


def gerar_prompt(data: VooData) -> str:
    return PROMPT_TEMPLATE.format(
        relato=data.relato,
        origem=data.origem,
        destino=data.destino,
        voo=data.voo,
        data_voo=data.data_voo,
        cia=data.cia,
        oferecido=", ".join(data.oferecido)
    )


async def run(data: VooData) -> str:
    prompt = gerar_prompt(data)
    return await chamar_openai(prompt, SYSTEM_MESSAGE)