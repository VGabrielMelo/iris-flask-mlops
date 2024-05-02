# Captando uma máquina python para iniciar os serviços
FROM python:3.9-slim-buster

# Definindo o diretório raiz
WORKDIR /app

#Copiando os requirements e instalando as dependências para economizar processamento em caso de alteração do projeto.
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

#Realizando a cópia do projeto e do Dockerfile
COPY iris_flask /app/iris_flask
COPY Dockerfile /app/Dockerfile

# Colocando a URL do database que criei para ter o modelo treinado e os dados de treinamento
ENV SQLALCHEMY_DATABASE_URI='sqlite:////app/iris.db'

# Rodando o arquivo que vai treinar e carregar os dados e o arquivo do modelo no banco
RUN python3 /app/iris_flask/iris_model.py

# Iniciando a aplicação flask
CMD ["python", "iris_flask/app.py"]