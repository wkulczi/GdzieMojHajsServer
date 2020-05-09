docker build -t gdziemojhajs-postgres:latest database/.
docker run -it -p 5432:5432 gdziemojhajs-postgres:latest
