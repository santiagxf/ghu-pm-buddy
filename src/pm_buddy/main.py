import asyncio
import logging
import sys
import os

from dotenv import load_dotenv
from agent_framework.observability import setup_observability
from agent_framework.devui import serve

from pm_buddy.workflow import build_workflow, run_once

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_devui():
    """Launch the branching workflow in DevUI."""

    logger.info("Building Agent Workflow...")
    workflow = build_workflow()

    logger.info("Starting Agent Workflow in DevUI...")
    logger.info("Available at: http://localhost:8093")
    serve(entities=[workflow], port=8093, auto_open=True)


if __name__ == "__main__":  
    load_dotenv()

    setup_observability(
        enable_sensitive_data=True,
        applicationinsights_connection_string=os.environ.get(
            "AGENT_FRAMEWORK_MONITOR_CONNECTION_STRING"
        ),
        vs_code_extension_port=4317,
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
