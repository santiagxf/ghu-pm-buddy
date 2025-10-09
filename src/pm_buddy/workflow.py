# Copyright (c) Microsoft. All rights reserved.

import asyncio
import logging
import os
from typing import Callable
from dotenv import load_dotenv
from opentelemetry.trace import SpanKind
from agent_framework.observability import setup_observability, get_tracer

from agent_framework import (
    AgentExecutorResponse,
    AgentRunEvent,
    WorkflowBuilder,
)
from azure.identity import AzureCliCredential

from pm_buddy.agents import IssueFormatAgent, RefineAgent, InvestigateAgent, RootCauseAnalysisAgent
from pm_buddy.agents.format_agent import GitHubIssue
from pm_buddy.extensions.chat_clients import AzureOpenAIChatClientWithRetry


def has_label_condition(label: str) -> Callable[[AgentExecutorResponse], bool]:
    """Generate a condition function to check if the issue has a specific label."""

    def condition(response: AgentExecutorResponse) -> bool:
        if not isinstance(response, AgentExecutorResponse):
            return True

        issue = GitHubIssue.model_validate_json(response.agent_run_response.text)
        return issue.labels and label in issue.labels

    return condition


async def main():
    """Main function to set up and run the workflow."""

    model = AzureOpenAIChatClientWithRetry(
        deployment_name="gpt-4.1", credential=AzureCliCredential()
    )

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
        RootCauseAnalysisAgent(
            id="root-cause-agent",
            name="root-cause-agent",
            client=model,
        ) as root_cause_agent,
    ):
        workflow = (
            WorkflowBuilder()
            .add_agent(format_agent, id="format-agent")
            .add_agent(investigate_agent, id="investigate-agent")
            .add_agent(refine_agent, id="refine-agent")
            .add_agent(root_cause_agent, id="root-cause-agent")
            .set_start_executor(format_agent)
            .add_edge(format_agent, investigate_agent, has_label_condition("enhancement"))
            .add_edge(format_agent, root_cause_agent, has_label_condition("bug"))
            .add_edge(investigate_agent, refine_agent)
            .add_edge(root_cause_agent, refine_agent)
            .build()
        )

        with get_tracer().start_as_current_span(
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

    # Configure logging to output to console
    logging.basicConfig(
        level=logging.WARNING,  # Set to WARNING to see warning logs
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

    load_dotenv()

    setup_observability(
        enable_sensitive_data=True,
        applicationinsights_connection_string=os.environ.get(
            "AGENT_FRAMEWORK_MONITOR_CONNECTION_STRING"
        ),
        vs_code_extension_port=4317,
    )

    asyncio.run(main())
