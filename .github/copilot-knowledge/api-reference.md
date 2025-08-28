# API Reference

## Terminal API

### POST /api/terminal

Execute allowed terminal commands with security constraints.

**Endpoint**: `/api/terminal`
**Method**: `POST`
**Content-Type**: `application/json`

#### Request Body

```typescript
interface TerminalRequest {
  command: string
}
```

#### Response

```typescript
interface TerminalResponse {
  output?: string
  error?: string
}
```

#### Allowed Commands

```typescript
const allowedCommands = [
  "npm",     // Node package manager
  "node",    // Node.js runtime
  "git",     // Git version control
  "cat",     // File content display
  "ls",      // Directory listing
  "pwd",     // Print working directory
  "whoami",  // Current user
  "date"     // Current date/time
]
```

#### Security Features

- **Command Allowlisting**: Only predefined commands are allowed
- **Timeout Protection**: 30-second execution limit
- **Buffer Limit**: 1MB maximum output buffer
- **Error Handling**: Proper error responses for security

#### Examples

**Successful Command**:
```bash
# Request
curl -X POST /api/terminal \
  -H "Content-Type: application/json" \
  -d '{"command": "npm --version"}'

# Response
{
  "output": "10.2.4"
}
```

**Forbidden Command**:
```bash
# Request
curl -X POST /api/terminal \
  -H "Content-Type: application/json" \
  -d '{"command": "rm -rf /"}'

# Response (403)
{
  "error": "Command 'rm' is not allowed for security reasons."
}
```

**Command Not Found**:
```bash
# Request
curl -X POST /api/terminal \
  -H "Content-Type: application/json" \
  -d '{"command": "nonexistent-command"}'

# Response (400)
{
  "error": "Command not found. Make sure the required tools are installed."
}
```

**Timeout Error**:
```bash
# Response (400)
{
  "error": "Command timed out after 30 seconds."
}
```

#### Implementation Details

```typescript
import { type NextRequest, NextResponse } from "next/server"
import { exec } from "child_process"
import { promisify } from "util"

const execAsync = promisify(exec)

export async function POST(request: NextRequest) {
  try {
    const { command } = await request.json()

    // Validation
    if (!command || typeof command !== "string") {
      return NextResponse.json({ error: "Invalid command" }, { status: 400 })
    }

    // Security check
    const allowedCommands = ["npm", "node", "git", "cat", "ls", "pwd", "whoami", "date"]
    const commandParts = command.trim().split(" ")
    const baseCommand = commandParts[0]

    if (!allowedCommands.includes(baseCommand)) {
      return NextResponse.json(
        { error: `Command '${baseCommand}' is not allowed for security reasons.` },
        { status: 403 }
      )
    }

    // Execute with constraints
    const { stdout, stderr } = await execAsync(command, {
      timeout: 30000,     // 30 second timeout
      maxBuffer: 1024 * 1024  // 1MB buffer
    })

    const output = stdout || stderr || "Command completed successfully"
    return NextResponse.json({ output })

  } catch (error: any) {
    console.error("Terminal command error:", error)

    if (error.code === "ENOENT") {
      return NextResponse.json({
        error: "Command not found. Make sure the required tools are installed."
      })
    }

    if (error.killed) {
      return NextResponse.json({
        error: "Command timed out after 30 seconds."
      })
    }

    return NextResponse.json({
      error: error.message || "An error occurred while executing the command."
    })
  }
}
```

## DNS Management API

The DNS management functionality is handled by Python scripts rather than Next.js API routes. These scripts integrate with GitHub Actions for automated DNS updates.

### Python DNS Script

**Script**: `manage_dns.py`
**Purpose**: Manage DNS records for emdr.dev domain via Porkbun API

#### Command Line Interface

```bash
python manage_dns.py [options]

Options:
  --subdomain TEXT    Subdomain to manage
  --domain TEXT       Domain name (default: emdr.dev)
  --type TEXT         Record type (A, CNAME, TXT, etc.)
  --content TEXT      Record content (IP address or target)
  --list             List existing records
  --filter TEXT      Filter records by subdomain
  --force            Force update even if record exists
```

#### Environment Variables

```bash
PORKBUN_API_KEY      # Porkbun API key
PORKBUN_SECRET_KEY   # Porkbun secret key
```

#### GitHub Actions Integration

The DNS management integrates with GitHub Actions through automated workflows:

**Trigger Events**:
- Manual workflow dispatch
- Push to main branch (app files)
- Release published

**Workflow Steps**:
1. Checkout repository
2. Set up Python environment
3. Install dependencies
4. Execute DNS update script
5. Verify DNS record creation

#### Example Usage

**Add CNAME Record**:
```bash
python manage_dns.py \
  --subdomain addfuture \
  --domain emdr.dev \
  --type CNAME \
  --content Addfunction.github.io
```

**List Records**:
```bash
python manage_dns.py --list --domain emdr.dev --filter addfuture
```

## Future API Endpoints

### Planned Endpoints

Based on the application architecture, future API endpoints might include:

#### GET /api/health
Health check endpoint for monitoring

#### GET /api/info
Application information and version

#### POST /api/contact
Contact form submission (if contact functionality is added)

#### GET /api/projects
List development projects (if project management is added)

### API Development Guidelines

When adding new API endpoints:

1. **Security First**:
   ```typescript
   // Input validation
   const schema = z.object({
     field: z.string().min(1).max(100)
   })
   
   try {
     const validatedData = schema.parse(requestBody)
   } catch (error) {
     return NextResponse.json({ error: 'Invalid input' }, { status: 400 })
   }
   ```

2. **Consistent Error Handling**:
   ```typescript
   try {
     // API logic
   } catch (error) {
     console.error('API Error:', error)
     return NextResponse.json(
       { error: 'Internal server error' },
       { status: 500 }
     )
   }
   ```

3. **Proper HTTP Status Codes**:
   - `200`: Success
   - `201`: Created
   - `400`: Bad Request
   - `401`: Unauthorized
   - `403`: Forbidden
   - `404`: Not Found
   - `500`: Internal Server Error

4. **Rate Limiting Considerations**:
   ```typescript
   // Future implementation
   const rateLimiter = new Map()
   
   function checkRateLimit(ip: string) {
     // Implementation for rate limiting
   }
   ```

5. **Response Format Consistency**:
   ```typescript
   // Success response
   return NextResponse.json({
     data: result,
     message: 'Operation completed successfully'
   })
   
   // Error response
   return NextResponse.json({
     error: 'Error description',
     code: 'ERROR_CODE'
   }, { status: 400 })
   ```

## Integration Notes

### Client-Side Usage

```typescript
// Example API client function
async function executeCommand(command: string) {
  const response = await fetch('/api/terminal', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ command })
  })
  
  const data = await response.json()
  
  if (!response.ok) {
    throw new Error(data.error || 'Command failed')
  }
  
  return data.output
}
```

### Error Handling

```typescript
// Client-side error handling
try {
  const output = await executeCommand('npm --version')
  console.log('Command output:', output)
} catch (error) {
  console.error('Command failed:', error.message)
  // Handle error appropriately in UI
}
```

This API reference provides the foundation for understanding and extending the application's backend functionality while maintaining security and consistency standards.