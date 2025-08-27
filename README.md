

## [1m[34m🔌 Oppsett for Neon-tilkobling[0m

1. Gå til [Neon](https://neon.tech) og logg inn.
2. Opprett et nytt prosjekt og en database.
3. Kopier din `DATABASE_URL` fra Neon og lim den inn i `.env`-filen:

```
DATABASE_URL=postgresql://brukernavn:passord@neon-host-url/dbnavn?sslmode=require
```

4. Installer avhengigheter:
```
npm install
```

5. Generer Prisma-klienten:
```
npx prisma generate
```

6. Kjør migrering for å sette opp databasen:
```
npx prisma migrate dev --name init
```

7. Start utviklingsserveren:
```
npm run dev
```

✅ Du er nå koblet til Neon og klar til å utvikle!
