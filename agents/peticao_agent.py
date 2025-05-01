from models import VooData
from common import chamar_openai

SYSTEM_MESSAGE = (
    "Você é um advogado com vasta experiência na redação de petições iniciais. "
    "Use formatação jurídica padrão e linguagem formal."
)

PROMPT_TEMPLATE = '''
Dados do Caso:
- Nome: {nome}
- CPF: {cpf}
- Companhia: {cia}
- Voo: {voo} ({origem}->{destino} em {data_voo})
- Relato: {relato}
- Oferecido: {oferecido}
- Valor pretendido: R$ {valor}
- Resumo: {resumo}
- Direitos: {regulacoes}
- Chance: {viabilidade}%
- Comp. Mín: R$ {min_comp}, Méd: R$ {med_comp}, Máx: R$ {max_comp}

Redija a petição inicial completa seguindo a estrutura legal brasileira.
'''.strip()

async def run(
    data: VooData,
    resumo: str,
    regulacoes: str,
    viabilidade: int,
    min_comp: float,
    med_comp: float,
    max_comp: float
) -> str:
    prompt = PROMPT_TEMPLATE.format(
        nome=data.nome,
        cpf=data.cpf,
        cia=data.cia,
        voo=data.voo,
        origem=data.origem,
        destino=data.destino,
        data_voo=data.data_voo,
        relato=data.relato,
        oferecido=", ".join(data.oferecido),
        valor=data.valor or 'Não informado',
        resumo=resumo,
        regulacoes=regulacoes,
        viabilidade=viabilidade,
        min_comp=min_comp,
        med_comp=med_comp,
        max_comp=max_comp
    )
    return await chamar_openai(prompt, SYSTEM_MESSAGE)