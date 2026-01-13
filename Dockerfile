FROM public.ecr.aws/docker/library/python:3.12-slim

WORKDIR /app

# Evita buffer de stdout (logs no CloudWatch)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código
COPY . .

# Porta padrão usada pelo AgentCore
EXPOSE 8080

# Entry point do runtime
CMD ["python", "runtime_market_agent.py"]
