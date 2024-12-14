# Stage 1

FROM python:3.13.1-alpine3.21 AS builder

WORKDIR /app

COPY requirements.txt  /app

RUN pip3 install --no-cache-dir virtualenv && virtualenv venv

RUN /app/venv/bin/pip3 install --no-cache-dir -r /app/requirements.txt

COPY ./src src


# Stage 2

FROM python:3.13.1-alpine3.21 AS production

WORKDIR /app

RUN apk update && apk add curl 

COPY --from=builder /app/venv ./venv

COPY --from=builder /app/src ./src

ENV PATH="/app/venv/bin:$PATH"

EXPOSE 5000

CMD ["python", "src/main.py"]
