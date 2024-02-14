FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD streamlit run app.py --server.address=0.0.0.0