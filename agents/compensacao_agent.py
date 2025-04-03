def gerar_prompt(data):
    return f'''
Baseado nos dados abaixo, estime o valor de compensação (em R$) que o passageiro pode pleitear. Fundamente com base na Resolução 400 da ANAC e outras normas aplicáveis.

Relato: {data.relato}
Oferecido pela companhia: {", ".join(data.oferecido)}
Valor desejado pelo passageiro: R$ {data.valor or 'Não informado'}
'''.strip()