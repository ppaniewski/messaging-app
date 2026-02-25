FROM node:22.19.0-slim as builder

WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .
RUN npm run build


FROM nginx:1.29.5 as runner

RUN rm -rf /etc/nginx/conf.d/*
COPY frontend.conf /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/

RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /app/dist/ /usr/share/nginx/html/

EXPOSE 80