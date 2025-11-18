"""Format Agent module for PM Buddy."""

import os
from typing import List
from agent_framework import __version__
from agent_framework import ChatAgent, ChatClientProtocol
from agent_framework._mcp import MCPStreamableHTTPTool
from pydantic import BaseModel

from pm_buddy.tools.toolkits import MCPToolWithFilter
from pm_buddy.utils import get_prompt_template

class GitHubIssue(BaseModel):
    """A simple representation of a GitHub issue."""
    repository: str
    issue_number: int
    title: str
    body: str
    labels: List[str]

class IssueFormatAgent(ChatAgent):
    """Agent that formats GitHub issues according to specific guidelines."""

    def __init__(self, client: ChatClientProtocol, **kwargs):
        super().__init__(
            chat_client=client,
            instructions=get_prompt_template("format_agent"),
            tools = MCPToolWithFilter(
                server=MCPStreamableHTTPTool(
                    name="github-mcp",
                    url="https://api.githubcopilot.com/mcp/",
                    headers={"Authorization": f"Bearer {os.environ['GITHUB_APP_TOKEN']}"},
                ),
                filter_func=lambda f: "issue" in f.name
            ),
            response_format=GitHubIssue,
            **kwargs
        )
