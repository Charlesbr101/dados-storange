from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import random
import csv

class Unidade(Enum):
    COMPRIMIDOS = "comprimidos"
    CAIXA = "caixa"
    FRASCOS = "frascos"
    GRAMAS = "gramas"

class NomeUnidade(Enum):
    ALMOXARIFADO = "almoxarifado"
    FARMACIA_CENTRAL = "farmacia central"
    BLOCO_CIRURGICO = "bloco cirurgico"

@dataclass
class AtaRegistroPrecos:
    id: int
    id_medicamento: int
    especificacao: str
    nome_fornecedor: str
    cnpj: str
    unidade: Unidade
    quantidade_maxima: int
    quantidade_minima: int
    valor_unitario: float
    data_abertura: datetime
    prazo: datetime

@dataclass
class Empenho:
    id: int
    id_ata: int
    unidade: Unidade
    quantidade: int
    data_abertura: datetime
    prazo_entrega: datetime

@dataclass
class Medicamento:
    id_medicamento: int
    nome_medicamento: str
    descricao: str

@dataclass
class Lote:
    id: int
    tipo_medicamento: str
    prazo_validade: datetime

@dataclass
class Fluxo:
    id: int
    id_lote: int
    nome_unidade: NomeUnidade
    timestamp: datetime
    variacao: int

def gerar_cnpj():
    return f"{random.randint(10, 99)}.{random.randint(100, 999)}.{random.randint(100, 999)}/{random.randint(1000, 9999)}-{random.randint(10, 99)}"

def gerar_ata(id_: int, id_medicamento: int) -> AtaRegistroPrecos:
    return AtaRegistroPrecos(
        id=id_,
        id_medicamento=id_medicamento,
        especificacao="Medicamento genérico de alta qualidade",
        nome_fornecedor=f"Fornecedor {id_}",
        cnpj=gerar_cnpj(),
        unidade=random.choice(list(Unidade)),
        quantidade_maxima=random.randint(100, 500),
        quantidade_minima=random.randint(10, 50),
        valor_unitario=round(random.uniform(1.0, 100.0), 2),
        data_abertura=datetime.now() - timedelta(days=random.randint(1, 365)),
        prazo=datetime.now() + timedelta(days=random.randint(30, 365))
    )

def gerar_empenho(id_: int, ata: AtaRegistroPrecos) -> Empenho:
    return Empenho(
        id=id_,
        id_ata=ata.id,
        unidade=ata.unidade,
        quantidade=random.randint(ata.quantidade_minima, ata.quantidade_maxima),
        data_abertura=datetime.now(),
        prazo_entrega=datetime.now() + timedelta(days=random.randint(7, 60))
    )

def gerar_medicamento(id_: int) -> Medicamento:
    return Medicamento(
        id_medicamento=id_,
        nome_medicamento=f"Medicamento {id_}",
        descricao="Descrição do medicamento genérico."
    )

def gerar_lote(id_: int, tipo: str) -> Lote:
    return Lote(
        id=id_,
        tipo_medicamento=tipo,
        prazo_validade=datetime.now() + timedelta(days=random.randint(180, 730))
    )

def gerar_fluxo(id_: int, id_lote: int, inicio: datetime) -> Fluxo:
    return Fluxo(
        id=id_,
        id_lote=id_lote,
        nome_unidade=random.choice(list(NomeUnidade)),
        timestamp=inicio + timedelta(days=random.randint(0, 50)),
        variacao=random.randint(-50, 50)
    )

def escrever_csv(obj, filename):
    data = asdict(obj)
    for key, value in data.items():
        if isinstance(value, Enum):
            data[key] = value.value
        elif isinstance(value, datetime):
            data[key] = value.isoformat()
    
    file_exists = False
    try:
        with open(filename, "r") as f:
            file_exists = True
    except FileNotFoundError:
        pass
    
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def main():
    medicamentos = [gerar_medicamento(i) for i in range(1, 4)]
    atas = [gerar_ata(i, medicamentos[i - 1].id_medicamento) for i in range(1, 4)]
    empenhos = [gerar_empenho(i, ata) for ata in atas for i in range(ata.id * 2 - 1, ata.id * 2 + 1)]
    lotes = [gerar_lote(i, "Tipo X") for i in range(1, len(empenhos) + 1)]
    fluxos = [gerar_fluxo(i, lote.id, datetime.now() - timedelta(days=50)) for lote in lotes for i in range(lote.id * 100 - 99, lote.id * 100 + 1)]
    
    for m in medicamentos:
        escrever_csv(m, "medicamentos.csv")
    for a in atas:
        escrever_csv(a, "atas_registro_precos.csv")
    for e in empenhos:
        escrever_csv(e, "empenhos.csv")
    for l in lotes:
        escrever_csv(l, "lotes.csv")
    for f in fluxos:
        escrever_csv(f, "fluxos.csv")

if __name__ == "__main__":
    main()
