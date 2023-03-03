# Ministério Público Militar (MPM)
Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público Militar. O site com as informações pode ser acessado [aqui](https://transparencia.mpm.mp.br/contracheque/).

O crawler está estruturado como uma CLI. Você passa dois argumentos (mês e ano) e serão baixadas duas planilhas no formato XLSX, cada planilha é referente a uma destas categorias: 

- Tipo I - Folha de remunerações: Membros Ativos. 
- Tipo II - Verbas Indenizatórias e outras remunerações temporárias.

## Como usar

### Executando com Docker

- Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

- Construção da imagem:

    ```sh
    $ cd coletor-mpm
    $ docker build --pull --rm -t mpm:latest .
    ```
- Execução:

    ```sh
    $ docker run -i --rm -e YEAR=2019 -e MONTH=12 -e OUTPUT_FOLDER=/output --name mpm --mount type=bind,src=/home/user/coletor-mpm,dst=/output mpm
    ```

### Executando sem uso do docker:

- Para executar o script é necessário rodar o seguinte comando, a partir do diretório coletor-mpba, adicionando às variáveis seus respectivos valores, a depender da consulta desejada. É válido lembrar que faz-se necessario ter o [Python 3.6.9](https://www.python.org/downloads/) instalado.
 
    ```sh
        YEAR=2020 MONTH=01 python3 src/main.py
    ```
- Para que a execução do script possa ser corretamente executada é necessário que todos os requirements sejam devidamente instalados. Para isso, executar o [PIP](https://pip.pypa.io/en/stable/installing/) passando o arquivo requiments.txt, por meio do seguinte comando:
   
    ```sh
        pip install -r requirements.txt
    ```
