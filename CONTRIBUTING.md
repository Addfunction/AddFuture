# Contributing to AddFuture/EMDR.dev

Thank you for your interest in contributing to the EMDR.dev development playground! This document provides guidelines for contributing to ensure a smooth collaboration process.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Git
- Python 3.6+ (for DNS management)
- Basic familiarity with Next.js, React, and TypeScript

### Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Addfunction/AddFuture.git
   cd AddFuture
   ```

2. **Install dependencies**:
   ```bash
   npm install --legacy-peer-deps
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your development configuration
   ```

4. **Start development server**:
   ```bash
   npm run dev
   ```

5. **Verify setup**:
   - Open http://localhost:3000
   - Run `npm run build` to test production build
   - Run `npm run lint` to check code quality

## 📋 Development Workflow

### Branch Strategy

- `main`: Production-ready code, deployed to GitHub Pages
- `develop`: Integration branch for new features (if used)
- Feature branches: `feature/description` or `fix/description`

### Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow the code style guidelines
   - Write or update tests as needed
   - Update documentation if applicable

3. **Test your changes**:
   ```bash
   npm run lint          # Check code style
   npm run build         # Verify production build
   npm run dev           # Test in development
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create a pull request**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Convention

Use conventional commit format for clear history:

```
type(scope): description

Examples:
feat: add new terminal command support
fix: resolve build error in production
docs: update API documentation
style: format code according to ESLint rules
refactor: reorganize component structure
test: add tests for terminal API
chore: update dependencies
```

## 🎨 Code Style Guidelines

### TypeScript

- Use strict TypeScript configuration
- Prefer explicit types over `any`
- Use proper interface definitions
- Follow existing naming conventions

```typescript
// ✅ Good
interface UserProps {
  name: string
  email: string
  isActive?: boolean
}

function UserCard({ name, email, isActive = true }: UserProps) {
  return <div>...</div>
}

// ❌ Avoid
function UserCard(props: any) {
  return <div>...</div>
}
```

### React Components

- Use functional components with hooks
- Prefer composition over complex prop interfaces
- Use proper TypeScript prop types
- Follow the existing component patterns

```typescript
// ✅ Preferred pattern
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "secondary"
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
        "base-styles",
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
}
```

### Styling

- Use Tailwind CSS classes
- Follow the existing design system
- Use the `cn()` utility for conditional classes
- Support both light and dark themes

```typescript
// ✅ Good
<div className={cn(
  "flex items-center space-x-2",
  variant === "primary" && "bg-primary text-primary-foreground",
  className
)}>
  {children}
</div>

// ❌ Avoid custom CSS unless necessary
<div className="custom-component" style={{ backgroundColor: '#123456' }}>
  {children}
</div>
```

### API Routes

- Validate all inputs with Zod schemas
- Use proper HTTP status codes
- Implement comprehensive error handling
- Follow security best practices

```typescript
// ✅ Good API route pattern
export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const schema = z.object({
      name: z.string().min(1).max(100),
      email: z.string().email()
    })
    
    const { name, email } = schema.parse(body)
    
    // Process request...
    
    return NextResponse.json({ success: true, data: result })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: "Invalid input", details: error.errors },
        { status: 400 }
      )
    }
    
    console.error("API Error:", error)
    return NextResponse.json(
      { error: "Internal server error" },
      { status: 500 }
    )
  }
}
```

## 🧪 Testing Guidelines

### Component Testing

```typescript
import { render, screen } from '@testing-library/react'
import { Button } from './button'

describe('Button', () => {
  it('renders with correct variant', () => {
    render(<Button variant="secondary">Test</Button>)
    expect(screen.getByRole('button')).toHaveClass('bg-secondary')
  })
})
```

### API Testing

```typescript
import { POST } from './route'
import { NextRequest } from 'next/server'

describe('/api/terminal', () => {
  it('executes allowed commands', async () => {
    const request = new NextRequest('http://localhost:3000/api/terminal', {
      method: 'POST',
      body: JSON.stringify({ command: 'npm --version' })
    })
    
    const response = await POST(request)
    const data = await response.json()
    
    expect(response.status).toBe(200)
    expect(data.output).toBeDefined()
  })
  
  it('rejects forbidden commands', async () => {
    const request = new NextRequest('http://localhost:3000/api/terminal', {
      method: 'POST',
      body: JSON.stringify({ command: 'rm -rf /' })
    })
    
    const response = await POST(request)
    
    expect(response.status).toBe(403)
  })
})
```

## 🔐 Security Guidelines

### API Security

- Always validate inputs
- Use allowlists for commands/operations
- Implement proper error handling
- Never expose sensitive information in error messages

### Environment Variables

- Never commit secrets to version control
- Use `.env.local` for development
- Document required environment variables
- Use GitHub Secrets for production

### Dependencies

- Regularly audit dependencies: `npm audit`
- Keep dependencies updated
- Review new dependency additions carefully

## 📚 Documentation

### Code Documentation

- Use JSDoc comments for complex functions
- Document API endpoints with examples
- Keep README files updated
- Include inline comments for complex logic

### Component Documentation

```typescript
/**
 * A flexible button component with multiple variants and sizes.
 * 
 * @param variant - The visual style variant
 * @param size - The size of the button
 * @param children - The button content
 * @param className - Additional CSS classes
 */
export function Button({ variant = "default", size = "md", ...props }: ButtonProps) {
  // Implementation...
}
```

## 🚨 Issues and Bug Reports

When reporting issues:

1. **Use the issue template** (if available)
2. **Provide clear reproduction steps**
3. **Include environment information**:
   - Node.js version
   - npm version
   - Browser (for frontend issues)
   - Operating system

4. **Include relevant code snippets or screenshots**
5. **Check for existing issues first**

### Bug Report Example

```markdown
## Bug Description
The terminal API returns 500 error when executing valid npm commands.

## Steps to Reproduce
1. Navigate to the terminal interface
2. Enter "npm --version"
3. Click execute

## Expected Behavior
Should return the npm version number.

## Actual Behavior
Returns "Internal server error" with 500 status code.

## Environment
- Node.js: 18.17.0
- npm: 9.6.7
- Browser: Chrome 115.0.0.0
- OS: macOS 13.4
```

## 🏷️ Pull Request Guidelines

### Before Submitting

- [ ] Code follows the style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] Commit messages follow convention
- [ ] No console.log statements in production code
- [ ] Build passes without errors

### PR Description Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
[Include screenshots for UI changes]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or breaking changes documented)
```

## 🤝 Code Review Process

### For Reviewers

- Check code quality and style
- Verify tests and documentation
- Test functionality locally if needed
- Provide constructive feedback
- Approve when requirements are met

### For Contributors

- Respond to feedback promptly
- Make requested changes
- Update tests and documentation as needed
- Keep PRs focused and atomic

## 📞 Getting Help

- **Questions**: Open a discussion or issue
- **Documentation**: Check the `/docs` directory and `.github/copilot-knowledge/`
- **Code Examples**: Refer to existing components in `/components/ui/`
- **Architecture**: See `.github/copilot-knowledge/architecture.md`

## 🎯 Project Goals

This repository serves as a development playground focusing on:

- Modern web development practices
- AI-assisted development workflows
- Security-conscious coding
- Performance optimization
- Accessibility and inclusive design
- Clean, maintainable code

Your contributions help achieve these goals while creating a valuable resource for the development community.

Thank you for contributing! 🚀