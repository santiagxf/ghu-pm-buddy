import os
import sys
from typing import Callable, List
from agent_framework import AIFunction
from agent_framework._mcp import MCPTool

from typing import Any

if sys.version_info >= (3, 11):
    from typing import Self  # pragma: no cover
else:
    from typing_extensions import Self  # prag

class MCPToolWithFilter(MCPTool):
    """A wrapper around MCPTool that filters its functions based on a provided filter function."""

    def __init__(self, server: MCPTool, filter_func: Callable[[AIFunction], bool]) -> None:
        """Initialize the MCPToolWithFilter with a server and a filter function.
        
        Args:
            server (MCPTool): The MCPTool instance to wrap.
            filter_func (Callable[[AIFunction], bool]): A function that takes 
                an AIFunction and returns True if it should be included.
        """
        self._wrapped = server
        self._filter_func = filter_func

    async def load_tools(self) -> None:
        await self._wrapped.load_tools()

        self._wrapped.functions = list(filter(self._filter_func, self._wrapped.functions))

    def __getattr__(self, name: str) -> Any:
        return getattr(self._wrapped, name)

    def __str__(self) -> str:
        return str(self._wrapped)

    async def __aenter__(self) -> Self:
        return await self._wrapped.__aenter__()

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: Any
    ) -> None:
        await self._wrapped.__aexit__(exc_type, exc_value, traceback)
