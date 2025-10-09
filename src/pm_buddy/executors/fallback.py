from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from agent_framework import (
    AgentExecutorResponse,
    __version__,
    ChatAgent,
    AgentRunEvent,
    Executor,
    ChatMessage,
    WorkflowContext,
    handler,
)
import agent_framework.exceptions


class FallbackAgentExecutor(Executor):
    """An executor that runs a given agent with retry logic and exponential backoff."""
    
    agent: ChatAgent

    def __init__(self, agent: ChatAgent, **data) -> None:
        # Initialize the parent Pydantic model properly
        super().__init__(agent=agent, **data)

    @handler
    async def handle(
        self, messages: list[ChatMessage], ctx: WorkflowContext[list[ChatMessage] | str]
    ) -> None:
        print(f"Running FallbackAgentExecutor {self.id}:")

        for message in messages:
            print(f"Message: {message.role}: {message.text}")

        # Handle agent_framework.exceptions.ServiceResponseException with
        # a backoff and retry mechanism using tenacity
        response = await self._run_with_retry(messages)
        messages.extend(response.messages)
        await ctx.send_message(response)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(agent_framework.exceptions.ServiceResponseException),
        reraise=True
    )
    async def _run_with_retry(self, messages: list[ChatMessage]):
        """Run the agent with retry logic and exponential backoff."""
        print(f"Attempting to run agent {self.agent.name}...")
        return await self.agent.run(messages)
