def gerar_prompt(data):
    return f'''
Você é um advogado especialista em direito do consumidor e transporte aéreo. 

Analise o caso abaixo e forneça APENAS a porcentagem de chance de sucesso do passageiro em obter a compensação, no seguinte formato:

Chance de sucesso: X%

Dados do Caso:
Relato: {data.relato}
Companhia: {data.cia}
Data do voo: {data.data_voo}
Origem: {data.origem}
Destino: {data.destino}
Oferecido: {", ".join(data.oferecido)}
Valor pretendido: R$ {data.valor or 'Não informado'}

IMPORTANTE: Retorne APENAS a porcentagem, sem nenhuma explicação ou texto adicional.
'''.strip()