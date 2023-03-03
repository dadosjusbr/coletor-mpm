import re
import number
from status import status
from coleta import coleta_pb2 as Coleta

from headers_keys import (HEADERS, INDENIZATORIAS, OBRIGATORIOS,
                          REMTEMP, REMUNERACAOBASICA, EVENTUALTEMP, OBRIGATORIOS)


def parse_employees(file, colect_key, month, year):
    employees = {}
    counter = 1
    for row in file:
        if "1  Remuneração" in str(row[0]):
            break
        if not number.is_nan(row[0]) and str(row[0]) != "Matrícula" and "MEMBROS ATIVOS" not in str(row[0]):
            member = Coleta.ContraCheque()
            member.id_contra_cheque = colect_key + "/" + str(counter)
            member.chave_coleta = colect_key
            member.matricula = str(row[0])
            member.nome = row[1]
            member.funcao = row[2]
            member.local_trabalho = row[3]
            member.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
            member.ativo = True
            member.remuneracoes.CopyFrom(
                create_remuneration(row, month, year)
            )

            employees[str(row[0])] = member
            counter += 1

    return employees


def remunerations(row):
    remuneration_array = Coleta.Remuneracoes()
    # VERBAS INDENIZATÓRIAS
    for key, value in HEADERS[INDENIZATORIAS].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = INDENIZATORIAS
        remuneration.item = key
        remuneration.valor = float(number.format_value(row[value]))
        remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(remuneration)
    # OUTRAS REMUNERAÇÕES TEMPORÁRIAS
    for key, value in HEADERS[REMTEMP].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = REMTEMP
        remuneration.item = key
        remuneration.valor = float(number.format_value(row[value]))
        remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")
        remuneration_array.remuneracao.append(remuneration)
    return remuneration_array


def create_remuneration(row, month, year):
    remuneration_array = Coleta.Remuneracoes()
    # REMUNERAÇÃO BÁSICA
    for key, value in HEADERS[REMUNERACAOBASICA].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = REMUNERACAOBASICA
        remuneration.item = key
        remuneration.valor = float(number.format_value(row[value]))
        remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
        remuneration_array.remuneracao.append(remuneration)
    # REMUNERAÇÃO EVENTUAL OU TEMPORÁRIA
    for key, value in HEADERS[EVENTUALTEMP].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneration.categoria = EVENTUALTEMP
        remuneration.item = key
        remuneration.valor = float(number.format_value(row[value]))
        remuneration.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
        remuneration_array.remuneracao.append(remuneration)
    # OBRIGATÓRIOS/LEGAIS
    for key, value in HEADERS[OBRIGATORIOS].items():
        remuneration = Coleta.Remuneracao()
        remuneration.natureza = Coleta.Remuneracao.Natureza.Value("D")
        remuneration.categoria = OBRIGATORIOS
        remuneration.item = key
        remuneration.valor = abs(
            float(number.format_value(row[value]))) * (-1)
        remuneration_array.remuneracao.append(remuneration)

    return remuneration_array


def update_employees(file_indenizacoes, employees):
    for row in file_indenizacoes:
        registration = str(row[0])
        if registration in employees.keys():
            emp = employees[registration]
            remu = remunerations(row)
            emp.remuneracoes.MergeFrom(remu)
            employees[registration] = emp
    return employees


def parse(data, colect_key):
    employees = {}
    payroll = Coleta.FolhaDePagamento()
    employees.update(parse_employees(
        data.contracheques, colect_key, data.month, data.year))

    if len(employees) == 0:
        status.exit_from_error(status.Error(
            status.DataUnavailable, "Sem dados"))

    update_employees(data.indenizacoes, employees)

    for i in employees.values():
        payroll.contra_cheque.append(i)

    return payroll
