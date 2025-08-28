# EMDR.dev - Development Playground

A modern Next.js website for personal development projects and experimentation, optimized for AI-assisted development with GitHub Copilot.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or pnpm
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Addfunction/AddFuture.git
cd AddFuture
```

2. Install dependencies:
```bash
npm install --legacy-peer-deps
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📜 Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run start` - Start the production server
- `npm run lint` - Run ESLint with enhanced configuration

## ✨ Features

- **Modern Stack**: Next.js 15 with React 19
- **Styling**: Tailwind CSS with custom design system
- **Components**: Radix UI primitives with custom styling
- **TypeScript**: Strict typing for better development experience
- **Responsive Design**: Mobile-first approach with dark/light theme support
- **DNS Management**: Automated DNS utilities for emdr.dev domain
- **Terminal API**: Secure command execution endpoint
- **GitHub Actions**: Automated deployment and DNS management

## 🤖 AI-Assisted Development

This repository is configured for optimal GitHub Copilot coding agent performance:

### Copilot Configuration

The repository includes comprehensive configuration for GitHub Copilot:

- **`.github/copilot-instructions.md`**: Detailed guidelines for AI assistance
- **`.github/copilot-knowledge/`**: Architecture and API documentation
- **Enhanced ESLint**: Code quality and consistency rules
- **TypeScript Configuration**: Strict typing for better AI suggestions
- **Structured Templates**: Issue and PR templates for better context

### Key Documentation for AI

- **Architecture Overview**: `.github/copilot-knowledge/architecture.md`
- **API Reference**: `.github/copilot-knowledge/api-reference.md`
- **Contributing Guidelines**: `CONTRIBUTING.md`
- **Code Style**: Defined in `.github/copilot-instructions.md`

### AI Development Guidelines

When working with Copilot on this project:

1. **Follow TypeScript patterns** for better AI suggestions
2. **Use existing component patterns** in `/components/ui/`
3. **Leverage the terminal API** for development automation
4. **Follow security guidelines** especially for API routes
5. **Maintain consistency** with the established architecture

## 🛠️ Development

### Code Quality

```bash
npm run lint          # ESLint with project-specific rules
npm run build         # Production build verification
```

### Architecture

```
├── app/                    # Next.js App Router
│   ├── api/               # API routes (secure terminal endpoint)
│   └── page.tsx           # Application pages
├── components/            # React components
│   └── ui/               # Reusable UI components (Radix + Tailwind)
├── .github/              # GitHub configuration
│   ├── copilot-instructions.md    # AI development guidelines
│   └── copilot-knowledge/         # AI knowledge base
└── lib/                  # Utilities and configurations
```

### Security Features

- **Terminal API**: Allowlisted commands with timeout protection
- **Input Validation**: Zod schemas for API routes
- **Environment Variables**: Secure credential management
- **Rate Limiting**: Prepared for production scaling

## 🌐 DNS Management

This project includes automated DNS management for the emdr.dev domain:

- **Python Scripts**: `manage_dns.py` for Porkbun API integration
- **GitHub Actions**: Automated DNS updates on deployment
- **Security**: Environment variables for API credentials

See `DNS_SETUP.md` for detailed setup instructions.

## 🤝 Contributing

We welcome contributions! This repository is designed for collaborative development with AI assistance.

1. **Read the guidelines**: Check `CONTRIBUTING.md` for detailed instructions
2. **Follow the patterns**: Use `.github/copilot-instructions.md` for code style
3. **Test your changes**: Ensure builds pass and linting is clean
4. **Submit a PR**: Use the provided template for clear communication

### For AI-Assisted Development

- The repository includes comprehensive context for AI tools
- Follow the established patterns for consistent AI suggestions
- Leverage the knowledge base for better AI understanding
- Use the terminal API for development automation

## 📚 Documentation

- **Getting Started**: This README
- **Architecture**: `.github/copilot-knowledge/architecture.md`
- **API Documentation**: `.github/copilot-knowledge/api-reference.md`
- **Contributing**: `CONTRIBUTING.md`
- **DNS Setup**: `DNS_SETUP.md`

## 🚀 Deployment

- **Automatic**: GitHub Actions deploys to GitHub Pages on main branch pushes
- **Manual**: Use workflow dispatch for manual deployments
- **DNS**: Automatic CNAME record management for `addfuture.emdr.dev`

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ for modern web development and AI-assisted coding**
