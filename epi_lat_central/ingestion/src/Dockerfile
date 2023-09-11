FROM python:3.8-slim-buster

RUN apt-get update && \
    apt-get install -y gcc python3-dev wget \
    gconf-service libasound2 libatk1.0-0 libcairo2 \ 
    libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 \ 
    libnspr4 libpango-1.0-0 libxss1 fonts-liberation \ 
    libappindicator1 libnss3 xdg-utils

# Install Chrome
RUN wget http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_94.0.4606.71-1_amd64.deb
RUN dpkg -i google-chrome-stable_94.0.4606.71-1_amd64.deb; apt-get -fy install

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3"]
