# Copyright (c) Microsoft. All rights reserved.

import logging
from typing import Callable
from opentelemetry.trace import SpanKind
from agent_framework.observability import get_tracer

from agent_framework import (
    AgentExecutorResponse,
    AgentRunEvent,
    WorkflowBuilder,
)
from azure.identity import DefaultAzureCredential

from pm_buddy.agents import IssueFormatAgent, RefineAgent, InvestigateAgent, RootCauseAnalysisAgent
from pm_buddy.agents.format_agent import GitHubIssue
from pm_buddy.extensions.chat_clients import AzureOpenAIChatClientWithRetry

logger = logging.getLogger(__name__)


def has_label_condition(label: str) -> Callable[[AgentExecutorResponse], bool]:
    """Generate a condition function to check if the issue has a specific label."""

    def condition(response: AgentExecutorResponse) -> bool:
        print("Checking for label:", label)
        if not isinstance(response, AgentExecutorResponse):
            return True

        try:
            issue = GitHubIssue.model_validate_json(response.agent_run_response.text)
        except Exception as e:
            print("Error parsing issue from response:", e)
            print("Full text", response.agent_run_response.text)
            return False
        return issue.labels and label in issue.labels

    return condition


def build_workflow() -> WorkflowBuilder:
    """Main function to set up and run the workflow."""

    model = AzureOpenAIChatClientWithRetry(
        deployment_name="gpt-4o", credential=DefaultAzureCredential()
    )

    format_agent = IssueFormatAgent(
        id="format-agent",
        name="format-agent",
        client=model,
    )
    investigate_agent = InvestigateAgent(
        id="investigate-agent",
        name="investigate-agent",
        client=model,
    )
    root_cause_agent = RootCauseAnalysisAgent(
        id="root-cause-agent",
        name="root-cause-agent",
        client=model,
    )
    refine_agent = RefineAgent(
        id="refine-agent",
        name="refine-agent",
        client=model,
    )

    workflow = (
        WorkflowBuilder()
        .add_agent(format_agent, id="format-agent")
#        .add_agent(investigate_agent, id="investigate-agent")
#        .add_agent(refine_agent, id="refine-agent")
#        .add_agent(root_cause_agent, id="root-cause-agent")
        .set_start_executor(format_agent)
#        .add_edge(format_agent, investigate_agent, has_label_condition("enhancement"))
#        .add_edge(format_agent, root_cause_agent, has_label_condition("bug"))
#        .add_edge(investigate_agent, refine_agent)
#        .add_edge(root_cause_agent, refine_agent)
        .build()
    )

    return workflow


async def run_once(inputs: str) -> str:
    """Run the workflow once with the given input.
    
    Args:
        inputs: The input string to process.
    Returns:
        The final state of the workflow run.
    """
    logger.info("Building workflow...")
    workflow = build_workflow()

    logger.info("Running workflow...")
    with get_tracer().start_as_current_span(
        name="pm-buddy-workflow",
        kind=SpanKind.CLIENT,
        attributes={
            "gen_ai.system": "agent-framework", 
            "gen_ai.operation.name": "invoke_agent",
            "gen_ai.agent.id": "pm-buddy-workflow:2"
        },
    ):
        events = await workflow.run(inputs)

        for event in events:
            if isinstance(event, AgentRunEvent):
                logger.info(f"{event.executor_id}: {event.data}")

        # Summarize the final run state (e.g., COMPLETED)
        final_state = events.get_final_state()
        logger.info(f"Final state: {final_state}")

        return final_state
