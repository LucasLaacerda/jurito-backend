def gerar_prompt(data):
    return f'''
Você é um especialista em ajudar passageiros a entender seus problemas com companhias aéreas.

Faça um resumo SIMPLES e CLARO do caso, como se estivesse explicando para uma pessoa leiga. Evite termos jurídicos.

Responda no seguinte formato:

1. O que aconteceu:
   - [Explique o problema de forma simples]

2. O que a companhia fez:
   - [Descreva a resposta da companhia]

3. O que você pode fazer:
   - [Lista 2-3 opções simples]

Dados do Caso:
Relato: {data.relato}
Nome: {data.nome}
CPF: {data.cpf}
Companhia aérea: {data.cia}
Número do voo: {data.voo}
Origem: {data.origem}
Destino: {data.destino}
Data do voo: {data.data_voo}
Oferecido: {", ".join(data.oferecido)}
Valor pretendido: R$ {data.valor or 'Não informado'}

IMPORTANTE: Use linguagem simples e direta. Seja breve e objetivo. Evite termos técnicos.
'''.strip()