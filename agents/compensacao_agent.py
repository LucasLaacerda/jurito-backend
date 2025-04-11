def gerar_prompt(data):
    return f'''
Você é um especialista em compensações por problemas em voos. Forneça APENAS os valores em reais (R$) que o passageiro pode receber, no seguinte formato:

Valor mínimo: R$ X
Valor médio: R$ Y
Valor máximo: R$ Z

Dados do Caso:
Relato: {data.relato}
Oferecido pela companhia: {", ".join(data.oferecido)}
Valor desejado pelo passageiro: R$ {data.valor or 'Não informado'}
Origem: {data.origem}
Destino: {data.destino}
Data do voo: {data.data_voo}

IMPORTANTE: Retorne APENAS os valores, sem nenhuma explicação ou texto adicional.
'''.strip()