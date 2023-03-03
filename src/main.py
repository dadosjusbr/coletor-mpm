import sys
import os

from dotenv import load_dotenv
from coleta import coleta_pb2 as Coleta, IDColeta
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf import text_format
from status import status

import crawler
import data
from parser import parse
import metadata

load_dotenv()

if "YEAR" in os.environ:
    year = os.environ["YEAR"]
else:
    status.exit_from_error(status.Error(
        status.InvalidInput, "Invalid arguments, missing parameter: 'YEAR'.\n"))

if "MONTH" in os.environ:
    month = os.environ["MONTH"]
    month = month.zfill(2)
else:
    status.exit_from_error(status.Error(
        status.InvalidInput, "Invalid arguments, missing parameter: 'MONTH'.\n"))

if "OUTPUT_FOLDER" in os.environ:
    output_path = os.environ["OUTPUT_FOLDER"]
else:
    output_path = "/output"

if "CRAWLER_VERSION" in os.environ:
    crawler_version = os.environ["CRAWLER_VERSION"]
else:
    crawler_version = "unspecified"


def parse_execution(data, file_names):
    # Cria objeto com dados da coleta.
    coleta = Coleta.Coleta()
    coleta.chave_coleta = IDColeta("mpm", month, year)
    coleta.orgao = "mpm"
    coleta.mes = int(month)
    coleta.ano = int(year)
    coleta.repositorio_coletor = "https://github.com/dadosjusbr/coletor-mpm"
    coleta.versao_coletor = crawler_version
    coleta.arquivos.extend(file_names)
    timestamp = Timestamp()
    timestamp.GetCurrentTime()
    coleta.timestamp_coleta.CopyFrom(timestamp)

    # Consolida folha de pagamento
    folha = Coleta.FolhaDePagamento()
    folha = parse(data, coleta.chave_coleta)

    # Monta resultado da coleta.
    rc = Coleta.ResultadoColeta()
    rc.folha.CopyFrom(folha)
    rc.coleta.CopyFrom(coleta)

    metadados = metadata.get()
    rc.metadados.CopyFrom(metadados)

    # Imprime a versão textual na saída padrão.
    print(text_format.MessageToString(rc), flush=True, end="")


# Main execution
def main():
    files = crawler.crawl(year, month, output_path)

    dados = data.load(files, year, month, output_path)
    dados.validate()  # Se não acontecer nada, é porque está tudo ok!

    parse_execution(dados, files)


if __name__ == "__main__":
    main()
