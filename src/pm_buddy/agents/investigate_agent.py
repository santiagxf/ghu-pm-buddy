"""Format Agent module for PM Buddy."""

import os
from collections.abc import AsyncIterable, Callable, MutableMapping, Sequence
from typing import Any, Literal

from agent_framework import __version__
from agent_framework import ChatAgent, ChatClientProtocol
from agent_framework._mcp import MCPStreamableHTTPTool
from agent_framework._types import AgentRunResponse, AgentRunResponseUpdate, ChatMessage, ToolMode
from agent_framework._threads import AgentThread
from agent_framework._tools import ToolProtocol
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from pm_buddy.tools.toolkits import MCPToolWithFilter
from pm_buddy.utils import get_prompt_template

class InvestigateAgent(ChatAgent):
    """Agent that investigates GitHub issues according to specific guidelines."""

    def __init__(self, client: ChatClientProtocol, **kwargs):
        super().__init__(
            chat_client=client,
            instructions=get_prompt_template("investigate_agent"),
            tools = MCPToolWithFilter(
                server=MCPStreamableHTTPTool(
                    name="github-mcp",
                    url="https://api.githubcopilot.com/mcp/",
                    headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"},
                ),
                filter_func=lambda t: "issue" in t.name or "search" in t.name or "file" in t.name
            ),
            **kwargs
        )

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    async def run(
        self,
        messages: str | ChatMessage | list[str] | list[ChatMessage] | None = None,
        *,
        thread: AgentThread | None = None,
        frequency_penalty: float | None = None,
        logit_bias: dict[str | int, float] | None = None,
        max_tokens: int | None = None,
        metadata: dict[str, Any] | None = None,
        model_id: str | None = None,
        presence_penalty: float | None = None,
        response_format: type[BaseModel] | None = None,
        seed: int | None = None,
        stop: str | Sequence[str] | None = None,
        store: bool | None = None,
        temperature: float | None = None,
        tool_choice: ToolMode | Literal["auto", "required", "none"] | dict[str, Any] | None = None,
        tools: ToolProtocol
        | Callable[..., Any]
        | MutableMapping[str, Any]
        | list[ToolProtocol | Callable[..., Any] | MutableMapping[str, Any]]
        | None = None,
        top_p: float | None = None,
        user: str | None = None,
        additional_chat_options: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> AgentRunResponse:
        """Run the agent with retry logic using exponential backoff.
        
        This method wraps the parent class's run method with retry logic.
        It will retry up to 3 times with exponential backoff (4s, 8s, 10s max).
        
        Args:
            messages: The messages to process.

        Keyword Args:
            thread: The thread to use for the agent.
            frequency_penalty: The frequency penalty to use.
            logit_bias: The logit bias to use.
            max_tokens: The maximum number of tokens to generate.
            metadata: Additional metadata to include in the request.
            model_id: The model_id to use for the agent.
            presence_penalty: The presence penalty to use.
            response_format: The format of the response.
            seed: The random seed to use.
            stop: The stop sequence(s) for the request.
            store: Whether to store the response.
            temperature: The sampling temperature to use.
            tool_choice: The tool choice for the request.
            tools: The tools to use for the request.
            top_p: The nucleus sampling probability to use.
            user: The user to associate with the request.
            additional_chat_options: Additional properties to include in the request.
            kwargs: Additional keyword arguments for the agent.
            
        Returns:
            An AgentRunResponse containing the agent's response.
            
        Raises:
            Exception: Re-raises the last exception if all retry attempts fail.
        """
        return await super().run(
            messages=messages,
            thread=thread,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            max_tokens=max_tokens,
            metadata=metadata,
            model_id=model_id,
            presence_penalty=presence_penalty,
            response_format=response_format,
            seed=seed,
            stop=stop,
            store=store,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            user=user,
            additional_chat_options=additional_chat_options,
            **kwargs
        )

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=10),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    async def run_stream(
        self,
        messages: str | ChatMessage | list[str] | list[ChatMessage] | None = None,
        *,
        thread: AgentThread | None = None,
        frequency_penalty: float | None = None,
        logit_bias: dict[str | int, float] | None = None,
        max_tokens: int | None = None,
        metadata: dict[str, Any] | None = None,
        model_id: str | None = None,
        presence_penalty: float | None = None,
        response_format: type[BaseModel] | None = None,
        seed: int | None = None,
        stop: str | Sequence[str] | None = None,
        store: bool | None = None,
        temperature: float | None = None,
        tool_choice: ToolMode | Literal["auto", "required", "none"] | dict[str, Any] | None = None,
        tools: ToolProtocol
        | Callable[..., Any]
        | MutableMapping[str, Any]
        | list[ToolProtocol | Callable[..., Any] | MutableMapping[str, Any]]
        | None = None,
        top_p: float | None = None,
        user: str | None = None,
        additional_chat_options: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> AsyncIterable[AgentRunResponseUpdate]:
        """Run the agent in streaming mode with retry logic using exponential backoff.
        
        This method wraps the parent class's run_stream method with retry logic.
        It will retry up to 3 times with exponential backoff (4s, 8s, 10s max).
        
        Args:
            messages: The messages to process.

        Keyword Args:
            thread: The thread to use for the agent.
            frequency_penalty: The frequency penalty to use.
            logit_bias: The logit bias to use.
            max_tokens: The maximum number of tokens to generate.
            metadata: Additional metadata to include in the request.
            model_id: The model_id to use for the agent.
            presence_penalty: The presence penalty to use.
            response_format: The format of the response.
            seed: The random seed to use.
            stop: The stop sequence(s) for the request.
            store: Whether to store the response.
            temperature: The sampling temperature to use.
            tool_choice: The tool choice for the request.
            tools: The tools to use for the request.
            top_p: The nucleus sampling probability to use.
            user: The user to associate with the request.
            additional_chat_options: Additional properties to include in the request.
            kwargs: Additional keyword arguments for the agent.
            
        Yields:
            AgentRunResponseUpdate objects containing streaming response chunks.
            
        Raises:
            Exception: Re-raises the last exception if all retry attempts fail.
        """
        async for update in super().run_stream(
            messages=messages,
            thread=thread,
            frequency_penalty=frequency_penalty,
            logit_bias=logit_bias,
            max_tokens=max_tokens,
            metadata=metadata,
            model_id=model_id,
            presence_penalty=presence_penalty,
            response_format=response_format,
            seed=seed,
            stop=stop,
            store=store,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_p=top_p,
            user=user,
            additional_chat_options=additional_chat_options,
            **kwargs
        ):
            yield update
