# AddFuture - Personal Development Playground

My personal development playground where code meets creativity. Building cool stuff, experimenting with new tech, and having fun along the way.

## Next.js Setup

Gå til https://neon.tech og logg inn.
2. Opprett et nytt prosjekt og en database.
3. Kopier din `DATABASE_URL` fra Neon og lim den inn i .env-filen:

```
DATABASE_URL=postgresql://brukernavn:passord@neon-host-url/dbnavn?sslmode=require
```

Installer avhengigheter:

```bash
npm install
```

Generer Prisma-klienten:

```bash
npx prisma generate
```

Kjør migrering for å sette opp databasen:

```bash
npx prisma migrate dev --name init
```

Start utviklingsserveren:

```bash
npm run dev
```

✅ Du er nå koblet til Neon og klar til å utvikle!

## DNS Management Script

This repository also includes a Python script for managing DNS records for the domain `emdr.dev` using the Porkbun API.

### Features

- Add DNS subdomains (A, CNAME, AAAA, etc.)
- List existing DNS records
- Delete DNS records
- Secure API key management via environment variables
- Example usage for `api.emdr.dev` and `add_function.emdr.dev`

### Prerequisites

- Python 3.7 or higher
- Porkbun API credentials

### Setup Instructions

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Porkbun API credentials:**
   - Go to [Porkbun.com](https://porkbun.com/)
   - Log into your account
   - Navigate to Account > API Access
   - Generate API Key and Secret Key

3. **Create environment file:**
   Create a `.env` file in the project root with your API credentials:
   ```env
   PORKBUN_API_KEY=your_api_key_here
   PORKBUN_SECRET_KEY=your_secret_key_here
   ```

4. **Run the script:**
   ```bash
   python manage_dns.py
   ```

### Usage Examples

The script includes built-in examples for adding subdomains:

```python
from manage_dns import PorkbunDNSManager

# Initialize the DNS manager
dns_manager = PorkbunDNSManager()

# Add api.emdr.dev with A record
dns_manager.add_subdomain(
    domain='emdr.dev',
    subdomain='api',
    record_type='A',
    content='192.168.1.100'
)

# Add add_function.emdr.dev with CNAME record
dns_manager.add_subdomain(
    domain='emdr.dev',
    subdomain='add_function',
    record_type='CNAME',
    content='main.emdr.dev'
)
```

### Available Functions

- `add_subdomain(domain, subdomain, record_type, content, ttl=600)` - Add a new DNS record
- `list_records(domain)` - List all DNS records for a domain
- `delete_record(domain, record_id)` - Delete a specific DNS record

### Security Notes

- Never commit your `.env` file to version control
- The `.gitignore` file is configured to exclude `.env*` files
- API credentials are loaded securely using environment variables
- The script includes proper error handling and validation

### GitHub Actions Integration

This script is designed to work with GitHub Actions for automated DNS management. A workflow can be configured separately for on-demand execution.
