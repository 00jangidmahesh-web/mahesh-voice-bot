FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# HF Spaces routes traffic to this port for Docker SDK spaces
EXPOSE 7860

# main.py uses plain sibling imports (from agent import ...), so run with
# app/ as the working root rather than treating it as a package.
CMD ["uvicorn", "main:app", "--app-dir", "app", "--host", "0.0.0.0", "--port", "7860"]
