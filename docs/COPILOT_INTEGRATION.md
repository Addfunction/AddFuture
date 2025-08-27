# Microsoft 365 Copilot Integration

This document describes the Microsoft 365 Copilot integration added to the EMDR.dev project.

## Overview

The integration adds AI-powered development assistance using Microsoft 365 Copilot capabilities, enhancing the development workflow with intelligent suggestions and automation.

## Features

### 🤖 AI-Powered Assistance
- **Code Review Assistant**: AI-powered code analysis and suggestions
- **Document Generator**: Generate technical documentation from codebase
- **Smart Email Drafting**: Compose professional emails with AI assistance
- **Meeting Summarizer**: Automatically summarize Teams meetings and extract action items

### 🔐 Authentication
- Secure authentication using Microsoft Authentication Library (MSAL)
- Support for Azure Active Directory integration
- Scoped permissions for specific Microsoft 365 services

### 🎨 User Interface
- Integrated Copilot component in the main landing page
- Modern UI with loading states and connection status
- Responsive design matching the existing theme

## Setup Instructions

### 1. Azure App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to Azure Active Directory > App registrations
3. Click "New registration"
4. Fill in the application details:
   - **Name**: Your application name (e.g., "EMDR.dev Copilot Integration")
   - **Supported account types**: Accounts in any organizational directory and personal Microsoft accounts
   - **Redirect URI**: 
     - Type: Single-page application (SPA)
     - URI: `http://localhost:3000` (for development) or your production URL

5. After registration, copy the **Application (client) ID**

### 2. Configure Permissions

In your Azure app registration:

1. Go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Choose **Delegated permissions**
5. Add the following permissions:
   - `User.Read` - Read user profile
   - `Mail.Read` - Read user mail
   - `Files.Read` - Read user files

### 3. Environment Configuration

1. Copy `.env.example` to `.env.local`:
   ```bash
   cp .env.example .env.local
   ```

2. Update the environment variables:
   ```env
   NEXT_PUBLIC_AZURE_CLIENT_ID=your-application-client-id-here
   ```

### 4. Install Dependencies

The required dependencies are already included:
- `@azure/msal-browser` - Microsoft Authentication Library
- `@microsoft/microsoft-graph-client` - Microsoft Graph API client
- `isomorphic-fetch` - Fetch polyfill

## Usage

### Basic Authentication

1. Click the "Connect" button in the Copilot section
2. Sign in with your Microsoft 365 account
3. Grant the requested permissions
4. Access AI-powered features

### Available Actions

Once authenticated, users can:

1. **Analyze Code**: Get AI suggestions for code improvements
2. **Generate Documentation**: Create technical docs from codebase
3. **Draft Emails**: Compose professional emails with context
4. **Summarize Meetings**: Extract key points from Teams meetings

## Technical Implementation

### Components

- **`components/copilot-integration.tsx`**: Main Copilot component
- **`app/page.tsx`**: Updated to include Copilot section

### Key Features

- **MSAL Configuration**: Secure authentication setup
- **Error Handling**: Robust error handling for auth failures
- **Loading States**: User-friendly loading indicators
- **Responsive Design**: Mobile-friendly interface

### Security Considerations

- Client-side authentication only (no server-side secrets)
- Scoped permissions for minimal access
- Session-based token storage
- Proper error handling for failed authentications

## Development Notes

### Testing

The integration includes demo functionality when not authenticated:
- Mock suggestions are displayed
- Click handlers show demo alerts
- No actual API calls are made without proper authentication

### Production Deployment

For production deployment:

1. Update the redirect URI in Azure to your production URL
2. Set the `NEXT_PUBLIC_AZURE_CLIENT_ID` environment variable
3. Ensure HTTPS is enabled for security
4. Consider implementing additional error monitoring

### Future Enhancements

Potential improvements:
- Server-side token management for enhanced security
- Integration with additional Microsoft 365 services
- Custom Copilot actions based on project context
- Enhanced UI with more detailed AI suggestions

## Troubleshooting

### Common Issues

1. **Authentication Popup Blocked**: Ensure browser allows popups for your domain
2. **Invalid Client ID**: Verify the client ID in environment variables
3. **Permission Denied**: Check Azure app permissions configuration
4. **Network Errors**: Ensure internet connectivity and Azure service availability

### Debug Information

Enable debug logging by setting the MSAL log level to `Info` or `Verbose` in the component configuration.

## Support

For issues or questions:
- Check Azure Portal app registration settings
- Review browser console for error messages
- Verify environment variable configuration
- Ensure all required permissions are granted