"""Root cause analysis agent."""

import os
from agent_framework import __version__
from agent_framework import ChatAgent, ChatClientProtocol
from agent_framework._mcp import MCPStreamableHTTPTool

from pm_buddy.tools.toolkits import MCPToolWithFilter
from pm_buddy.utils import get_prompt_template


class RootCauseAnalysisAgent(ChatAgent):
    """Agent that analyzes the root cause of GitHub issues."""

    def __init__(self, client: ChatClientProtocol, **kwargs):
        super().__init__(
            chat_client=client,
            instructions=get_prompt_template("root_cause_analysis_agent"),
            tools = MCPToolWithFilter(
                server=MCPStreamableHTTPTool(
                    name="github-mcp",
                    url="https://api.githubcopilot.com/mcp/",
                    headers={"Authorization": f"Bearer {os.environ['GITHUB_APP_TOKEN']}"},
                ),
                filter_func=lambda t: "issue" in t.name or "search" in t.name or "file" in t.name
            ),
            **kwargs
        )
