def gerar_prompt(data):
    return f'''
Com base nas informações abaixo, elabore um plano de ação simples e direto para o passageiro buscar seus direitos, incluindo prazos e etapas (ex: enviar carta formal, protocolar ação, etc).

Relato: {data.relato}
Cidade onde abrirá o processo: {data.cidade_estado}
'''.strip()