from models import VooData
from utils.common import chamar_openai

SYSTEM_MESSAGE = (
    "Você é um especialista em ajudar passageiros a resolver problemas com companhias aéreas. "
    "Forneça um plano de ação simples e prático."
)

PROMPT_TEMPLATE = '''
1. Primeiros passos:
   - [Ações iniciais]

2. Documentos necessários:
   - [Essenciais]

3. Como entrar em contato:
   - [Instruções]

4. Prazos:
   - [Prazos relevantes]

Dados:
Relato: {relato}
Companhia: {cia}
Data: {data_voo}
Cidade: {cidade_estado}
Valor: R$ {valor}
'''.strip()


def gerar_prompt(data: VooData) -> str:
    return PROMPT_TEMPLATE.format(
        relato=data.relato,
        cia=data.cia,
        data_voo=data.data_voo,
        cidade_estado=data.cidade_estado,
        valor=data.valor or 'Não informado'
    )


async def run(data: VooData) -> str:
    prompt = gerar_prompt(data)
    return await chamar_openai(prompt, SYSTEM_MESSAGE)