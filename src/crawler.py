import requests
import pathlib
from status import status


def download(url, file_path):
    try:
        response = requests.get(url, verify=False, allow_redirects=False)
        with open(file_path, "wb") as file:
            file.write(response.content)
        file.close()
    except Exception as excep:
        status.exit_from_error(status.Error(
            status.ConnectionError, f"Não foi possível fazer o download do arquivo: {file_path}. O seguinte erro foi gerado: {str(excep)}"))


def crawl(year, month, output_path):
    pathlib.Path(output_path).mkdir(exist_ok=True)

    files = []
    urls = {
        "contracheques": "https://www.mpm.mp.br/sistemas/consultaFolha/php/RelatorioRemuneracaoMensal.php?grupo=1&mes={}&ano={}".format(int(month), year),
        "indenizacoes": "https://www.mpm.mp.br/sistemas/consultaFolha/php/RelatorioRemuneracaoMensalVerbasIndenizatoriasGeral.php?grupo=7&mes={}&ano={}".format(int(month), year)
    }

    for key in urls:
        filename = "membros-ativos-{}-{}-{}.xlsx".format(key, month, year)
        file_path = f'{output_path}/{filename}'
        download(urls[key], file_path)
        files.append(file_path)

    return files
