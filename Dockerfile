FROM python:3.9-buster
WORKDIR /fxtok
COPY Pipfile Pipfile.lock ./
EXPOSE 5000
RUN pip install pipenv && pipenv install --dev --system --deploy
RUN python3 -m pip install -U yt-dlp

COPY . .

CMD [ "python3", "app.py" ]
