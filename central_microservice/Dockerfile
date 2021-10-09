FROM python:3.9
ADD . /app
WORKDIR /app

ENV PYTHONUNBUFFERED=1
RUN python3 -m venv /app/venv
RUN . /app/venv/bin/activate && python3 -m pip install -r requirements.txt

RUN chmod +x /app/entrypoint.sh

RUN export PYTHONPATH="$PYTHONPATH:/app"
ENTRYPOINT ["/app/entrypoint_microservice.sh"]
