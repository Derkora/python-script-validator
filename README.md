# PYTHON SCRIPT VALIDATOR
This project is designed to validate Python scripts in a Dockerized environment. It can be used for various purposes, including:
- CTF (Capture The Flag) Challenges: Automatically validate answers submitted by players for Python-based challenges.
- Code Review Automation: Validate code for syntax, logic, and structure before deployment.
- Python Learning Platform: Use it as a backend to check Python exercises for students.

## 1. Add your questions in the `src/` directory.
Place your Python scripts or questions in the `src/` folder. These scripts will be validated when the container is up.

## 2. Build the Docker Image
To create the Docker image, run the following command:
```.sh
sudo docker build -t <imagename>
```
Replace `<imagename>` with a name of your choice for the image.

## 3. Start the Container
To start the Docker container, use the following command:
```.sh
sudo docker-compose up -d
```
This will launch the container in detached mode.