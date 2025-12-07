FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install redis
EXPOSE 8083
CMD ["python", "main.py"]