# ChatBot-Clothes


rasa run --enable-api --cors "*"

## Rasa validate Data
rasa data validate

## Rasa Action Server
rasa run actions 

## Run Duckling Server
docker run -p 8000:8000 rasa/duckling