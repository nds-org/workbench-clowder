# workbench-clowder
An extractor that can fetch files from Clowder V2 and download them into Workbench V2 shared storage

This allows users to use Workbench tools to analyze or manipulate Clowder data

# Parameters
You can set the following parameters to adjust the behavior of this extractor:

* `RABBITMQ_URI` - Point this at the RabbitMQ instance that is used by Clowder
* `RABBITMQ_QUEUE` - Select a unique name for your extractor queue: e.g. `private.SOMETHING.ncsa.workbench.connector`

* `NDSLABS_HOME` - Select the target folder where downloaded resources should be stored

* `SECRET_KEY` - (optional) Override the API key that is used to download files from Clowder


# Running the Pre-Built Image
Modify the `.env` file to adjust the parameters being passed to the extractor


Docker Compose:
```bash
docker compose up -d
```

Docker:
```bash
docker run -it \
    -v $(pwd)/downloads:/home/worksman \
    --env-file .env \
    ndslabs/clowder-extractors-workbench
```


# Building the image
Docker Compose:
```bash
docker compose build
```

Docker:
```bash
docker build -t ndslabs/clowder-extractors-workbench .
```

# TODOs

* add default .env file for local testing
