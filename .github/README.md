# GitHub Actions Workflows

## update-dns.yml

Automated workflow to update DNS records for GitHub Pages hosting.

### Purpose

This workflow automatically creates/updates a CNAME record to point `addfuture.emdr.dev` to `Addfunction.github.io` (GitHub Pages hosting).

### Triggers

- **Manual**: Use the "Actions" tab and click "Run workflow"
- **Automatic**: Triggers on:
  - Pushes to `main` branch (when app/component files change)
  - New releases

### Required Secrets

Configure these in repository Settings → Secrets and variables → Actions:

- `DNS_API_KEY`: Your Porkbun API key
- `PORKBUN_SECRET_KEY`: Your Porkbun secret key

### Manual Trigger Options

- **Force Update**: Force update the DNS record even if it already exists with the correct value

### What it does

1. Checks out the repository
2. Sets up Python 3.12
3. Installs Python dependencies
4. Runs the DNS management script to create/update the CNAME record
5. Verifies the record was created successfully

### Example Output

```
🚀 DNS Management Script for emdr.dev
==================================================

📍 Updating addfuture.emdr.dev subdomain...
✅ Record addfuture.emdr.dev (CNAME) -> Addfunction.github.io already exists and is up to date

✅ Successfully configured addfuture.emdr.dev
```