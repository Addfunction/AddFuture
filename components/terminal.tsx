"use client"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { TerminalIcon, Minimize2, X } from "lucide-react"

interface CommandHistory {
  command: string
  output: string
  timestamp: Date
}

export default function Terminal() {
  const [isMinimized, setIsMinimized] = useState(false)
  const [currentCommand, setCurrentCommand] = useState("")
  const [history, setHistory] = useState<CommandHistory[]>([
    {
      command: "welcome",
      output: "Welcome to FutureOS Terminal v2.1.0\nType 'help' for available commands.",
      timestamp: new Date(),
    },
  ])
  const [commandHistory, setCommandHistory] = useState<string[]>([])
  const [historyIndex, setHistoryIndex] = useState(-1)
  const inputRef = useRef<HTMLInputElement>(null)
  const terminalRef = useRef<HTMLDivElement>(null)

  const executeSystemCommand = async (cmd: string): Promise<string> => {
    try {
      const response = await fetch("/api/terminal", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ command: cmd }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data.output || data.error || "Command executed"
    } catch (error) {
      return `Error executing command: ${error instanceof Error ? error.message : "Unknown error"}`
    }
  }

  const commands = {
    help: "Available commands:\n• help - Show this help message\n• clear - Clear terminal\n• date - Show current date and time\n• whoami - Display current user\n• ls - List directory contents\n• pwd - Print working directory\n• echo [text] - Display text\n• neofetch - System information\n• matrix - Enter the matrix\n• npm [args] - Run npm commands\n• node [file] - Run Node.js files\n• git [args] - Run git commands\n• cat [file] - Display file contents",
    clear: "",
    date: () => new Date().toString(),
    whoami: "future_user@futureos",
    ls: "Documents/  Downloads/  Projects/  System/  .config/  node_modules/  package.json",
    pwd: "/home/future_user/projects/futuristic-app",
    neofetch: `
    ╭─────────────────────────────╮
    │  ███████╗██╗   ██╗████████╗ │
    │  ██╔════╝██║   ██║╚══██╔══╝ │
    │  █████╗  ██║   ██║   ██║    │
    │  ██╔══╝  ██║   ██║   ██║    │
    │  ██║     ╚██████╔╝   ██║    │
    │  ╚═╝      ╚═════╝    ╚═╝    │
    ╰─────────────────────────────╯
    
    OS: FutureOS 2024.1
    Kernel: 6.8.0-future
    Shell: ash
    Terminal: FutureTerminal
    CPU: Quantum Processor X1
    Memory: 32GB Holographic RAM
    Node: v20.10.0
    npm: 10.2.3`,
    matrix: "Wake up, Neo... The Matrix has you.",
  }

  const executeCommand = async (cmd: string) => {
    const trimmedCmd = cmd.trim()
    if (!trimmedCmd) return

    let output = ""

    if (trimmedCmd === "clear") {
      setHistory([])
      return
    }

    // Handle echo command
    if (trimmedCmd.startsWith("echo ")) {
      output = trimmedCmd.substring(5)
    }
    // Handle system commands (npm, node, git, etc.)
    else if (
      trimmedCmd.startsWith("npm ") ||
      trimmedCmd.startsWith("node ") ||
      trimmedCmd.startsWith("git ") ||
      trimmedCmd.startsWith("cat ") ||
      trimmedCmd === "npm" ||
      trimmedCmd === "node" ||
      trimmedCmd === "git"
    ) {
      // Add loading indicator
      const loadingEntry: CommandHistory = {
        command: trimmedCmd,
        output: "Executing command...",
        timestamp: new Date(),
      }
      setHistory((prev) => [...prev, loadingEntry])

      // Execute system command
      output = await executeSystemCommand(trimmedCmd)

      // Remove loading entry and add result
      setHistory((prev) => prev.slice(0, -1))
    }
    // Handle built-in commands
    else if (commands[trimmedCmd as keyof typeof commands]) {
      const result = commands[trimmedCmd as keyof typeof commands]
      output = typeof result === "function" ? result() : result
    } else {
      output = `Command not found: ${trimmedCmd}\nType 'help' for available commands.`
    }

    const newEntry: CommandHistory = {
      command: trimmedCmd,
      output,
      timestamp: new Date(),
    }

    setHistory((prev) => [...prev, newEntry])
    setCommandHistory((prev) => [...prev, trimmedCmd])
    setHistoryIndex(-1)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      executeCommand(currentCommand)
      setCurrentCommand("")
    } else if (e.key === "ArrowUp") {
      e.preventDefault()
      if (commandHistory.length > 0) {
        const newIndex = historyIndex === -1 ? commandHistory.length - 1 : Math.max(0, historyIndex - 1)
        setHistoryIndex(newIndex)
        setCurrentCommand(commandHistory[newIndex])
      }
    } else if (e.key === "ArrowDown") {
      e.preventDefault()
      if (historyIndex !== -1) {
        const newIndex = historyIndex + 1
        if (newIndex >= commandHistory.length) {
          setHistoryIndex(-1)
          setCurrentCommand("")
        } else {
          setHistoryIndex(newIndex)
          setCurrentCommand(commandHistory[newIndex])
        }
      }
    }
  }

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight
    }
  }, [history])

  useEffect(() => {
    if (!isMinimized && inputRef.current) {
      inputRef.current.focus()
    }
  }, [isMinimized])

  if (isMinimized) {
    return (
      <div className="fixed bottom-4 left-4 z-50">
        <Badge
          variant="outline"
          className="border-primary bg-black/90 text-primary hover:bg-primary/10 cursor-pointer px-4 py-2"
          onClick={() => setIsMinimized(false)}
        >
          <TerminalIcon className="w-4 h-4 mr-2" />
          Terminal
        </Badge>
      </div>
    )
  }

  return (
    <div className="fixed bottom-4 right-4 z-50 w-96 h-80">
      <Card className="h-full bg-black/95 border-primary/50 shadow-2xl shadow-primary/20">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 px-4 py-2 border-b border-primary/20">
          <div className="flex items-center space-x-2">
            <TerminalIcon className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">FutureTerminal</span>
          </div>
          <div className="flex items-center space-x-1">
            <button
              onClick={() => setIsMinimized(true)}
              className="w-6 h-6 rounded-full bg-yellow-500/20 hover:bg-yellow-500/30 flex items-center justify-center transition-colors"
            >
              <Minimize2 className="w-3 h-3 text-yellow-400" />
            </button>
            <button className="w-6 h-6 rounded-full bg-red-500/20 hover:bg-red-500/30 flex items-center justify-center transition-colors">
              <X className="w-3 h-3 text-red-400" />
            </button>
          </div>
        </CardHeader>
        <CardContent className="p-0 h-full">
          <div
            ref={terminalRef}
            className="h-full overflow-y-auto p-4 font-mono text-sm bg-black text-green-400 scrollbar-thin scrollbar-thumb-primary/30"
          >
            {history.map((entry, index) => (
              <div key={index} className="mb-2">
                <div className="flex items-center space-x-2 text-cyan-400">
                  <span className="text-pink-400">future_user@futureos</span>
                  <span className="text-white">:</span>
                  <span className="text-blue-400">~</span>
                  <span className="text-white">$</span>
                  <span className="text-green-400">{entry.command}</span>
                </div>
                {entry.output && <pre className="whitespace-pre-wrap text-green-300 mt-1 ml-4">{entry.output}</pre>}
              </div>
            ))}
            <div className="flex items-center space-x-2 text-cyan-400">
              <span className="text-pink-400">future_user@futureos</span>
              <span className="text-white">:</span>
              <span className="text-blue-400">~</span>
              <span className="text-white">$</span>
              <input
                ref={inputRef}
                type="text"
                value={currentCommand}
                onChange={(e) => setCurrentCommand(e.target.value)}
                onKeyDown={handleKeyDown}
                className="flex-1 bg-transparent outline-none text-green-400 font-mono"
                placeholder=""
                autoFocus
              />
              <span className="animate-pulse text-green-400">█</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
