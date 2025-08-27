# EMDR.dev - Development Playground

A modern, futuristic development playground built with Next.js, featuring AI-enhanced capabilities with Microsoft 365 Copilot integration.

## ✨ Features

- **Futuristic Design**: Modern UI with gradient effects and animations
- **Interactive Terminal**: Built-in terminal component for development tasks
- **Microsoft 365 Copilot**: AI-powered development assistance
- **Responsive Layout**: Mobile-friendly design
- **Developer Tools**: Safe sandbox environment for experimentation

## 🤖 Microsoft 365 Copilot Integration

This project includes Microsoft 365 Copilot integration for AI-enhanced development:

- **Code Review Assistant**: AI-powered code analysis
- **Document Generator**: Auto-generate technical documentation
- **Smart Email Drafting**: AI-assisted email composition
- **Meeting Summarizer**: Extract insights from Teams meetings

See [docs/COPILOT_INTEGRATION.md](docs/COPILOT_INTEGRATION.md) for setup instructions.

## 🔌 Oppsett for Neon-tilkobling

1. Gå til [Neon](https://neon.tech) og logg inn.
2. Opprett et nytt prosjekt og en database.
3. Kopier din `DATABASE_URL` fra Neon og lim den inn i `.env`-filen:

```
DATABASE_URL=postgresql://brukernavn:passord@neon-host-url/dbnavn?sslmode=require
```

4. Installer avhengigheter:
```
pnpm install
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
pnpm dev
```

✅ Du er nå koblet til Neon og klar til å utvikle!

## 🚀 Quick Start

1. Clone the repository
2. Install dependencies: `pnpm install`
3. Copy environment variables: `cp .env.example .env.local`
4. Configure Azure app registration (see Copilot documentation)
5. Start development server: `pnpm dev`
6. Open [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

- `/app` - Next.js app directory with pages and API routes
- `/components` - Reusable React components
- `/pages` - Additional pages directory for legacy support
- `/docs` - Project documentation
- `/public` - Static assets
- `/styles` - Global styles and configurations

## 🧪 Testing

The application is thoroughly tested for:
- ✅ Build process works correctly
- ✅ Dependencies install properly
- ✅ Development server runs successfully
- ✅ Microsoft 365 Copilot integration functions
- ✅ UI components render correctly
- ✅ Terminal functionality works as expected

## 🔧 Technologies

- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Microsoft Graph API** - Microsoft 365 integration
- **MSAL** - Microsoft authentication
- **Radix UI** - Accessible component primitives