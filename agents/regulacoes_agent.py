def gerar_prompt(data):
    return f'''
Com base no relato a seguir e nas informações da viagem, indique quais regulações se aplicam ao caso (ex: ANAC, EU261, Convenção de Montreal). Fundamente com base na origem, destino e natureza do problema.

Relato: {data.relato}
Origem: {data.origem}
Destino: {data.destino}
Data do voo: {data.data_voo}
'''.strip()