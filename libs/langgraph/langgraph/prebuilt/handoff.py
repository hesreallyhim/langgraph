from typing import Literal, Optional

from langchain_core.tools import StructuredTool

from langgraph.graph import GraphCommand


class GraphCommandTool(StructuredTool):
    command: GraphCommand


def create_handoff_tool(
    goto: str, name: Optional[str] = None, description: Optional[str] = None
) -> GraphCommandTool:
    """Create a tool that can hand off control to another node."""

    def func():
        return f"Transferred to '{goto}'!", GraphCommand(goto=goto)

    if description is None:
        description = f"Transfer to '{goto}'. Do not ask any details."

    if name is None:
        name = goto

    command = GraphCommand(goto=goto)
    transfer_tool = GraphCommandTool.from_function(
        func,
        command=command,
        name=name,
        description=description,
        response_format="content_and_artifact",
        args_schema=None,
        infer_schema=True,
        return_direct=True,
    )
    return transfer_tool
