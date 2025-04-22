FROM golang:1.24 AS builder
RUN apt-get update && apt-get install -y librdkafka-dev

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . ./
RUN CGO_ENABLED=1 GOOS=linux go build -o main ./cmd/app

# Use debian instead of alpine
FROM debian:stable-slim

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    librdkafka-dev \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root/
COPY --from=builder /app/main .

EXPOSE 8080
CMD ["./main"]