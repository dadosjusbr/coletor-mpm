import os
from status import status
import pandas as pd


def _read(file):
    try:
        data = pd.read_excel(file, engine="openpyxl").to_numpy()
    except Exception as excep:
        status.exit_from_error(status.Error(
            status.SystemError, f"Erro lendo as planilhas: {excep}"))
    return data


def load(files, year, month, output_path):
    """Carrega os arquivos passados como parâmetros.

     :param files: slice contendo o arquivo baixado pelo coletor.
    O nome do arquivo deve seguir uma convenção e começar com 
    membros-ativos-contracheques
     :param year e month: usados para fazer a validação na planilha de controle de dados
     :return um objeto Data() pronto para operar com os arquivos
    """
    contracheques = _read([c for c in files if "contracheques" in c][0])
    indenizacoes = _read([i for i in files if "indenizacoes" in i][0])

    return Data(contracheques, indenizacoes, year, month, output_path)


class Data:
    def __init__(self, contracheques, indenizacoes, year, month, output_path):
        self.year = year
        self.month = month
        self.output_path = output_path
        self.contracheques = contracheques
        self.indenizacoes = indenizacoes

    def validate(self):
        """
         Validação inicial do arquivo passado como parâmetro.
        Aborta a execução do script caso não encontre o arquivo,
        retornando o codigo 4, esse codigo significa que não 
        existe dados para a data pedida.
        """

        if not (
            os.path.isfile(
                f"{self.output_path}/membros-ativos-contracheques-{self.month}-{self.year}.xlsx"
            )
        ) or not (
                os.path.isfile(
                    f"{self.output_path}/membros-ativos-indenizacoes-{self.month}-{self.year}.xlsx"
                )):
            status.exit_from_error(status.Error(
                status.DataUnavailable, f"Não existe planilhas para {self.month}/{self.year}."))
