###########################################
# BASE IMAGE
###########################################

FROM python:3.11-slim AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .


###########################################
# MULTI-STAGE & DISTROLESS BUILD
###########################################
FROM gcr.io/distroless/python3-debian11
WORKDIR /app
COPY --from=base /app /app
CMD [ "python", "app.py" ]