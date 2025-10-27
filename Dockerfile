###########################################
# BASE IMAGE
###########################################
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .


###########################################
# MULTI-STAGE & DISTROLESS BUILD
###########################################
FROM gcr.io/distroless/python3-debian12
WORKDIR /app
COPY --from=builder /app /app
ENV PYTHONPATH=/app
CMD ["python", "app.py"]