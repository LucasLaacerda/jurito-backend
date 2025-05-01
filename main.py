from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import VooData, RespostaAgente
from utils.utils import parse_comp, parse_percentage
from openai import OpenAI
import os
import json
import asyncio

# Imports dos agents
from agents import (
    resumo_agent,
    regulacoes_agent,
    viabilidade_agent,
    compensacao_agent,
    acao_agent,
    peticao_agent
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
@app.post("/avaliar-caso-completo")
async def avaliar_caso_completo(data: VooData) -> dict:
    try:  
        # Executa em paralelo
        resumo, regulacoes, viab, comp, plano = await asyncio.gather(
            resumo_agent.run(data),
            regulacoes_agent.run(data),
            viabilidade_agent.run(data),
            compensacao_agent.run(data),
            acao_agent.run(data),
        )
        # Extrai valores de compensacao
        min_c, med_c, max_c = map(parse_comp, comp)
        # Gera petição
        peticao = await peticao_agent.run(
            data,
            resumo,
            regulacoes,
            int(parse_percentage(viab)),
            min_c,
            med_c,
            max_c
        )
        return {
            "resumo":        {"resposta": resumo},
            "regulacoes":    {"resposta": regulacoes},
            "viabilidade":   {"resposta": viab},
            "compensacao":   {"resposta": comp},
            "plano_acao":    {"resposta": plano},
            "peticao":       {"resposta": peticao}
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar análise completa: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
