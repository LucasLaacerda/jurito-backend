# Jurito Viagens Pro - Backend (FastAPI + OpenAI)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from typing import Optional, Dict, Any
import json

# Imports dos agents
from agents import (
    resumo_agent,
    regulacoes_agent,
    viabilidade_agent,
    compensacao_agent,
    acao_agent
)

app = FastAPI(
    title="Jurito API",
    description="API para análise jurídica de casos envolvendo companhias aéreas",
    version="1.0.0"
)

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
    valor: Optional[str] = None
    cidade_estado: str

# Modelo de resposta padronizada
class RespostaAgente(BaseModel):
    status: str
    dados: Dict[str, Any]
    mensagem: Optional[str] = None

async def processar_resposta_agente(prompt: str, system_message: str) -> RespostaAgente:
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return RespostaAgente(
            status="success",
            dados={"resposta": response.choices[0].message.content},
            mensagem="Análise concluída com sucesso"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar a análise: {str(e)}"
        )

# Rotas modulares por agente
@app.post("/gerar-resumo", response_model=RespostaAgente)
async def gerar_resumo(data: VooData):
    prompt = resumo_agent.gerar_prompt(data)
    return await processar_resposta_agente(
        prompt,
        "Você é um advogado especialista em direito do consumidor e transporte aéreo."
    )

@app.post("/avaliar-regulacoes", response_model=RespostaAgente)
async def avaliar_regulacoes(data: VooData):
    prompt = regulacoes_agent.gerar_prompt(data)
    return await processar_resposta_agente(
        prompt,
        "Você é um especialista em normas internacionais de aviação civil."
    )

@app.post("/avaliar-viabilidade", response_model=RespostaAgente)
async def avaliar_viabilidade(data: VooData):
    prompt = viabilidade_agent.gerar_prompt(data)
    return await processar_resposta_agente(
        prompt,
        "Você é um advogado que avalia a força de casos jurídicos contra companhias aéreas."
    )

@app.post("/calcular-compensacao", response_model=RespostaAgente)
async def calcular_compensacao(data: VooData):
    prompt = compensacao_agent.gerar_prompt(data)
    return await processar_resposta_agente(
        prompt,
        "Você é um especialista em compensações por atrasos e cancelamentos de voo."
    )

@app.post("/gerar-plano-acao", response_model=RespostaAgente)
async def gerar_plano_acao(data: VooData):
    prompt = acao_agent.gerar_prompt(data)
    return await processar_resposta_agente(
        prompt,
        "Você é um advogado que orienta consumidores a buscar seus direitos."
    )

# Rota para análise completa
@app.post("/avaliar-caso-completo", response_model=Dict[str, RespostaAgente])
async def avaliar_caso_completo(data: VooData):
    try:
        resultados = {
            "resumo": await gerar_resumo(data),
            "regulacoes": await avaliar_regulacoes(data),
            "viabilidade": await avaliar_viabilidade(data),
            "compensacao": await calcular_compensacao(data),
            "plano_acao": await gerar_plano_acao(data)
        }
        return resultados
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar análise completa: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
