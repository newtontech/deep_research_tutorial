from typing import Optional

from google.adk.agents import LlmAgent

from .prompt import instructions_v2_zh, instructions_v2_en
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse

from ...tools.io import save_llm_request


def save_response(callback_context: CallbackContext, llm_response: LlmResponse) -> None:
    """save llm response to file"""
    if llm_response.content.parts[0].text:
        original_text = llm_response.content.parts[0].text
        print(f"response:{original_text}")
        with open("response.md", "w", encoding="utf-8") as f:
            f.write(f"response: {original_text}")


def update_invoke_message(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    """save llm request to file"""
    output_file = "llm_contents_report.json"
    save_llm_request(llm_request, output_file)


def init_report_agent(config):
    """Initialize the researcher agent with the given configuration."""
    # Select the model based on the configuration
    selected_model = config.gemini_2_5_pro
    # selected_model = config.gpt_4o

    root_agent = LlmAgent(
        name="report_agent",
        model=selected_model,
        instruction=instructions_v2_en,
        description="Merge results from multiple paper agents in parallel and generate a deep research literature report.",
        output_key="deep_research_report",
        before_model_callback=update_invoke_message,
        after_model_callback=save_response
    )
    return root_agent
