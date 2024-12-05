FROM python:3.12.4-slim
WORKDIR /workspace
ENV FLASK_APP=app
COPY requirements.txt /workspace
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download ja_core_news_sm

COPY . .
CMD ["gunicorn", "--reload", "-w", "1" ,"--bind", "0.0.0.0:3030", "--chdir", "/workspace/app", "wsgi:oroshi_api"]