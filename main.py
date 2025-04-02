# Jurito MVP - Backend (FastAPI + OpenAI + PyMuPDF)
# Versão inicial: rota /analisar que recebe contrato e responde sumário

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import openai
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

# CORS para frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_BASE = """
Você é um especialista jurídico. Leia o contrato abaixo e extraia as seguintes informações:
1. Quem são as partes envolvidas?
2. Quais as obrigações de cada parte?
3. Qual é o prazo e data de término?
4. Há multas ou penalidades? Quais?
5. Quais cláusulas exigem atenção?
6. Alerta se houver lacunas importantes ou termos incomuns.

Formato da resposta:
- Partes:
- Obrigações:
- Prazos:
- Multas:
- Cláusulas sensíveis:
- Alertas:
"""

@app.post("/analisar")
async def analisar_contrato(file: UploadFile = File(...)):
    conteudo = await file.read()
    with fitz.open(stream=conteudo, filetype="pdf") as doc:
        texto = "\n".join([page.get_text() for page in doc])

    prompt_final = PROMPT_BASE + "\n\n" + texto[:6000]  # corta para evitar limite de tokens

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um advogado especialista em contratos."},
            {"role": "user", "content": prompt_final}
        ]
    )

    resultado = response["choices"][0]["message"]["content"]
    return {"resumo": resultado}
