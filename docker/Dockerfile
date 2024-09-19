FROM python:3.11.9-alpine3.19

WORKDIR /app
COPY src/ . 
RUN chmod +x /app/entrypoint.sh

EXPOSE 10000
# add more here

CMD ["/bin/sh","-c","/app/entrypoint.sh"]
