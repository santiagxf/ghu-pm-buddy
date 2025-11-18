"""Main entry point for the PM Buddy agent workflow."""

import asyncio
import logging
import sys

from dotenv import load_dotenv
from agent_framework.observability import setup_observability
from agent_framework_devui import serve

from azure.ai.agentserver.agentframework import from_agent_framework
from azure.identity import DefaultAzureCredential

from pm_buddy.extensions.token_provider import set_github_access_token_from_env
from pm_buddy.workflow import build_workflow, run_once


logger = logging.getLogger(__name__)
#patch_transform_output_for_response()


def run_devui(port: int = 8093):
    """Launch the branching workflow in DevUI."""

    logger.info("Building Agent Workflow...")
    workflow = build_workflow()

    logger.info("Starting Agent Workflow in DevUI...")
    logger.info("Available at: http://localhost:%s", port)
    serve(entities=[workflow], port=port, auto_open=True)


def run_server(port: int = 8088):
    """Launch the agent workflow in Agents Hosting."""

    logger.info("Building Agent Workflow...")
    workflow = build_workflow()

    logger.info("Starting Agent Workflow in Agents Hosting...")
    from_agent_framework(workflow.as_agent(), credentials=DefaultAzureCredential()).run(port=port)

if __name__ == "__main__":
    load_dotenv()

    set_github_access_token_from_env(
        app_id_env="PMBUDDY_APP_ID",
        secret_key_env="PMBUDDY_PRIVATE_KEY",
    )

    if "--debug" in sys.argv:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()],
            force=True  # Force reconfiguration even if logging was already set up
        )
        logger.info("Debug logging is enabled.")

    # if runned with command --devui, launch devui
    if "--devui" in sys.argv:
        run_devui()
    elif "--input" in sys.argv:
        setup_observability(enable_sensitive_data=True)

        # gets the input from command line argument --input
        input_index = sys.argv.index("--input") + 1 if "--input" in sys.argv else -1
        inputs = sys.argv[input_index]

        asyncio.run(run_once(inputs))
    else:
        port_index = sys.argv.index("--port") + 1 if "--port" in sys.argv else -1
        port_input = int(sys.argv[port_index]) if port_index != -1 else 8093
        run_server(port_input)
