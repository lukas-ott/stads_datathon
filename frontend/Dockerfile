# Wähle ein Node.js-Image
FROM node:alpine

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere die Dateien ins Arbeitsverzeichnis
COPY . .

# Installiere die Abhängigkeiten
RUN npm install

# Exponiere den Port
EXPOSE 8080

# Starte den HTTP-Server
CMD ["npm", "start"]
