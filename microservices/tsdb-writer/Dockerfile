# getting maven
FROM maven:3.9-sapmachine-17 AS builder
WORKDIR /app

COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# getting jre
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# copy the jar
COPY --from=builder /app/target/*.jar app.jar

ENTRYPOINT ["sh", "-c", "java -jar app.jar"]