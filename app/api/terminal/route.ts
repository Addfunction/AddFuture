import { type NextRequest, NextResponse } from "next/server"
import { exec } from "child_process"
import { promisify } from "util"

const execAsync = promisify(exec)

export async function POST(request: NextRequest) {
  try {
    const { command } = await request.json()

    if (!command || typeof command !== "string") {
      return NextResponse.json({ error: "Invalid command" }, { status: 400 })
    }

    // Security: Only allow specific commands
    const allowedCommands = ["npm", "node", "git", "cat", "ls", "pwd", "whoami", "date"]
    const commandParts = command.trim().split(" ")
    const baseCommand = commandParts[0]

    if (!allowedCommands.includes(baseCommand)) {
      return NextResponse.json(
        {
          error: `Command '${baseCommand}' is not allowed for security reasons.`,
        },
        { status: 403 },
      )
    }

    // Execute the command with timeout
    const { stdout, stderr } = await execAsync(command, {
      timeout: 30000, // 30 second timeout
      maxBuffer: 1024 * 1024, // 1MB buffer
    })

    const output = stdout || stderr || "Command completed successfully"

    return NextResponse.json({ output })
  } catch (error: any) {
    console.error("Terminal command error:", error)

    if (error.code === "ENOENT") {
      return NextResponse.json({
        error: `Command not found. Make sure the required tools are installed.`,
      })
    }

    if (error.killed) {
      return NextResponse.json({
        error: "Command timed out after 30 seconds.",
      })
    }

    return NextResponse.json({
      error: error.message || "An error occurred while executing the command.",
    })
  }
}
