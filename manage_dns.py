#!/usr/bin/env python3
"""
DNS Management Script for Porkbun API

This script provides functionality to manage DNS records for the domain `emdr.dev`
using the Porkbun API. It includes functions to add subdomains and manage DNS records.

Requirements:
- PORKBUN_API_KEY: Your Porkbun API key
- PORKBUN_SECRET_KEY: Your Porkbun secret key

Usage:
    python manage_dns.py
"""

import os
import sys
import json
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class PorkbunDNSManager:
    """Class to manage DNS records using Porkbun API"""
    
    def __init__(self):
        """Initialize the DNS manager with API credentials"""
        self.api_key = os.getenv('PORKBUN_API_KEY')
        self.secret_key = os.getenv('PORKBUN_SECRET_KEY')
        self.base_url = 'https://porkbun.com/api/json/v3'
        
        if not self.api_key or not self.secret_key:
            raise ValueError(
                "Missing API credentials. Please set PORKBUN_API_KEY and PORKBUN_SECRET_KEY environment variables."
            )
    
    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a request to the Porkbun API
        
        Args:
            endpoint: API endpoint to call
            data: Data to send with the request
            
        Returns:
            Response from the API
            
        Raises:
            requests.RequestException: If the request fails
        """
        # Add API credentials to every request
        data.update({
            'apikey': self.api_key,
            'secretapikey': self.secret_key
        })
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error making request to {url}: {e}")
            raise
    
    def add_subdomain(self, domain: str, subdomain: str, record_type: str, content: str, ttl: int = 600) -> Dict[str, Any]:
        """
        Add a subdomain DNS record
        
        Args:
            domain: The main domain (e.g., 'emdr.dev')
            subdomain: The subdomain name (e.g., 'api', 'add_function')
            record_type: The DNS record type (e.g., 'A', 'CNAME', 'AAAA')
            content: The value for the DNS record (e.g., IP address or target domain)
            ttl: Time to live for the record in seconds (default: 600)
            
        Returns:
            Response from the Porkbun API
            
        Raises:
            ValueError: If parameters are invalid
            requests.RequestException: If the API request fails
        """
        if not domain or not subdomain or not record_type or not content:
            raise ValueError("All parameters (domain, subdomain, record_type, content) are required")
        
        # Validate record type
        valid_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SRV', 'TLSA', 'CAA']
        if record_type.upper() not in valid_types:
            raise ValueError(f"Invalid record type. Must be one of: {', '.join(valid_types)}")
        
        endpoint = f"dns/create/{domain}"
        data = {
            'name': subdomain,
            'type': record_type.upper(),
            'content': content,
            'ttl': str(ttl)
        }
        
        print(f"Adding {record_type} record for {subdomain}.{domain} -> {content}")
        
        try:
            response = self._make_request(endpoint, data)
            
            if response.get('status') == 'SUCCESS':
                print(f"✅ Successfully added {subdomain}.{domain}")
                return response
            else:
                error_msg = response.get('message', 'Unknown error')
                print(f"❌ Failed to add {subdomain}.{domain}: {error_msg}")
                return response
                
        except Exception as e:
            print(f"❌ Error adding {subdomain}.{domain}: {e}")
            raise
    
    def list_records(self, domain: str) -> Dict[str, Any]:
        """
        List all DNS records for a domain
        
        Args:
            domain: The domain to list records for
            
        Returns:
            Response containing all DNS records
        """
        endpoint = f"dns/retrieve/{domain}"
        data = {}
        
        try:
            response = self._make_request(endpoint, data)
            return response
        except Exception as e:
            print(f"❌ Error listing records for {domain}: {e}")
            raise
    
    def delete_record(self, domain: str, record_id: str) -> Dict[str, Any]:
        """
        Delete a DNS record by ID
        
        Args:
            domain: The domain the record belongs to
            record_id: The ID of the record to delete
            
        Returns:
            Response from the API
        """
        endpoint = f"dns/delete/{domain}/{record_id}"
        data = {}
        
        try:
            response = self._make_request(endpoint, data)
            
            if response.get('status') == 'SUCCESS':
                print(f"✅ Successfully deleted record {record_id}")
            else:
                error_msg = response.get('message', 'Unknown error')
                print(f"❌ Failed to delete record {record_id}: {error_msg}")
            
            return response
        except Exception as e:
            print(f"❌ Error deleting record {record_id}: {e}")
            raise


def main():
    """Main function with example usage"""
    print("🌐 Porkbun DNS Management Script")
    print("=" * 40)
    
    try:
        # Initialize DNS manager
        dns_manager = PorkbunDNSManager()
        
        # Example usage: Add api.emdr.dev subdomain
        print("\n📋 Example 1: Adding api.emdr.dev")
        try:
            result1 = dns_manager.add_subdomain(
                domain='emdr.dev',
                subdomain='api',
                record_type='A',
                content='192.168.1.100'  # Replace with your actual IP
            )
            print(f"Result: {result1}")
        except Exception as e:
            print(f"Error in example 1: {e}")
        
        # Example usage: Add add_function.emdr.dev subdomain
        print("\n📋 Example 2: Adding add_function.emdr.dev")
        try:
            result2 = dns_manager.add_subdomain(
                domain='emdr.dev',
                subdomain='add_function',
                record_type='CNAME',
                content='main.emdr.dev'  # Replace with your actual target
            )
            print(f"Result: {result2}")
        except Exception as e:
            print(f"Error in example 2: {e}")
        
        # Optional: List all records to verify
        print("\n📋 Current DNS records for emdr.dev:")
        try:
            records = dns_manager.list_records('emdr.dev')
            if records.get('status') == 'SUCCESS':
                for record in records.get('records', []):
                    print(f"  - {record.get('name', '')}.emdr.dev ({record.get('type', '')}) -> {record.get('content', '')}")
            else:
                print(f"Failed to retrieve records: {records.get('message', 'Unknown error')}")
        except Exception as e:
            print(f"Error listing records: {e}")
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n💡 Setup Instructions:")
        print("1. Create a .env file in this directory")
        print("2. Add your Porkbun API credentials:")
        print("   PORKBUN_API_KEY=your_api_key_here")
        print("   PORKBUN_SECRET_KEY=your_secret_key_here")
        print("3. Run the script again")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()