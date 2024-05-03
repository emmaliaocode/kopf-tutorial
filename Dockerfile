FROM python:3.10-alpine
COPY src /src
RUN pip install -r /src/requirements.txt
CMD kopf run /src/ephemeral.py --verbose
