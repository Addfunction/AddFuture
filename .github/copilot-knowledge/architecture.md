# Architecture Overview

## Project Structure

The AddFuture/EMDR.dev repository is a modern web application built with Next.js 15 and React 19, serving as a development playground with integrated DNS management capabilities.

### Core Technologies

```
Frontend Stack:
├── Next.js 15 (App Router)
├── React 19 (Latest features)
├── TypeScript (Strict configuration)
├── Tailwind CSS (Custom design system)
└── Radix UI (Accessible component primitives)

Backend/API:
├── Next.js API Routes
├── Node.js runtime
└── Python DNS management scripts

Deployment:
├── GitHub Actions (CI/CD)
├── GitHub Pages (Static hosting)
└── Custom DNS via Porkbun API
```

### Directory Architecture

```
/
├── .github/                    # GitHub configuration
│   ├── workflows/             # CI/CD workflows
│   ├── copilot-instructions.md # Copilot guidelines
│   └── copilot-knowledge/     # Documentation for AI
│
├── app/                       # Next.js App Router
│   ├── api/                  # API routes
│   │   └── terminal/         # Terminal command API
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Homepage
│   └── globals.css           # Global styles
│
├── components/               # React components
│   └── ui/                  # Base UI components (Shadcn/ui)
│
├── lib/                     # Utilities and configurations
├── hooks/                   # Custom React hooks
├── styles/                  # Additional stylesheets
├── public/                  # Static assets
├── docs/                    # Project documentation
│
├── manage_dns.py           # DNS management script
├── requirements.txt        # Python dependencies
└── next.config.mjs        # Next.js configuration
```

## Design Patterns

### Component Architecture

**Base Components** (`/components/ui/`):
- Built on Radix UI primitives
- Styled with Tailwind CSS
- TypeScript interfaces for props
- Support for variants and sizes
- Consistent naming conventions

```typescript
// Example: Button component pattern
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "secondary" | "destructive"
  size?: "sm" | "md" | "lg"
}

export function Button({ variant = "default", size = "md", ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "base-styles",
        variants[variant],
        sizes[size],
        props.className
      )}
      {...props}
    />
  )
}
```

**Composition Pattern**:
- Components accept `children` and spread props
- Use `forwardRef` for components that need ref forwarding
- Leverage compound components for complex UI patterns

### State Management

**Local State Strategy**:
- React hooks for component state
- Context API for shared state across component trees
- No external state management library (Redux, Zustand) currently

**Data Fetching**:
- Server Components for static data
- Client Components with `use` hook for dynamic data
- API routes for server-side operations

### API Design

**REST Conventions**:
```typescript
// GET /api/resource - List resources
// POST /api/resource - Create resource
// GET /api/resource/[id] - Get specific resource
// PUT /api/resource/[id] - Update resource
// DELETE /api/resource/[id] - Delete resource
```

**Security Patterns**:
- Input validation with Zod schemas
- Command allowlisting for terminal API
- Environment variable protection
- Proper error handling and status codes

## Key Features

### 1. Terminal API (`/app/api/terminal/route.ts`)

Provides controlled command execution with security constraints:

```typescript
const allowedCommands = ["npm", "node", "git", "cat", "ls", "pwd", "whoami", "date"]
```

**Security Features**:
- Command allowlisting
- Timeout protection (30 seconds)
- Buffer size limits (1MB)
- Error handling for missing commands

### 2. DNS Management System

Python-based DNS management for the `emdr.dev` domain:

**Features**:
- Porkbun API integration
- GitHub Actions automation
- Environment variable security
- Automated CNAME record management for GitHub Pages

**Workflow Integration**:
- Triggers on main branch pushes
- Manual workflow dispatch
- Secure secret management

### 3. Static Site Generation

**Next.js Configuration**:
```javascript
const nextConfig = {
  eslint: { ignoreDuringBuilds: true },
  typescript: { ignoreBuildErrors: true },
  images: { unoptimized: true }
}
```

**Build Process**:
- Static export for GitHub Pages
- Asset optimization
- Build caching for faster deployments

## Development Workflow

### Local Development

```bash
# Setup
npm install --legacy-peer-deps
npm run dev

# Development server runs on http://localhost:3000
```

### Build and Deploy

```bash
# Local build test
npm run build

# Linting
npm run lint

# Production deployment via GitHub Actions
git push origin main
```

### DNS Management

```bash
# Python environment setup
pip install -r requirements.txt

# DNS operations
python manage_dns.py --subdomain [name] --domain emdr.dev --type [A|CNAME] --content [target]
```

## Configuration Management

### Environment Variables

**Development** (`.env.local`):
```bash
# Local development environment variables
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Production** (GitHub Secrets):
```bash
DNS_API_KEY=         # Porkbun API key
PORKBUN_SECRET_KEY=  # Porkbun secret key
```

### TypeScript Configuration

**Strict Settings**:
- `strict: true`
- `noUnusedLocals: true`
- `noUnusedParameters: true`
- Path aliases for clean imports

### Tailwind CSS Configuration

**Custom Design System**:
- CSS variables for theming
- Light/dark mode support
- Custom color palette
- Consistent spacing scale

## Performance Considerations

### Next.js Optimizations

- Static site generation where possible
- Image optimization disabled for GitHub Pages compatibility
- Build caching in CI/CD pipeline
- Component code splitting

### Bundle Size Management

- Tree shaking for unused code
- Dynamic imports for heavy components
- Modular architecture to avoid bloat

## Security Architecture

### Input Validation

- Zod schemas for API input validation
- TypeScript for compile-time type safety
- Sanitization of user inputs

### API Security

- Command allowlisting for terminal API
- Rate limiting considerations
- Proper error handling without information leakage
- Environment variable protection

### Deployment Security

- GitHub Actions with minimal permissions
- Secret management for API credentials
- No sensitive data in repository
- Secure DNS management practices

## Testing Strategy

### Component Testing

- React Testing Library for component behavior
- Jest for unit testing
- MSW for API mocking

### Integration Testing

- API route testing
- End-to-end workflows
- DNS management functionality

### Build Testing

- TypeScript compilation
- Linting validation
- Build process verification

This architecture supports rapid development while maintaining security, performance, and maintainability standards suitable for a development playground environment.