"use client"

import React, { useState, useEffect } from 'react'
import { PublicClientApplication, Configuration, LogLevel } from '@azure/msal-browser'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Brain, MessageSquare, Zap, Loader2 } from 'lucide-react'

// MSAL configuration
const msalConfig: Configuration = {
  auth: {
    clientId: process.env.NEXT_PUBLIC_AZURE_CLIENT_ID || 'demo-client-id', // Replace with your Azure App Registration client ID
    authority: 'https://login.microsoftonline.com/common',
    redirectUri: typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000',
  },
  cache: {
    cacheLocation: 'sessionStorage',
    storeAuthStateInCookie: false,
  },
  system: {
    loggerOptions: {
      loggerCallback: (level, message, containsPii) => {
        if (containsPii) {
          return
        }
        switch (level) {
          case LogLevel.Error:
            console.error(message)
            return
          case LogLevel.Info:
            console.info(message)
            return
          case LogLevel.Verbose:
            console.debug(message)
            return
          case LogLevel.Warning:
            console.warn(message)
            return
        }
      },
    },
  },
}

interface CopilotSuggestion {
  id: string
  title: string
  description: string
  action: string
}

export default function CopilotIntegration() {
  const [msalInstance, setMsalInstance] = useState<PublicClientApplication | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [suggestions, setSuggestions] = useState<CopilotSuggestion[]>([])
  const [userInfo, setUserInfo] = useState<any>(null)

  useEffect(() => {
    const initializeMsal = async () => {
      try {
        const pca = new PublicClientApplication(msalConfig)
        await pca.initialize()
        setMsalInstance(pca)

        // Check if user is already authenticated
        const accounts = pca.getAllAccounts()
        if (accounts.length > 0) {
          setIsAuthenticated(true)
          setUserInfo(accounts[0])
          loadCopilotSuggestions()
        }
      } catch (error) {
        console.error('MSAL initialization failed:', error)
      }
    }

    initializeMsal()
  }, [])

  const signIn = async () => {
    if (!msalInstance) return

    setIsLoading(true)
    try {
      const loginRequest = {
        scopes: ['User.Read', 'Mail.Read', 'Files.Read'],
      }

      const result = await msalInstance.loginPopup(loginRequest)
      if (result) {
        setIsAuthenticated(true)
        setUserInfo(result.account)
        loadCopilotSuggestions()
      }
    } catch (error) {
      console.error('Sign in failed:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const signOut = async () => {
    if (!msalInstance) return

    try {
      await msalInstance.logoutPopup()
      setIsAuthenticated(false)
      setUserInfo(null)
      setSuggestions([])
    } catch (error) {
      console.error('Sign out failed:', error)
    }
  }

  const loadCopilotSuggestions = () => {
    // Simulated Copilot suggestions - in a real implementation, 
    // these would come from Microsoft Graph API and Copilot services
    const mockSuggestions: CopilotSuggestion[] = [
      {
        id: '1',
        title: 'Code Review Assistant',
        description: 'AI-powered code analysis and suggestions for your development projects',
        action: 'analyze-code'
      },
      {
        id: '2',
        title: 'Document Generator',
        description: 'Generate technical documentation from your codebase using AI',
        action: 'generate-docs'
      },
      {
        id: '3',
        title: 'Smart Email Drafting',
        description: 'Compose professional emails with AI assistance based on your work context',
        action: 'draft-email'
      },
      {
        id: '4',
        title: 'Meeting Summarizer',
        description: 'Automatically summarize and extract action items from your Teams meetings',
        action: 'summarize-meetings'
      }
    ]

    setSuggestions(mockSuggestions)
  }

  const executeCopilotAction = (action: string) => {
    // In a real implementation, this would trigger specific Copilot actions
    console.log(`Executing Copilot action: ${action}`)
    
    // Show a simple notification for demo purposes
    alert(`Copilot action "${action}" would be executed here. This requires proper Microsoft 365 Copilot API integration.`)
  }

  return (
    <Card className="border-border/50 bg-card/80 backdrop-blur-sm hover:border-primary/50 transition-all duration-300 hover:shadow-lg hover:shadow-primary/10">
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
              <Brain className="w-4 h-4 text-primary" />
            </div>
            <h3 className="text-lg font-semibold">Microsoft 365 Copilot</h3>
            <Badge variant="outline" className="border-primary text-primary">
              AI Enhanced
            </Badge>
          </div>
          
          {!isAuthenticated ? (
            <Button 
              onClick={signIn} 
              disabled={isLoading}
              size="sm"
              className="bg-primary hover:bg-primary/90"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                'Connect'
              )}
            </Button>
          ) : (
            <div className="flex items-center space-x-2">
              <span className="text-xs text-muted-foreground">
                {userInfo?.name || 'Connected'}
              </span>
              <Button onClick={signOut} variant="outline" size="sm">
                Disconnect
              </Button>
            </div>
          )}
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {!isAuthenticated ? (
          <div className="text-center py-6 space-y-3">
            <MessageSquare className="w-12 h-12 text-muted-foreground mx-auto" />
            <p className="text-muted-foreground">
              Connect to Microsoft 365 to unlock AI-powered development assistance
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="flex items-center space-x-2 text-sm">
              <Zap className="w-4 h-4 text-primary" />
              <span className="font-medium">AI Suggestions Available</span>
            </div>
            
            <div className="grid gap-3">
              {suggestions.map((suggestion) => (
                <div 
                  key={suggestion.id}
                  className="p-3 bg-muted/30 rounded-lg border border-border/50 hover:border-primary/50 transition-colors cursor-pointer"
                  onClick={() => executeCopilotAction(suggestion.action)}
                >
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <h4 className="text-sm font-medium">{suggestion.title}</h4>
                      <p className="text-xs text-muted-foreground">{suggestion.description}</p>
                    </div>
                    <Button variant="ghost" size="sm" className="ml-2">
                      Try
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}