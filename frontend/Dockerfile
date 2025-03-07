# Wähle ein Node.js-Image
FROM node:alpine

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere die Dateien ins Arbeitsverzeichnis
COPY . .

# Installiere die Abhängigkeiten
RUN npm install

# Installiere http-server global
RUN npm install -g http-server

# Exponiere den Port
EXPOSE 8080

# Starte den HTTP-Server
CMD ["http-server", "-p", "8080"]