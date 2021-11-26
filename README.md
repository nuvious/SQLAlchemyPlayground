# SQLAlchemy Playground

Just an exploration of the SQLAlchemy API using docker containers to represent
various flavors of SQL available as docker images.

## Prerequisites

- docker
- docker-compose

## Running

Simply bring up the docker compose.

```bash
docker compose up
```

This will build and launch the demo. Every PMLB dataset will be downloaded and 
written to a database with each dataset having its own table. Then the schemas
are crawled and dumped to json for validation the data was written.