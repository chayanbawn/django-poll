FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
RUN mkdir /static
WORKDIR /src
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000