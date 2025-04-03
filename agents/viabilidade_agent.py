def gerar_prompt(data):
    return f'''
Você é um advogado especialista. Avalie a chance de sucesso do passageiro em obter compensação com base nos fatos abaixo. Dê uma nota de 0 a 100% e fundamente com base na jurisprudência brasileira ou internacional.

Relato: {data.relato}
Companhia: {data.cia}
Data do voo: {data.data_voo}
Origem: {data.origem}
Destino: {data.destino}
Oferecido: {", ".join(data.oferecido)}
'''.strip()