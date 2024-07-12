# Use a imagem oficial do Python 3.12.4 como base
FROM python:3.12.4-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os arquivos requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação para o diretório de trabalho
COPY . .

# Defina a variável de ambiente para desativar buffers
ENV PYTHONUNBUFFERED=1

# Exponha a porta que a aplicação vai rodar
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]

