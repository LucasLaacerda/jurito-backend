def gerar_prompt(data):
    return f'''
Você é um especialista em direitos do passageiro aéreo. Explique de forma SIMPLES e DIRETA quais são os direitos do passageiro neste caso específico.

Use linguagem clara e acessível, como se estivesse explicando para uma pessoa leiga. Evite termos jurídicos complexos.

Responda no seguinte formato:

1. Direitos do passageiro:
   - [Lista os direitos principais de forma simples]

2. O que a companhia deve fazer:
   - [Lista as obrigações da companhia de forma simples]

3. Documentos necessários:
   - [Lista apenas os documentos essenciais]

Dados do Caso:
Relato: {data.relato}
Origem: {data.origem}
Destino: {data.destino}
Data do voo: {data.data_voo}
Companhia: {data.cia}
Oferecido: {", ".join(data.oferecido)}

IMPORTANTE: Use linguagem simples e direta, evitando termos técnicos. Seja breve e objetivo.
'''.strip()