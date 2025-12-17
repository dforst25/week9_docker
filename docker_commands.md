# Docker Commands

Fill in the Docker commands you used to complete the test.

## Volume

### Create the volume

```bash
docker volume create fastapi-db
```

### Seed the volume (via Docker Desktop)

```bash
I import the db using GUI
```

## Server 1

### Build the image

```bash
docker build -t shopping-server1:v1 .\server1
```

### Run the container

```bash
docker run -p 8080:8080 --mount source=fastapi-db,target=/app/db shopping-serv
er1:v1
```

## Server 2

### Build the image

```bash
docker build -t shopping-server2:v1 .\server2
```

### Run the container

```bash
docker run -p 8081:8081 --mount source=fastapi-db,target=/app/db -v ${PWD}\server2\data:/app/data shopping-server2:v1
```

