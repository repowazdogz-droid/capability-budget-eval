"""Provider smoke test: the stock Inspect tool-calling example.

Taken from the current Inspect docs (https://inspect.aisi.org.uk/tools.html).
Its only job is to confirm, end to end, that the local provider works AND that
the local model emits a real native tool call -- rather than trusting the
`tools` capability string in the Ollama manifest.

    .venv/bin/inspect eval smoke_addition.py --model ollama/<model>
"""

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import match
from inspect_ai.solver import generate, use_tools
from inspect_ai.tool import tool


@tool
def add():
    async def execute(x: int, y: int):
        """
        Add two numbers.

        Args:
            x: First number to add.
            y: Second number to add.

        Returns:
            The sum of the two numbers.
        """
        return x + y

    return execute


@task
def addition_problem():
    return Task(
        dataset=[Sample(input="What is 1 + 1?", target=["2"])],
        solver=[use_tools(add()), generate()],
        scorer=match(numeric=True),
    )
