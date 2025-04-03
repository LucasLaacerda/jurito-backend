def gerar_prompt(data):
    return f'''
Você é um advogado especializado em direito do consumidor e transporte aéreo. Escreva um resumo claro, técnico e objetivo com base nas informações do passageiro abaixo, como se fosse apresentado em uma petição:

Relato: {data.relato}
Nome: {data.nome}
CPF: {data.cpf}
Companhia aérea: {data.cia}
Número do voo: {data.voo}
Origem: {data.origem}
Destino: {data.destino}
Data do voo: {data.data_voo}

Evite repetir dados óbvios e foque nos fatos relevantes com linguagem jurídica acessível.
'''.strip()