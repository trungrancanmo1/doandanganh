FROM maven:3.9-sapmachine-17 AS builder
WORKDIR /app

COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# JRE to run the package
FROM openjdk:17-alpine

RUN apk add --no-cache libstdc++

COPY --from=builder /app/target/*.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]
