# PM Buddy - AI-Powered GitHub Issue Management

> **GitHub Universe 2025** - Build intelligent, multi-agent workflows with GitHub and the Microsoft Agent Framework

PM Buddy is a multi-agent workflow system that automatically triages, investigates, and refines GitHub issues. Built with the [Agent Framework](https://github.com/microsoft/agent-framework) and powered by MCP, it demonstrates how AI agents can collaborate to automate repository management tasks.

## 🎯 What It Does

PM Buddy automates the entire GitHub issue lifecycle:

1. **Format Agent** - Standardizes issue formatting with proper Markdown and applies appropriate labels
2. **Investigate Agent** - Searches codebase, finds related issues, and provides context
3. **Root Cause Agent** - Analyzes bugs and identifies potential causes
4. **Refine Agent** - Synthesizes investigation results into actionable reports

The workflow intelligently branches based on issue type (bug vs. enhancement) and uses MCP tools to interact with GitHub repositories.

## 🏗️ Architecture

```
Issue Created → Format Agent → [Bug? → Root Cause Agent] → Refine Agent
                            → [Enhancement? → Investigate Agent] → Refine Agent
```

### Key Components

- **Agent Framework**: Microsoft's framework for building and orchestrating AI agents
- **Model Context Protocol (MCP)**: Provides standardized tools for GitHub interactions
- **Azure OpenAI**: Powers the AI agents with GPT-4.1
- **GitHub App Authentication**: Secure, automated access to repositories

## 🚀 Getting Started

### Prerequisites

- GitHub Codespaces (recommended) or local dev container
- Azure CLI access
- GitHub App credentials (for MCP integration)
- Azure OpenAI deployment

### Setup

1. **Open in GitHub Codespaces**
   ```bash
   # The repository is configured with a dev container
   # that includes all necessary tools
   ```

2. **Install AI Toolkit Extension**
   ```bash
   # From VS Code command palette
   Extensions: Install from VSIX
   # Navigate to /extensions and install the VSIX files
   ```

3. **Install Dependencies**
   ```bash
   # Install uv package manager
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install project dependencies
   cd src
   uv sync
   ```

4. **Configure Environment**
   ```bash
   # Create .env file from template
   cp .env.example .env
   
   # Edit .env and add:
   # - Azure OpenAI credentials
   # - GitHub App ID and private key
   # - Application Insights connection string (optional)
   
   # Add to ~/.bashrc
   export UV_ENV_FILE=".env"
   ```

5. **Setup Azure CLI**
   ```bash
   # Install Azure CLI
   curl -LsSf https://aka.ms/InstallAzureCLIDeb | sudo bash
   
   # Login
   az login
   ```

6. **Configure MCP**
   
   Edit `mcp.json` to configure the GitHub MCP server with your access token:
   ```json
   {
     "servers": {
       "github": {
         "type": "http",
         "url": "https://api.githubcopilot.com/mcp/",
         "headers": {
           "Authorization": "Bearer YOUR_ACCESS_TOKEN"
         }
       }
     }
   }
   ```

## 🎮 Usage

### Run with DevUI

Launch the interactive development UI to test and debug agents:

```bash
uv run python pm_buddy/main.py --devui
# Opens at http://localhost:8093
```

### Run from Command Line

Process a specific GitHub issue:

```bash
uv run python pm_buddy/main.py --input "You are assigned issue #8 at santiagxf/travel-app"
```

### Debug Mode

Enable detailed logging:

```bash
uv run python pm_buddy/main.py --debug --input "Your issue description"
```

## 🧪 Demo Walkthrough

Check out the [Demo Script](./demo-script.md) for a step-by-step walkthrough of:
- Building agents with AI Toolkit
- Integrating MCP tools
- Testing and iterating on agent prompts
- Running the complete workflow

## 📚 Project Structure

```
pm_buddy/
├── agents/               # Agent implementations
│   ├── format_agent.py   # Issue formatting and labeling
│   ├── investigate_agent.py  # Code search and context gathering
│   ├── refine_agent.py   # Report synthesis
│   ├── root_cause_agent.py   # Bug analysis
│   └── prompts/          # Agent instruction templates
├── extensions/           # Custom integrations
│   ├── chat_clients.py   # Azure OpenAI client with retry logic
│   └── token_provider.py # GitHub App authentication
├── tools/                # MCP tool configuration
│   └── toolkits.py       # Tool filtering utilities
├── main.py               # Entry point
└── workflow.py           # Workflow orchestration
```

## 🔧 Key Features

### Multi-Agent Collaboration
Agents work together in a workflow, each specialized for specific tasks. The workflow intelligently routes issues based on their type and labels.

### MCP Integration
Uses the Model Context Protocol to provide agents with standardized tools for:
- Reading and updating GitHub issues
- Searching code repositories
- Finding related issues and pull requests
- Managing labels and comments

### Observability
Built-in tracing and monitoring with:
- OpenTelemetry instrumentation
- Azure Application Insights integration
- VS Code AI Toolkit tracing support

### Flexible Deployment
- Interactive DevUI for development and testing
- Command-line interface for automation
- GitHub Actions integration (coming soon)

## 🎓 Learning Resources

- [Quickstart Guide](./quickstart.md) - Detailed setup instructions
- [Demo Script](./demo-script.md) - GitHub Universe presentation walkthrough
- [Agent Framework Docs](https://github.com/microsoft/agent-framework)
- [MCP Documentation](https://modelcontextprotocol.io/)

## 📋 Requirements

### Python Packages
- `agent-framework>=1.0.0b251007`
- `agent-framework-devui>=1.0.0b251007`
- `python-dotenv>=1.1.1`
- `tenacity>=8.0.0`

### External Services
- Azure OpenAI (GPT-4.1 deployment)
- GitHub App with repository access
- Azure Application Insights (optional, for monitoring)

## 🤝 Contributing

This is a demo project for GitHub Universe 2025. Feel free to fork and experiment with different agent configurations, prompts, and workflows!

## 📝 License

This project is provided as-is for educational and demonstration purposes.

## 🎤 About This Talk

PM Buddy demonstrates the power of combining:
- **AI Agents** for autonomous task execution
- **MCP** for standardized tool integration
- **Workflow orchestration** for complex automation
- **Azure AI** for enterprise-grade AI capabilities

Learn how to build your own AI-powered automation using GitHub Copilot, Azure OpenAI, and the emerging MCP ecosystem.

---

**Built for GitHub Universe 2025** | [Watch the talk](#) | [Explore the code](https://github.com/santiagxf/ghu-pm-buddy)

GitHub Universe sample
