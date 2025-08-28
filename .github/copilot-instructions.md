# GitHub Copilot Instructions for AddFuture/EMDR.dev

This repository contains a Next.js 15 application with React 19 for the EMDR.dev development playground. Follow these guidelines when contributing code or suggesting improvements.

## 🏗️ Architecture & Stack

- **Framework**: Next.js 15 with App Router
- **React**: Version 19 (latest features)
- **TypeScript**: Strict typing preferred
- **Styling**: Tailwind CSS with custom design system
- **UI Components**: Radix UI primitives with custom styling
- **State Management**: React hooks, no external state library
- **API Routes**: Next.js API routes in `/app/api/`
- **Deployment**: GitHub Pages with custom DNS management

## 📝 Code Style & Conventions

### TypeScript
- Use strict TypeScript configuration
- Prefer explicit types over `any`
- Use proper interface definitions for props and API responses
- Leverage React 19 type improvements

### Components
- Use functional components with hooks
- Follow the existing component structure in `/components/ui/`
- Prefer composition over inheritance
- Use proper TypeScript props interfaces

```typescript
interface ComponentProps {
  children: React.ReactNode
  className?: string
  variant?: "default" | "secondary"
}

export function Component({ children, className, variant = "default" }: ComponentProps) {
  return (
    <div className={cn("base-styles", variant === "secondary" && "secondary-styles", className)}>
      {children}
    </div>
  )
}
```

### Styling
- Use Tailwind CSS classes, not custom CSS unless absolutely necessary
- Follow the existing design system in `styles/globals.css`
- Use the `cn()` utility from `@/lib/utils` for conditional classes
- Prefer semantic color tokens (e.g., `text-foreground`, `bg-background`)
- Support both light and dark themes

### File Organization
```
app/                    # Next.js App Router pages and layouts
├── api/               # API routes
├── globals.css        # Global styles
└── layout.tsx         # Root layout

components/            # Reusable UI components
├── ui/               # Base UI components (Radix + styling)
└── [feature]/        # Feature-specific components

lib/                  # Utility functions and configurations
hooks/               # Custom React hooks
public/              # Static assets
```

## 🔐 Security Guidelines

### API Routes
- Validate all inputs using zod or similar validation
- Implement proper error handling
- Use allowlists for terminal commands (see `/app/api/terminal/route.ts`)
- Never expose sensitive environment variables
- Implement rate limiting for public endpoints

```typescript
// Example secure API route
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    // Validate input
    const schema = z.object({
      command: z.string().min(1).max(100)
    })
    
    const { command } = schema.parse(body)
    
    // Security check
    if (!allowedCommands.includes(command.split(' ')[0])) {
      return NextResponse.json({ error: 'Command not allowed' }, { status: 403 })
    }
    
    // Process request...
  } catch (error) {
    return NextResponse.json({ error: 'Invalid request' }, { status: 400 })
  }
}
```

### Environment Variables
- Never commit secrets to version control
- Use `.env.local` for development secrets
- Use GitHub Secrets for production environment variables
- Follow the pattern in `DNS_SETUP.md` for secure credential handling

## 🧪 Testing Philosophy

- Write tests for complex business logic
- Test API routes with various input scenarios
- Include error cases and edge conditions
- Use React Testing Library for component tests
- Mock external dependencies in tests

## 🚀 Development Workflow

### Getting Started
```bash
npm install --legacy-peer-deps
npm run dev
```

### Before Committing
```bash
npm run lint        # Check for linting errors
npm run build       # Ensure production build works
```

### API Development
- Follow REST conventions for API routes
- Use proper HTTP status codes
- Implement comprehensive error handling
- Document API endpoints with clear examples

### DNS Management
- Use the existing DNS management system in `manage_dns.py`
- Follow security practices outlined in `DNS_SETUP.md`
- Test DNS changes in development before applying to production

## 🎨 UI/UX Guidelines

### Design System
- Follow the existing color scheme and spacing
- Use consistent border radius (0.625rem)
- Implement proper hover and focus states
- Ensure accessibility with proper ARIA labels

### Component Patterns
```typescript
// Preferred component pattern
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "secondary" | "destructive"
  size?: "sm" | "md" | "lg"
}

export function Button({ 
  children, 
  className, 
  variant = "default", 
  size = "md",
  ...props 
}: ButtonProps) {
  return (
    <button
      className={cn(
        // Base styles
        "inline-flex items-center justify-center rounded-md font-medium transition-colors",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
        "disabled:pointer-events-none disabled:opacity-50",
        
        // Variants
        variant === "default" && "bg-primary text-primary-foreground hover:bg-primary/90",
        variant === "secondary" && "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        variant === "destructive" && "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        
        // Sizes
        size === "sm" && "h-9 px-3 text-xs",
        size === "md" && "h-10 px-4 py-2",
        size === "lg" && "h-11 px-8",
        
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}
```

### Responsive Design
- Mobile-first approach
- Use Tailwind responsive prefixes (`sm:`, `md:`, `lg:`, `xl:`)
- Test on various screen sizes
- Ensure touch-friendly interactions on mobile

## 🔧 Configuration Files

### Key Configuration
- `next.config.mjs`: Next.js configuration with image optimization disabled for static export
- `tailwind.config.js`: Tailwind configuration with custom design tokens
- `tsconfig.json`: TypeScript configuration with strict settings
- `components.json`: Shadcn/ui component configuration

### ESLint Rules
- Extend Next.js recommended rules
- Enable TypeScript-specific rules
- Enforce consistent code formatting
- Warn on unused variables and imports

## 🚨 Common Pitfalls to Avoid

1. **React 19 Compatibility**: Ensure all dependencies support React 19
2. **Build Errors**: Test production builds locally before pushing
3. **Type Safety**: Don't use `any` types; prefer proper TypeScript interfaces
4. **Security**: Validate all user inputs, especially in API routes
5. **Performance**: Optimize images and use Next.js optimization features
6. **Accessibility**: Include proper ARIA labels and keyboard navigation

## 📚 Additional Resources

- [Next.js 15 Documentation](https://nextjs.org/docs)
- [React 19 Features](https://react.dev/blog/2024/12/05/react-19)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Radix UI Documentation](https://www.radix-ui.com/docs)
- Repository-specific documentation in `/docs/` directory

## 🤝 Contributing

When suggesting code changes:
1. Follow the existing code patterns and conventions
2. Ensure TypeScript compatibility
3. Test changes locally before suggesting
4. Consider accessibility and responsive design
5. Update documentation if adding new features
6. Follow security best practices, especially for API routes

Remember: This repository serves as a development playground, so creative solutions and modern patterns are encouraged while maintaining code quality and security.