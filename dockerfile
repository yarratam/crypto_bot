FROM python:3

WORKDIR /home/pi/crypto_bot

COPY requirements.txt ./
RUN sudo pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]