FROM python:3-alpine

# gcc needed for slackclient
RUN apk add --no-cache build-base libffi-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /usr/src/app

CMD ["python", "manage.py", "listener"]
