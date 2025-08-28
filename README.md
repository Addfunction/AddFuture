Gå til https://neon.tech og logg inn.
2. Opprett et nytt prosjekt og en database.
3. Kopier din `DATABASE_URL` fra Neon og lim den inn i .env-filen:


DATABASE_URL=postgresql://brukernavn:passord@neon-host-url/dbnavn?sslmode=require


Installer avhengigheter:

npm install


Generer Prisma-klienten:

npx prisma generate


Kjør migrering for å sette opp databasen:

npx prisma migrate dev --name init


Start utviklingsserveren:

npm run dev


✅ Du er nå koblet til Neon og klar til å utvikle!
