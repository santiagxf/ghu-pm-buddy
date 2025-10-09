# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os
from typing import override
from agent_framework.exceptions import ServiceResponseException
from agent_framework_azure_ai import AzureAIAgentClient
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from agent_framework.observability import setup_observability

from agent_framework import (
    AgentExecutorResponse,
    __version__,
    AgentRunEvent,
    WorkflowBuilder,
)
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
#from azure.ai.projects import AIProjectClient

from pm_buddy.agents import IssueFormatAgent, RefineAgent, InvestigateAgent
from pm_buddy.agents.format_agent import GitHubIssue

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


def is_feature_condition(response: AgentExecutorResponse) -> bool:
    """Condition function to check if the issue is labeled as a feature."""

    if not isinstance(response, AgentExecutorResponse):
        return True

    issue = GitHubIssue.model_validate_json(response.agent_run_response.text)
    return issue.labels and "enhancement" in issue.labels

def print_exception(retry_state):
    print(f"All retry attempts failed. Last exception: {retry_state.outcome.exception()}")
    return retry_state.outcome.result()

class AzureOpenAIChatClientWithRetry(AzureOpenAIChatClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @override
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(ServiceResponseException),
        reraise=True,
        retry_error_callback=print_exception
    )
    def get_response(self, *args, **kwargs):
        return super().get_response(*args, **kwargs)

async def main():
    model = AzureOpenAIChatClientWithRetry(
        deployment_name="gpt-4.1", credential=AzureCliCredential()
    )
    client = AzureAIAgentClient(
        async_credential=AzureCliCredential(),
        model_deployment_name="gpt-4.1"
    )

    #project_client = AIProjectClient(
    #    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    #    credential=AzureCliCredential(),
    #)
    #thread = project_client.agents.threads.create()

    async with (
        IssueFormatAgent(
            id="format-agent",
            name="format-agent",
            client=model,
        ) as format_agent,
        InvestigateAgent(
            id="investigate-agent",
            name="investigate-agent",
            client=model,
        ) as investigate_agent,
        RefineAgent(
            id="refine-agent",
            name="refine-agent",
            client=model,
        ) as refine_agent,
    ):
        #investigation_thread = investigate_agent.get_new_thread(service_thread_id=thread.id)
        workflow = (
            WorkflowBuilder()
            .add_agent(format_agent, id="format-agent")
            .add_agent(investigate_agent, id="investigate-agent")
            .set_start_executor(format_agent)
            .add_edge(format_agent, investigate_agent, is_feature_condition)
            # .add_edge(investigate_agent, refine_agent)
            .build()
        )

        tracer = trace.get_tracer("agent_framework", __version__)
        with tracer.start_as_current_span(
            name="pm-buddy-workflow",
            kind=SpanKind.CLIENT,
            attributes={
                "gen_ai.system": "agent-framework", 
                "gen_ai.operation.name": "invoke_agent"
            },
        ):
            events = await workflow.run(
                "You are assigned issue number 8 in the repository `santiagxf/travel-app`"
            )
            # Print agent run events and final outputs
            for event in events:
                if isinstance(event, AgentRunEvent):
                    print(f"{event.executor_id}: {event.data}")

            # Summarize the final run state (e.g., COMPLETED)
            print("Final state:", events.get_final_state())


if __name__ == "__main__":

    # load .env file if it exists

    load_dotenv()

    setup_observability(
        enable_sensitive_data=True,
        applicationinsights_connection_string=os.environ.get(
            "AGENT_FRAMEWORK_MONITOR_CONNECTION_STRING"
        ),
        otlp_endpoint=None,
        vs_code_extension_port=None,
    )

    asyncio.run(main())
