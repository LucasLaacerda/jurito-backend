from models import VooData
from common import chamar_openai

SYSTEM_MESSAGE = (
    "Você é um especialista em ajudar passageiros a entender seus problemas com companhias aéreas. "
    "Use linguagem simples e direta."
)

PROMPT_TEMPLATE = '''
Faça um resumo SIMPLES e CLARO do caso, como se estivesse explicando para uma pessoa leiga.

1. O que aconteceu:
   - [Explique o problema]

2. O que a companhia fez:
   - [Descreva a resposta]

3. O que você pode fazer:
   - [Liste 2-3 opções simples]

Dados:
Nome: {nome}
Relato: {relato}
Origem: {origem}
Destino: {destino}
Voo: {voo}
Data: {data_voo}
Oferecido: {oferecido}
Valor: R$ {valor}
'''.strip()


def gerar_prompt(data: VooData) -> str:
    return PROMPT_TEMPLATE.format(
        nome=data.nome,
        relato=data.relato,
        origem=data.origem,
        destino=data.destino,
        voo=data.voo,
        data_voo=data.data_voo,
        oferecido=", ".join(data.oferecido),
        valor=data.valor or 'Não informado'
    )


async def run(data: VooData) -> str:
    prompt = gerar_prompt(data)
    return await chamar_openai(prompt, SYSTEM_MESSAGE)