FROM python:3.11.9-alpine3.19

WORKDIR /app

COPY src/ . 

RUN pip install -r requirements.txt

RUN chmod +x /app/entrypoint.sh

EXPOSE 10000
EXPOSE 10500
# Add more ports as needed

CMD ["/bin/sh","-c","/app/entrypoint.sh"]
