# Jurito Viagens - Backend (FastAPI + OpenAI)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://jurito-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia o client OpenAI
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

PETICAO_PROMPT = """
Você é um advogado especialista em direitos do consumidor e legislação da ANAC. Gere uma petição inicial para o Juizado Especial Cível com base nas informações abaixo:

Dados do passageiro:
- Nome: {nome}
- CPF: {cpf}
- E-mail: {email}
- Companhia aérea: {cia}
- Número do voo: {voo}
- Aeroporto de origem: {origem}
- Aeroporto de destino: {destino}
- Data e horário do voo: {data_voo}
- Descrição do problema: {relato}
- O que foi (ou não foi) oferecido: {oferecido}
- Valor desejado: R$ {valor}
- Cidade onde o processo será aberto: {cidade_estado}

Com base na Resolução 400 da ANAC, fundamente os direitos violados e redija a petição inicial com uma linguagem clara, objetiva e jurídica.
"""

@app.post("/gerar-peticao")
async def gerar_peticao(data: VooData):
    prompt = PETICAO_PROMPT.format(**data.dict())

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um advogado especialista em processos de passageiros."},
            {"role": "user", "content": prompt}
        ]
    )

    resultado = response.choices[0].message.content
    return {"peticao": resultado}