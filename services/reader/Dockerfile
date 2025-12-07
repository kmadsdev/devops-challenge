FROM golang:1.22-alpine
WORKDIR /app
COPY . .
RUN go mod init reader || true
RUN go mod tidy
RUN go build -o reader .
EXPOSE 8082
CMD ["./reader"]