import os
from pathlib import Path
from typing import List

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

from agents.shared.models import Diagnostic, Doctor

# Get the absolute path to your project root (capstone folder)
ROOT_DIR = str(Path(__file__).parents[2])
_server_script = str(Path(__file__).parents[2] / "servers" / "insurance_server.py")
# Set up the MCP server to fetch doctors from the insurance server
server = MCPServerStdio(
    "uv", 
    args=["run", "python", _server_script], 
    env={**os.environ, "PYTHONPATH": ROOT_DIR})

system_prompt = """
    You are a helpful assistant that recommends doctors based on the provided diagnostic data.

    ### Role and behaviour:
    - Use the 'fetch_doctors' tool to retrieve the list of doctors covered by the insurance network.
    - Select the most appropriate doctors based on their speciality and the diagnostic information.
    - You may select more than one doctor to let the patient pick between them.
    - If the diagnostic information is not sufficient, then return an empty list of doctors.
    - If no doctors match the given diagnostic information, then return a list with general practitioner 
    doctors. Only use general practitioner doctors for this purpose.
    - Do not fabricate any new doctor data.
    """

agent = Agent(
    model="anthropic:claude-sonnet-4-5",
    system_prompt=system_prompt,
    toolsets=[server],
    output_type=List[Doctor]
)

async def fetch_doctors_from(diagnostics: List[Diagnostic]) -> List[Doctor]:
    diagnostics_str = "\n".join([f"{diagnostic.title}: {diagnostic.definition}" for diagnostic in diagnostics])

    prompt = f"""
    Use the 'fetch_doctors' tool to retrieve the available doctors, then recommend the most
    appropriate ones based on the following diagnostics:

    Diagnostics:
    {diagnostics_str}
    """

    answer = input('\nWould you like to see a list of recommended doctors? (y/n): ')
    if answer.lower() == 'y':
        async with agent:
            from rich.console import Console

            console = Console()
            with console.status("[bold green]Creating a list of doctors...", spinner="dots"):
                result = await agent.run(prompt)
            return result.output
    else:
        print("No problem! If you change your mind, just ask again. Bye!")
        return []
