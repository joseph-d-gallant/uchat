FROM python:3.10-alpine
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
COPY . .
CMD ["python", "-u", "app.py"]