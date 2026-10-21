# Imagem base leve (python:3.11-slim)
FROM python:3.11-slim

# Diretório de trabalho no container
WORKDIR /app

# Variáveis para logs em tempo real sem arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . /app/

# Comando de entrada principal: executa o pytest por padrão
CMD ["pytest", "-v"]