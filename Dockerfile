# Use uma imagem base com o Python
FROM python:3.11-slim

# Instale o Hashcat e outras dependências
RUN apt-get update && apt-get install -y \
    hashcat \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Crie um diretório para o log
RUN mkdir -p /hashcat/logs

# Copie o script Python para o container
COPY app.py /app/app.py

# Instale Flask
RUN pip install Flask

# Defina o diretório de trabalho
WORKDIR /app

# Exponha a porta em que o Flask será executado
EXPOSE 5000

# Comando para iniciar o servidor Flask
CMD ["python", "app.py"]
