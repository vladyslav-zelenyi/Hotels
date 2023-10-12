FROM mongo

COPY hotels.json /data/data.json
CMD mongoimport --db fornova_hotels --collection hotels --file data/data.json --jsonArray
