from datetime import datetime

from google.adk.agents.callback_context import CallbackContext
from .tools.database import DatabaseManager


def init_prepare_state_before_agent(config):
    """prepare state before agent runs"""
    def prepare_state_before_agent(callback_context: CallbackContext):
        callback_context.state['target_language'] = config.target_language
        callback_context.state['current_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        callback_context.state['db_name'] = config.db_name
        db_manager = DatabaseManager(config.db_name)
        callback_context.state['available_tables'] = db_manager.table_schema
    return prepare_state_before_agent
