from pathlib import Path
from typing import TypedDict, Optional
from dotenv import load_dotenv


# Load .env from the same directory as this script, else from project root
def locate_dot_env_file() -> Path:
    return Path(__file__).parent / ".env" if (Path(__file__).parent / ".env").exists() else Path(__file__).parent.parent / ".env"


env_path = locate_dot_env_file()
load_dotenv(dotenv_path=env_path)

from langchain_litellm import ChatLiteLLM
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    appraisal_result: Optional[str]
    messages: list

# Initialize the LLM via LiteLLM pointing to SAP Generative AI Hub
model = ChatLiteLLM(model="sap/gemini-2.5-flash-lite", temperature=0)

system_prompt = """You are an experienced Stolen Goods Loss Appraiser specializing in fine art and valuables.
Your goal is to assess the value of stolen items and provide a professional insurance appraisal report.
You provide detailed assessments based on your expertise and rely strictly on evidence — you never guess values."""

def appraiser_node(state: AgentState) -> dict:
    response = model.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content="Provide a brief explanation of how an insurance appraiser would approach assessing stolen artwork and valuables."),
    ])

    appraisal_result = response.content

    return {
        "appraisal_result": appraisal_result,
        "messages": state["messages"] + [{"role": "assistant", "content": appraisal_result}],
    }

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("appraiser", appraiser_node)
    workflow.add_edge(START, "appraiser")
    workflow.add_edge("appraiser", END)

    return workflow.compile()


def main():
    app = build_graph()

    result = app.invoke({
        "appraisal_result": None,
        "messages": [],
    })

    print("\n" + "="*50)
    print("Insurance Appraiser Report:")
    print("="*50)
    print(result["appraisal_result"])


if __name__ == "__main__":
    main()
