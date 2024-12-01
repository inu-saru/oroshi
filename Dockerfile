FROM python:3.12.4-slim
WORKDIR /usr/src/app
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
COPY /app/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download ja_core_news_sm
COPY . .
CMD ["flask", "run"]