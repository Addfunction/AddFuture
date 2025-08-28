# DNS Management for emdr.dev

This directory contains a Python script to manage DNS records for the domain `emdr.dev` using the Porkbun API.

## Files

- `manage_dns.py` - Main DNS management script
- `requirements.txt` - Python dependencies
- `DNS_SETUP.md` - Setup and usage instructions (this file)

## Prerequisites

1. **Python 3.6+** installed on your system
2. **Porkbun API credentials** for the `emdr.dev` domain
3. **Internet connection** for API requests

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

You need to set up your Porkbun API credentials as environment variables. You can do this in several ways:

#### Option A: Export directly in terminal
```bash
export PORKBUN_API_KEY="your_api_key_here"
export PORKBUN_SECRET_KEY="your_secret_key_here"
```

#### Option B: Create a .env file (recommended for development)
Create a `.env` file in the same directory as the script:

```bash
# .env file
PORKBUN_API_KEY=your_api_key_here
PORKBUN_SECRET_KEY=your_secret_key_here
```

Then load it before running the script:
```bash
set -a && source .env && set +a
```

#### Option C: Set in your shell profile
Add the export commands to your `~/.bashrc`, `~/.zshrc`, or equivalent:

```bash
echo 'export PORKBUN_API_KEY="your_api_key_here"' >> ~/.bashrc
echo 'export PORKBUN_SECRET_KEY="your_secret_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Obtain Porkbun API Credentials

1. Log in to your [Porkbun account](https://porkbun.com/)
2. Go to the API section in your account dashboard
3. Generate API credentials for your domain
4. Copy the API Key and Secret Key

## Usage

### Basic Usage

Run the script with the example subdomains:

```bash
python manage_dns.py
```

This will:
- Add `api.emdr.dev` subdomain (A record pointing to 192.168.1.100)
- Add `add_function.emdr.dev` subdomain (A record pointing to 192.168.1.101)
- List all current DNS records for the domain

### Custom Usage

You can modify the script or use it as a module to add your own subdomains:

```python
from manage_dns import PorkbunDNS

# Initialize DNS manager
dns = PorkbunDNS()

# Add a subdomain
dns.add_subdomain(
    domain="emdr.dev",
    subdomain="my-app",
    record_type="A",
    content="192.168.1.200"
)

# Add a CNAME record
dns.add_subdomain(
    domain="emdr.dev", 
    subdomain="www",
    record_type="CNAME",
    content="emdr.dev"
)
```

## Supported Record Types

The script supports common DNS record types:
- **A** - IPv4 address
- **AAAA** - IPv6 address  
- **CNAME** - Canonical name (alias)
- **TXT** - Text record
- **MX** - Mail exchange
- **NS** - Name server

## Example Output

```
🚀 DNS Management Script for emdr.dev
==================================================

📍 Adding api.emdr.dev subdomain...
✅ Successfully added api.emdr.dev (A) -> 192.168.1.100

📍 Adding add_function.emdr.dev subdomain...
✅ Successfully added add_function.emdr.dev (A) -> 192.168.1.101

📋 Current DNS records for emdr.dev:
  • api.emdr.dev (A) -> 192.168.1.100
  • add_function.emdr.dev (A) -> 192.168.1.101
  • emdr.dev (A) -> 192.168.1.1
  • www.emdr.dev (CNAME) -> emdr.dev

==================================================
✅ All operations completed successfully!
```

## Security Notes

- **Never commit API credentials** to version control
- The `.env` file is already excluded in `.gitignore`
- Use environment variables or secure secret management in production
- Rotate API keys regularly
- Limit API key permissions to only DNS management

## Troubleshooting

### Common Issues

1. **Missing environment variables**
   ```
   ❌ Configuration error: Missing required environment variables.
   ```
   **Solution**: Make sure `PORKBUN_API_KEY` and `PORKBUN_SECRET_KEY` are set

2. **API authentication failed**
   ```
   ❌ API request failed: 401 Unauthorized
   ```
   **Solution**: Verify your API credentials are correct

3. **Domain not found**
   ```
   ❌ Failed to add subdomain: Domain not found
   ```
   **Solution**: Ensure the domain is managed by your Porkbun account

4. **Network connectivity issues**
   ```
   ❌ API request failed: Connection timeout
   ```
   **Solution**: Check your internet connection and firewall settings

### Getting Help

- Check the [Porkbun API documentation](https://porkbun.com/api/json/v3/documentation)
- Verify your domain is properly configured in Porkbun
- Test API credentials with a simple API call

## GitHub Actions Integration

This script can be easily integrated into GitHub Actions workflows for automated DNS management. Example workflow:

```yaml
name: Update DNS
on:
  workflow_dispatch:
    inputs:
      subdomain:
        description: 'Subdomain to add'
        required: true
      ip_address:
        description: 'IP address to point to'
        required: true

jobs:
  update-dns:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python manage_dns.py
        env:
          PORKBUN_API_KEY: ${{ secrets.PORKBUN_API_KEY }}
          PORKBUN_SECRET_KEY: ${{ secrets.PORKBUN_SECRET_KEY }}
```