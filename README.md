# PM Buddy - AI-Powered GitHub Issue Management

> **GitHub Universe 2025** - [Build intelligent, multi-agent workflows with GitHub and the Microsoft Agent Framework](https://reg.githubuniverse.com/flow/github/universe25/attendee-portal/page/sessioncatalog/session/1753979299598001wbZM)

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
- A GitHub App (or you can use your PAT)
- Azure CLI access
- Azure AI Foundry project with model deployment or access to GitHub Models.

### Setup

Follow this steps to get the environment ready:

1. Open the repository in GitHub Codespaces.
1. Install the AI Toolkit extension.
2. Install `uv` package manager:
    - In the console type `curl -LsSf https://astral.sh/uv/install.sh | sh`
    - Type `uv --version` to confirm `uv` is installed.

3. Install packages.
    - Move to the folder `src`.
    - Restore the project with `uv sync`.

4. Configure `uv` environment file:
    - Edit the file `.env.example` and rename it to `.env`.
    - Configure the environment variables indicated there.
    - Edit `~/.bashrc` and add `export UV_ENV_FILE=".env"`.

5. Install the Azure CLI tool:
    - Run `curl -LsSf https://aka.ms/InstallAzureCLIDeb | sudo bash`
    - Login to Azure with `az login`. Use `az login`


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
uv run python pm_buddy/main.py --input "You are assigned issue #26 at santiagxf/travel-app"
```

### Debug Mode

Enable detailed logging:

```bash
uv run python pm_buddy/main.py --debug --input "You are assigned issue #8 at santiagxf/travel-app"
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
├── agents/                   # Agent implementations
│   ├── prompts/              # Agent instruction templates
│   ├── investigate_agent.py  # Code search and context gathering
│   ├── refine_agent.py       # Report synthesis
│   ├── format_agent.py       # Issue formatting and labeling
│   └── root_cause_agent.py   # Bug analysis
├── extensions/               # Custom integrations
│   ├── chat_clients.py       # Azure OpenAI client with retry logic
│   └── token_provider.py     # GitHub App authentication
├── tools/                    # MCP tool configuration
│   └── toolkits.py           # Tool filtering utilities
├── main.py                   # Entry point
└── workflow.py               # Workflow orchestration
```

## 🔧 Key Features

### Multi-Agent Collaboration
Agents work together in a workflow, each specialized for specific tasks. The workflow intelligently routes issues based on their type and labels. Microsoft Agent Framework allows the composability of multiple agents and their orchestration.

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

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) file for the full terms.

## 🎤 About This Talk

PM Buddy demonstrates the power of combining:
- **AI Agents** for autonomous task execution
- **MCP** for standardized tool integration
- **Microsft Agent Framework** for orchestration and complex automation
- **Azure AI Foundry** for enterprise-grade AI capabilities

Learn how to build your own AI-powered automation using GitHub Copilot, Azure, and the emerging MCP ecosystem.

---

**Built for GitHub Universe 2025** | [Watch the talk](https://reg.githubuniverse.com/flow/github/universe25/attendee-portal/page/sessioncatalog/session/1753979299598001wbZM) | [Explore the code](https://github.com/santiagxf/ghu-pm-buddy)
