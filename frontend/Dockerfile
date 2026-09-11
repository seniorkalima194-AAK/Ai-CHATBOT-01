FROM node:22-alpine AS build

WORKDIR /app

COPY chatbot01/package.json chatbot01/package-lock.json ./
RUN npm ci

COPY chatbot01 ./

# A relative URL makes the production frontend work from localhost or any LAN
# address without exposing an internal Docker service name to the browser.
ARG VITE_API_BASE_URL=/api/v1
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build

FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
