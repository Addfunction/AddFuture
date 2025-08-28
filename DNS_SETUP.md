# DNS Management for emdr.dev

This document provides detailed instructions for using the DNS management script with the Porkbun API.

## Quick Start

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API credentials:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual Porkbun API credentials
   ```

3. **Run the script:**
   ```bash
   python manage_dns.py
   ```

## API Credentials Setup

### Getting Porkbun API Credentials

1. Go to [Porkbun.com](https://porkbun.com/)
2. Log into your account
3. Navigate to **Account** → **API Access**
4. Click **Create API Key**
5. Copy both the **API Key** and **Secret Key**

### Configuration

Create a `.env` file in the project root:

```env
PORKBUN_API_KEY=pk1_1234567890abcdef1234567890abcdef
PORKBUN_SECRET_KEY=sk1_abcdef1234567890abcdef1234567890
```

## Script Usage

### Add Subdomains

The script includes examples for adding the required subdomains:

- `api.emdr.dev` - A record pointing to an IP address
- `add_function.emdr.dev` - CNAME record pointing to another domain

### Supported Record Types

- **A** - IPv4 address
- **AAAA** - IPv6 address  
- **CNAME** - Canonical name (alias)
- **MX** - Mail exchange
- **TXT** - Text record
- **NS** - Name server
- **SRV** - Service record
- **TLSA** - TLS authentication
- **CAA** - Certificate authority authorization

### Example Usage

```python
from manage_dns import PorkbunDNSManager

# Initialize
dns = PorkbunDNSManager()

# Add A record
dns.add_subdomain('emdr.dev', 'api', 'A', '203.0.113.1')

# Add CNAME record  
dns.add_subdomain('emdr.dev', 'add_function', 'CNAME', 'main.emdr.dev')

# List all records
records = dns.list_records('emdr.dev')

# Delete a record by ID
dns.delete_record('emdr.dev', 'record_id_here')
```

## Security Best Practices

- Never commit `.env` files to version control
- Use environment variables in production
- Rotate API keys regularly
- Limit API key permissions if possible

## Troubleshooting

### Common Issues

1. **Missing API credentials:**
   - Ensure `.env` file exists with correct credentials
   - Check that environment variables are set

2. **Invalid record type:**
   - Use only supported record types (A, AAAA, CNAME, etc.)

3. **API rate limits:**
   - Porkbun has rate limits; wait between requests if needed

4. **Domain permissions:**
   - Ensure your API key has permissions for the domain

### Error Messages

- `Missing API credentials` - Set up your `.env` file
- `Invalid record type` - Use a supported DNS record type
- `Command not found` - Install Python dependencies with `pip install -r requirements.txt`

## GitHub Actions Integration

This script is designed to work with GitHub Actions. You can set up workflows to:

- Automatically update DNS records on deployment
- Manage staging/production domain switching
- Bulk DNS record management

Example workflow configuration would use repository secrets for API credentials.

## Support

For issues with:
- **The script:** Check the troubleshooting section above
- **Porkbun API:** Visit [Porkbun API Documentation](https://porkbun.com/api/json/v3/documentation)
- **Domain configuration:** Contact Porkbun support