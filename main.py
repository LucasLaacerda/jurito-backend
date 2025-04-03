# Jurito Viagens Pro - Backend (FastAPI + OpenAI)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    valor: str
    cidade_estado: str

ANALISE_PROMPT = """
Você é um advogado especialista em direitos do consumidor e voos. Analise o seguinte caso com base nas informações fornecidas. Retorne os seguintes blocos, separados e formatados:

1. **Resumo do Caso**: Resuma o que aconteceu de forma clara e objetiva.

2. **Regulações Aplicáveis**: Liste as leis e regras que se aplicam ao caso (ex: ANAC, Código do Consumidor).

3. **Análise de Viabilidade**: Diga se o caso é forte e por quê. Dê uma nota de viabilidade (0 a 100%) com base nas chances reais de sucesso.

4. **Potencial de Compensação**: Com base nas regulações, quanto a pessoa pode solicitar (valor estimado).

5. **Plano de Ação**: Explique quais passos ela pode seguir (ex: carta, juizado, Procon etc).

6. **Petição Inicial**: Caso seja viável, gere a minuta de uma petição inicial para o Juizado Especial Cível, com base nas informações abaixo.

Informações:
- Nome: {nome}
- CPF: {cpf}
- Email: {email}
- Companhia aérea: {cia}
- Número do voo: {voo}
- Origem: {origem}
- Destino: {destino}
- Data do voo: {data_voo}
- O que foi oferecido: {oferecido}
- Valor desejado: R$ {valor}
- Cidade onde abrirá processo: {cidade_estado}
- Relato: {relato}

Organize a resposta com subtítulos e clareza.
"""

@app.post("/avaliar-caso")
async def avaliar_caso(data: VooData):
    prompt = ANALISE_PROMPT.format(**data.dict())

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um advogado que atua com voos, ANAC e direito do consumidor."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"resposta": response.choices[0].message.content}
