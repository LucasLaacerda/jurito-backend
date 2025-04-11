def gerar_prompt(data):
    return f'''
Você é um especialista em ajudar passageiros a resolver problemas com companhias aéreas. 

Forneça um plano de ação SIMPLES e PRÁTICO, como se estivesse explicando para uma pessoa leiga. Evite termos jurídicos.

Responda no seguinte formato:

1. Primeiros passos:
   - [Lista 2-3 ações iniciais simples]

2. Documentos necessários:
   - [Lista apenas os documentos essenciais]

3. Como entrar em contato com a companhia:
   - [Instruções simples de contato]

4. Prazos importantes:
   - [Lista apenas os prazos mais relevantes]

Dados do Caso:
Relato: {data.relato}
Cidade onde abrirá o processo: {data.cidade_estado}
Companhia: {data.cia}
Data do voo: {data.data_voo}
Valor pretendido: R$ {data.valor or 'Não informado'}

IMPORTANTE: Use linguagem simples e direta. Seja prático e objetivo. Evite termos técnicos.
'''.strip()