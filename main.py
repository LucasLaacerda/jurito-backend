# Jurito Viagens Pro - Backend (FastAPI + OpenAI)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# Imports dos agents
from agents import (
    resumo_agent,
    regulacoes_agent,
    viabilidade_agent,
    compensacao_agent,
    acao_agent
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    valor: str
    cidade_estado: str

# Rota para análise completa (modelo antigo unificado)
@app.post("/avaliar-caso")
async def avaliar_caso(data: VooData):
    prompt = f"""
Você é um advogado especialista em direitos do consumidor e voos. Analise o seguinte caso com base nas informações fornecidas. Retorne os seguintes blocos, separados e formatados:

1. **Resumo do Caso**
2. **Regulações Aplicáveis**
3. **Análise de Viabilidade**
4. **Potencial de Compensação**
5. **Plano de Ação**
6. **Petição Inicial**

Informações:
{data.json(indent=2)}
""".strip()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um advogado especialista em voos e defesa do consumidor."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"resposta": response.choices[0].message.content}


# === Rotas modulares por agente ===

@app.post("/gerar-resumo")
async def gerar_resumo(data: VooData):
    prompt = resumo_agent.gerar_prompt(data)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um advogado especialista em direito do consumidor."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"resposta": response.choices[0].message.content}


@app.post("/avaliar-regulacoes")
async def avaliar_regulacoes(data: VooData):
    prompt = regulacoes_agent.gerar_prompt(data)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um especialista em normas internacionais de aviação civil."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"resposta": response.choices[0].message.content}


@app.post("/avaliar-viabilidade")
async def avaliar_viabilidade(data: VooData):
    prompt = viabilidade_agent.gerar_prompt(data)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um advogado que avalia a força de casos jurídicos contra companhias aéreas."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"resposta": response.choices[0].message.content}


@app.post("/calcular-compensacao")
async def calcular_compensacao(data: VooData):
    prompt = compensacao_agent.gerar_prompt(data)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um especialista em compensações por atrasos e cancelamentos de voo."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"resposta": response.choices[0].message.content}


@app.post("/gerar-plano-acao")
async def gerar_plano_acao(data: VooData):
    prompt = acao_agent.gerar_prompt(data)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um advogado que orienta consumidores a buscar seus direitos."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"resposta": response.choices[0].message.content}
