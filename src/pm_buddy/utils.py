"""Utility functions for PM Buddy application."""

from pathlib import Path

def get_prompt_template(agent_name: str) -> str:
    """Load prompt template for the specified agent.
    
    Args:
        agent_name: Name of the agent (e.g., 'format_agent')
        
    Returns:
        The prompt template content as a string
    """
    prompt_path = Path(__file__).parent / "agents" / "prompts" / f"{agent_name}.prompt"

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {prompt_path}")

    return prompt_path.read_text(encoding="utf-8")
