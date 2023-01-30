# NODE
FROM node:alpine
# create and set workdir
WORKDIR /app/backend
COPY ./widget/package.json ./widget/package.json
COPY ./widget/webpack.config.js ./widget/webpack.config.js
RUN npm install
ADD node /backend/static/
# PYTHON
FROM python:3.10.9-bullseye
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# create and set workdir
WORKDIR /app/backend
# copy local project
COPY . .
#update pip
# install requirements
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt
# make our server-entrypoint.sh executable
RUN chmod +x config/server-entrypoint.sh
EXPOSE 8000
# execute our server-entrypoint.sh file
ENTRYPOINT ["./config/server-entrypoint.sh"]