FROM python:3.10.9-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/websocket

COPY . .
#update pip
# install requirements
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt
# make our server-entrypoint.sh executable
RUN chmod +x config/entrypoint.sh
EXPOSE 8088


# execute our server-entrypoint.sh file
ENTRYPOINT ["./config/entrypoint.sh"]
