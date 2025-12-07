FROM node:latest
WORKDIR /app
COPY package*.json ./
RUN npm install -g serve
RUN npm install
COPY . .
EXPOSE 5000
CMD ["serve", "-s", "."]