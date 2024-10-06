# PYTHON SCRIPT VALIDATOR
This project is designed to validate Python scripts in a Dockerized environment. It can be used for various purposes, including:

## Add Questions
To add your Python questions or scripts, simply place them in the `src/` directory. Each challenge must include the following configurations:

- **flag**: The expected answer or validation key for the script.
- **title**: The name of the challange.
- **difficulty**: Set the challenge level (easy, medium, hard).
- **question**: A description of the task to be solved.
- **answer**: The expected solution for the task.
- **port**: The service port for the challenge. (adjust as needed).
- **challenge**: Identifier for the challenge, such as challenge number or unique ID.

## Database Configuration
The MySQL database stores all challenge data, including flags and user progress. **All sensitive information such as MySQL credentials (host, user, password, and database name) is now managed** via the `.env` file to enhance security and flexibility.

1. Copy the `.env.example` for your local version `.env`
2. `.env` File Example:
```sh
MYSQL_HOST=<hostname>
MYSQL_USER=<username>
MYSQL_PASSWORD=<password>
MYSQL_DATABASE=<dbname>
```

## Docker Configuration
Make sure the `docker-compose.yaml` file, `Dockerfile`, and `challenge.py` all have **proper port configurations** to avoid conflicts and ensure the services run on the correct ports.

1. **Docker Compose**: In `docker-compose.yaml`, configure the ports for the soal service to match your challenges:
```yaml
services:
  soal:
    ports:
      - "10000:10000"
      - "10500:10500"
    # Add more ports if needed

```

2. **Dockerfile**: In the `Dockerfile`, expose the ports for your challenges:
```yaml
EXPOSE 10000
EXPOSE 10500
# Add more ports as needed

```

3. **challenge.py**: Ensure the correct ports are being used for the challenges in `challenge.py` for each service that is running

## ENTRYPOINT SCRIPT (entrypoint.sh)
To add new challenges to the project, you can modify the entrypoint.sh script to run additional Python scripts:
```sh
python3 challenge1.py &
python3 challenge2.py &
# add more here

```
This script runs each challenge in the background (`&`) and keeps the container running by tailing a null file. Make sure to add any new challenge scripts to this file.

## Start the Container
To start the Docker container, use the following command:
```sh
sudo docker-compose up -d
```
This command will start the container in detached mode, running the validator in the background.

### NB
If table does not exist in the db, just wait :D

## PREVIEW 
![preview](img/preview.png)
