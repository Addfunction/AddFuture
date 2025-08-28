#!/usr/bin/env python3
"""
DNS Management Script for emdr.dev domain using Porkbun API

This script provides functionality to manage DNS records for the emdr.dev domain
using the Porkbun API. It includes functions to add subdomains with specified
record types and content.

Requirements:
- Set environment variables: PORKBUN_API_KEY and PORKBUN_SECRET_KEY
- Install required Python packages: requests

Usage:
    python manage_dns.py
"""

import os
import requests
import json
import sys
import argparse
from typing import Optional, Dict, Any


class PorkbunDNS:
    """Class to manage DNS records using Porkbun API."""
    
    def __init__(self):
        """Initialize the PorkbunDNS class with API credentials from environment variables."""
        self.api_key = os.getenv('PORKBUN_API_KEY')
        self.secret_key = os.getenv('PORKBUN_SECRET_KEY')
        self.base_url = 'https://porkbun.com/api/json/v3'
        
        if not self.api_key or not self.secret_key:
            raise ValueError(
                "Missing required environment variables. "
                "Please set PORKBUN_API_KEY and PORKBUN_SECRET_KEY."
            )
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a request to the Porkbun API.
        
        Args:
            endpoint (str): API endpoint
            data (dict): Request data
            
        Returns:
            dict: API response
            
        Raises:
            Exception: If the API request fails
        """
        # Add authentication to the request
        data.update({
            'apikey': self.api_key,
            'secretapikey': self.secret_key
        })
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
    
    def add_subdomain(self, domain: str, subdomain: str, record_type: str, content: str, ttl: int = 600) -> bool:
        """
        Add a subdomain DNS record.
        
        Args:
            domain (str): The main domain (e.g., 'emdr.dev')
            subdomain (str): The subdomain name (e.g., 'api', 'add_function')
            record_type (str): The DNS record type (e.g., 'A', 'CNAME', 'TXT')
            content (str): The value for the DNS record (e.g., IP address or target domain)
            ttl (int): Time to live in seconds (default: 600)
            
        Returns:
            bool: True if successful, False otherwise
        """
        endpoint = f"dns/create/{domain}"
        
        data = {
            'name': subdomain,
            'type': record_type.upper(),
            'content': content,
            'ttl': ttl
        }
        
        try:
            response = self._make_request(endpoint, data)
            
            if response.get('status') == 'SUCCESS':
                print(f"✅ Successfully added {subdomain}.{domain} ({record_type}) -> {content}")
                return True
            else:
                print(f"❌ Failed to add {subdomain}.{domain}: {response.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Error adding {subdomain}.{domain}: {e}")
            return False
    
    def list_records(self, domain: str) -> Optional[list]:
        """
        List all DNS records for a domain.
        
        Args:
            domain (str): The domain to list records for
            
        Returns:
            list: List of DNS records or None if failed
        """
        endpoint = f"dns/retrieve/{domain}"
        
        try:
            response = self._make_request(endpoint, {})
            
            if response.get('status') == 'SUCCESS':
                return response.get('records', [])
            else:
                print(f"❌ Failed to retrieve records: {response.get('message', 'Unknown error')}")
                return None
                
        except Exception as e:
            print(f"❌ Error retrieving records: {e}")
            return None
    
    def update_or_create_record(self, domain: str, subdomain: str, record_type: str, content: str, ttl: int = 600, force: bool = False) -> bool:
        """
        Update an existing DNS record or create a new one.
        
        Args:
            domain (str): The main domain (e.g., 'emdr.dev')
            subdomain (str): The subdomain name (e.g., 'api', 'addfuture')
            record_type (str): The DNS record type (e.g., 'A', 'CNAME', 'TXT')
            content (str): The value for the DNS record (e.g., IP address or target domain)
            ttl (int): Time to live in seconds (default: 600)
            force (bool): Force update even if record exists with same content
            
        Returns:
            bool: True if successful, False otherwise
        """
        full_name = f"{subdomain}.{domain}"
        
        # Check if record already exists
        existing_records = self.list_records(domain)
        if existing_records:
            for record in existing_records:
                if (record.get('name') == subdomain and 
                    record.get('type') == record_type.upper()):
                    
                    if record.get('content') == content and not force:
                        print(f"✅ Record {full_name} ({record_type}) -> {content} already exists and is up to date")
                        return True
                    
                    # Delete existing record before creating new one
                    print(f"🔄 Updating existing record {full_name}...")
                    if self.delete_record(domain, record.get('id')):
                        print(f"✅ Deleted old record for {full_name}")
                    else:
                        print(f"⚠️  Failed to delete old record for {full_name}, proceeding anyway...")
        
        # Create new record
        return self.add_subdomain(domain, subdomain, record_type, content, ttl)

    def list_records_filtered(self, domain: str, filter_name: Optional[str] = None) -> Optional[list]:
        """
        List DNS records for a domain with optional filtering.
        
        Args:
            domain (str): The domain to list records for
            filter_name (str): Optional filter to only show records containing this name
            
        Returns:
            list: List of DNS records or None if failed
        """
        records = self.list_records(domain)
        if not records:
            return records
            
        if filter_name:
            filtered_records = [
                record for record in records 
                if filter_name.lower() in record.get('name', '').lower()
            ]
            return filtered_records
            
        return records

    def delete_record(self, domain: str, record_id: str) -> bool:
        """
        Delete a DNS record by ID.
        
        Args:
            domain (str): The domain
            record_id (str): The record ID to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        endpoint = f"dns/delete/{domain}/{record_id}"
        
        try:
            response = self._make_request(endpoint, {})
            
            if response.get('status') == 'SUCCESS':
                print(f"✅ Successfully deleted record {record_id}")
                return True
            else:
                print(f"❌ Failed to delete record: {response.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Error deleting record: {e}")
            return False


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='DNS Management Script for emdr.dev domain using Porkbun API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add/update addfuture.emdr.dev CNAME record
  python manage_dns.py --subdomain addfuture --domain emdr.dev --type CNAME --content Addfunction.github.io
  
  # List all records for emdr.dev
  python manage_dns.py --list --domain emdr.dev
  
  # List filtered records
  python manage_dns.py --list --domain emdr.dev --filter addfuture
  
  # Run with example data (default behavior)
  python manage_dns.py
        """
    )
    
    parser.add_argument('--subdomain', 
                       help='Subdomain name to add/update (e.g., "addfuture")')
    parser.add_argument('--domain', 
                       help='Domain name (e.g., "emdr.dev")')
    parser.add_argument('--type', 
                       help='DNS record type (A, CNAME, TXT, etc.)')
    parser.add_argument('--content', 
                       help='DNS record content (IP address, target domain, etc.)')
    parser.add_argument('--ttl', type=int, default=600,
                       help='Time to live in seconds (default: 600)')
    parser.add_argument('--force', action='store_true',
                       help='Force update even if record exists with same content')
    parser.add_argument('--list', action='store_true',
                       help='List DNS records for the specified domain')
    parser.add_argument('--filter',
                       help='Filter records by name when listing')
    
    return parser.parse_args()


def main():
    """Main function with example usage."""
    args = parse_arguments()
    
    # Check for help argument (backward compatibility)
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print(__doc__)
        print("\nFor detailed setup instructions, see DNS_SETUP.md")
        return
    
    # Handle list mode argument validation before DNS manager initialization
    if args.list and not args.domain:
        print("❌ --domain is required when using --list")
        sys.exit(1)
    
    # Validate required arguments for record operations
    if any([args.subdomain, args.domain, args.type, args.content]):
        missing_args = []
        if not args.subdomain:
            missing_args.append("--subdomain")
        if not args.domain:
            missing_args.append("--domain")
        if not args.type:
            missing_args.append("--type")
        if not args.content:
            missing_args.append("--content")
            
        if missing_args:
            print(f"❌ Missing required arguments: {', '.join(missing_args)}")
            print("Use --help for usage information")
            sys.exit(1)
    
    try:
        # Initialize DNS manager
        dns_manager = PorkbunDNS()
        
        # Handle command line arguments
        if args.list:
            # List records mode
            print(f"📋 DNS records for {args.domain}:")
            records = dns_manager.list_records_filtered(args.domain, args.filter)
            if records:
                for record in records:
                    record_name = record.get('name', '')
                    if record_name:
                        full_name = f"{record_name}.{args.domain}"
                    else:
                        full_name = args.domain
                    print(f"  • {full_name} ({record.get('type', '')}) -> {record.get('content', '')}")
                print(f"\n✅ Found {len(records)} record(s)")
            else:
                print("  No records found or failed to retrieve records")
            return
            
        elif args.subdomain and args.domain and args.type and args.content:
            # Single record update mode
            print(f"🚀 DNS Management Script for {args.domain}")
            print("=" * 50)
            print(f"\n📍 Updating {args.subdomain}.{args.domain} subdomain...")
            
            success = dns_manager.update_or_create_record(
                domain=args.domain,
                subdomain=args.subdomain,
                record_type=args.type,
                content=args.content,
                ttl=args.ttl,
                force=args.force
            )
            
            if success:
                print(f"\n✅ Successfully configured {args.subdomain}.{args.domain}")
            else:
                print(f"\n❌ Failed to configure {args.subdomain}.{args.domain}")
                sys.exit(1)
            return
            
        # Default example mode (backward compatibility)
        print("🚀 DNS Management Script for emdr.dev")
        print("=" * 50)
        
        # Example: Add api.emdr.dev subdomain
        print("\n📍 Adding api.emdr.dev subdomain...")
        success1 = dns_manager.add_subdomain(
            domain="emdr.dev",
            subdomain="api", 
            record_type="A",
            content="192.168.1.100"  # Replace with actual IP address
        )
        
        # Example: Add add_function.emdr.dev subdomain
        print("\n📍 Adding add_function.emdr.dev subdomain...")
        success2 = dns_manager.add_subdomain(
            domain="emdr.dev",
            subdomain="add_function",
            record_type="A", 
            content="192.168.1.101"  # Replace with actual IP address
        )
        
        # List current records
        print("\n📋 Current DNS records for emdr.dev:")
        records = dns_manager.list_records("emdr.dev")
        if records:
            for record in records:
                print(f"  • {record.get('name', '')}.emdr.dev ({record.get('type', '')}) -> {record.get('content', '')}")
        
        # Summary
        print("\n" + "=" * 50)
        if success1 and success2:
            print("✅ All operations completed successfully!")
        else:
            print("⚠️  Some operations failed. Check the output above.")
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease ensure you have set the following environment variables:")
        print("  export PORKBUN_API_KEY='your_api_key_here'")
        print("  export PORKBUN_SECRET_KEY='your_secret_key_here'")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()