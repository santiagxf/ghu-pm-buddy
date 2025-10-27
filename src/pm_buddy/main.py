"""Main entry point for the PM Buddy agent workflow."""

import asyncio
import logging
import sys

from dotenv import load_dotenv
from agent_framework.observability import setup_observability
from agent_framework_devui import serve

from pm_buddy.extensions.token_provider import set_github_access_token_from_env
from pm_buddy.workflow import build_workflow, run_once

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_devui():
    """Launch the branching workflow in DevUI."""

    logger.info("Building Agent Workflow...")
    workflow = build_workflow()
    port = 8093

    logger.info("Starting Agent Workflow in DevUI...")
    logger.info("Available at: http://localhost:%s", port)
    serve(entities=[workflow], port=port, auto_open=True)


if __name__ == "__main__":
    load_dotenv()

    set_github_access_token_from_env(
        app_id_env="PMBUDDY_APP_ID",
        secret_key_env="PMBUDDY_PRIVATE_KEY",
    )

    setup_observability(
        enable_sensitive_data=True,
    )

    if "--debug" in sys.argv:
        logging.basicConfig(
            level=logging.WARNING,  # Set to WARNING to see warning logs
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )

    # if runned with command --devui, launch devui
    if "--devui" in sys.argv:
        run_devui()
    else:
        # gets the input from command line argument --input
        input_index = sys.argv.index("--input") + 1 if "--input" in sys.argv else -1
        if input_index == -1 or input_index >= len(sys.argv):
            print("Please provide an input using --input 'your issue description'")
            sys.exit(1)

        inputs = sys.argv[input_index]

        asyncio.run(run_once(inputs))
