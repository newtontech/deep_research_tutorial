from typing import Dict, Any

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool

from .prompt import instructions_v1, instructions_v1_zh
from ..llm_config import create_default_config
from ..tools.database import DatabaseManager


def save_query_results(
        tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Any
    ) -> None:
    """Callback to modify state parameters for search tools"""
    tool_info = {}
    tool_info['tool_name'] = tool.name
    tool_info['tool_args'] = args
    tool_info['tool_response'] = tool_response
    if tool_context.state.get('database_agent_tool_call', None) is None:
        tool_context.state['database_agent_tool_call'] = [tool_info]
    else:
        toolcall = tool_context.state['database_agent_tool_call']
        toolcall.append(tool_info)
        tool_context.state['database_agent_tool_call'] = toolcall
    return


def init_database_agent(config):
    """Initialize the database agent with the given configuration."""
    selected_model = config.deepseek_chat
    db_manager = DatabaseManager()
    query_table = db_manager.init_query_table()

    database_agent = LlmAgent(
        name="database_agent",
        model=selected_model,
        instruction=instructions_v1,
        description="Construct database queries based on user's question and summarize the results.",
        tools=[query_table],
        output_key="query_result",
        after_tool_callback=save_query_results,
    )
    return database_agent

config = create_default_config()
root_agent = init_database_agent(config)