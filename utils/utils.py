import re

def parse_percentage(text: str) -> int:
    """
    Extrai um inteiro X de uma string no formato "Chance de sucesso: X%".
    Se nada for encontrado, retorna 0.
    """
    m = re.search(r'(\d+)%', text)
    return int(m.group(1)) if m else 0

def parse_comp(text: str) -> tuple[float, float, float]:
    """
    Extrai três valores em reais de um texto no formato:
      Valor mínimo: R$ X
      Valor médio: R$ Y
      Valor máximo: R$ Z
    Retorna uma tupla (X, Y, Z) como floats.
    """
    # regex que pega os números depois de "R$ "
    nums = re.findall(r'R\$\s*([\d\.,]+)', text)
    # normaliza "1.234,56" → "1234.56" e converte para float
    def to_num(s):
        return float(s.replace('.', '').replace(',', '.'))
    if len(nums) >= 3:
        return to_num(nums[0]), to_num(nums[1]), to_num(nums[2])
    # fallback genérico
    return 0.0, 0.0, 0.0