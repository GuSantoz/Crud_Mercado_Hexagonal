FROM python:3.9-slim

WORKDIR /app

# Instala dependências do sistema necessárias para drivers de banco
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]