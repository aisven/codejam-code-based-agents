from pathlib import Path
from typing import TypedDict, Optional
from dotenv import load_dotenv
from gen_ai_hub.proxy.native.sap.client import RPTClient
import json


# Load .env from the same directory as this script, else from project root
def locate_dot_env_file() -> Path:
    return Path(__file__).parent / ".env" if (Path(__file__).parent / ".env").exists() else Path(__file__).parent.parent / ".env"


env_path = locate_dot_env_file()
load_dotenv(dotenv_path=env_path)


from langchain_litellm import ChatLiteLLM
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END


# Initialize RPT-1 client after loading environment variables
rpt1_client = RPTClient()


class AgentState(TypedDict):
    appraisal_result: Optional[str]
    messages: list


# Payload data for stolen items appraisal
payload = {
    "prediction_config": {
        "target_columns": [
            {
                "name": "INSURANCE_VALUE",
                "prediction_placeholder": "[PREDICT]",
                "task_type": "regression",
            },
            {
                "name": "ITEM_CATEGORY",
                "prediction_placeholder": "[PREDICT]",
                "task_type": "classification",
            },
        ]
    },
    "index_column": "ITEM_ID",
    "rows": [
        {
            "ITEM_ID": "ART_001",
            "ITEM_NAME": "Water Lilies - Series 1",
            "ARTIST": "Claude Monet",
            "ACQUISITION_DATE": "1987-03-15",
            "INSURANCE_VALUE": 45000000,
            "ITEM_CATEGORY": "Painting",
            "DIMENSIONS": "200x180cm",
            "CONDITION_SCORE": 9,
            "RARITY_SCORE": 9,
            "PROVENANCE_CLARITY": 8,
        },
        {
            "ITEM_ID": "ART_002",
            "ITEM_NAME": "Japanese Bridge at Giverny",
            "ARTIST": "Claude Monet",
            "ACQUISITION_DATE": "1995-06-22",
            "INSURANCE_VALUE": 42000000,
            "ITEM_CATEGORY": "Painting",
            "DIMENSIONS": "92x73cm",
            "CONDITION_SCORE": 8,
            "RARITY_SCORE": 8,
            "PROVENANCE_CLARITY": 9,
        },
        {
            "ITEM_ID": "ART_003",
            "ITEM_NAME": "Irises",
            "ARTIST": "Vincent van Gogh",
            "ACQUISITION_DATE": "2001-11-08",
            "INSURANCE_VALUE": "[PREDICT]",
            "ITEM_CATEGORY": "Painting",
            "DIMENSIONS": "71x93cm",
            "CONDITION_SCORE": 7,
            "RARITY_SCORE": 9,
            "PROVENANCE_CLARITY": 8,
        },
        {
            "ITEM_ID": "ART_004",
            "ITEM_NAME": "Starry Night Over the Rhone",
            "ARTIST": "Vincent van Gogh",
            "ACQUISITION_DATE": "1998-09-14",
            "INSURANCE_VALUE": 48000000,
            "ITEM_CATEGORY": "Painting",
            "DIMENSIONS": "73x92cm",
            "CONDITION_SCORE": 8,
            "RARITY_SCORE": 9,
            "PROVENANCE_CLARITY": 9,
        },
        {
            "ITEM_ID": "ART_005",
            "ITEM_NAME": "The Birth of Venus",
            "ARTIST": "Sandro Botticelli",
            "ACQUISITION_DATE": "1992-04-30",
            "INSURANCE_VALUE": 55000000,
            "ITEM_CATEGORY": "Painting",
            "DIMENSIONS": "172x278cm",
            "CONDITION_SCORE": 6,
            "RARITY_SCORE": 10,
            "PROVENANCE_CLARITY": 10,
        },
        {
            "ITEM_ID": "ART_006",
            "ITEM_NAME": "Primavera",
            "ARTIST": "Sandro Botticelli",
            "ACQUISITION_DATE": "1989-02-19",
            "INSURANCE_VALUE": 52000000,
            "ITEM_CATEGORY": "Painting",
            "DIMENSIONS": "203x314cm",
            "CONDITION_SCORE": 7,
            "RARITY_SCORE": 10,
            "PROVENANCE_CLARITY": 10,
        },
        {
            "ITEM_ID": "ART_007",
            "ITEM_NAME": "Girl with a Pearl Earring",
            "ARTIST": "Johannes Vermeer",
            "ACQUISITION_DATE": "2003-07-11",
            "INSURANCE_VALUE": "[PREDICT]",
            "ITEM_CATEGORY": "Painting",
            "DIMENSIONS": "44x39cm",
            "CONDITION_SCORE": 8,
            "RARITY_SCORE": 10,
            "PROVENANCE_CLARITY": 9,
        },
        {
            "ITEM_ID": "ART_008",
            "ITEM_NAME": "The Music Lesson",
            "ARTIST": "Johannes Vermeer",
            "ACQUISITION_DATE": "1994-05-20",
            "INSURANCE_VALUE": 38000000,
            "ITEM_CATEGORY": "Painting",
            "DIMENSIONS": "64x73cm",
            "CONDITION_SCORE": 8,
            "RARITY_SCORE": 9,
            "PROVENANCE_CLARITY": 9,
        },
        {
            "ITEM_ID": "ART_009",
            "ITEM_NAME": "The Persistence of Memory",
            "ARTIST": "Salvador Dalí",
            "ACQUISITION_DATE": "2005-03-10",
            "INSURANCE_VALUE": 35000000,
            "ITEM_CATEGORY": "[PREDICT]",
            "DIMENSIONS": "24x33cm",
            "CONDITION_SCORE": 9,
            "RARITY_SCORE": 9,
            "PROVENANCE_CLARITY": 10,
        },
        {
            "ITEM_ID": "ART_010",
            "ITEM_NAME": "Metamorphosis of Narcissus",
            "ARTIST": "Salvador Dalí",
            "ACQUISITION_DATE": "1996-08-12",
            "INSURANCE_VALUE": 32000000,
            "ITEM_CATEGORY": "Painting",
            "DIMENSIONS": "51x78cm",
            "CONDITION_SCORE": 8,
            "RARITY_SCORE": 8,
            "PROVENANCE_CLARITY": 8,
        },
        {
            "ITEM_ID": "ART_011",
            "ITEM_NAME": "The Bronze Dancer",
            "ARTIST": "Auguste Rodin",
            "ACQUISITION_DATE": "1991-07-22",
            "INSURANCE_VALUE": 8500000,
            "ITEM_CATEGORY": "Sculpture",
            "DIMENSIONS": "Height: 1.8m",
            "CONDITION_SCORE": 9,
            "RARITY_SCORE": 7,
            "PROVENANCE_CLARITY": 8,
        },
        {
            "ITEM_ID": "ART_012",
            "ITEM_NAME": "The Thinker",
            "ARTIST": "Auguste Rodin",
            "ACQUISITION_DATE": "2000-11-05",
            "INSURANCE_VALUE": "[PREDICT]",
            "ITEM_CATEGORY": "Sculpture",
            "DIMENSIONS": "Height: 1.9m",
            "CONDITION_SCORE": 9,
            "RARITY_SCORE": 7,
            "PROVENANCE_CLARITY": 9,
        },
        {
            "ITEM_ID": "ART_013",
            "ITEM_NAME": "Hope Diamond Replica - Royal Cut",
            "ARTIST": "Unknown Jeweler",
            "ACQUISITION_DATE": "1988-02-19",
            "INSURANCE_VALUE": 12000000,
            "ITEM_CATEGORY": "Jewelry",
            "DIMENSIONS": "Width: 15cm",
            "CONDITION_SCORE": 10,
            "RARITY_SCORE": 10,
            "PROVENANCE_CLARITY": 7,
        },
        {
            "ITEM_ID": "ART_014",
            "ITEM_NAME": "Cartier Ruby Necklace - 1920s",
            "ARTIST": "Cartier",
            "ACQUISITION_DATE": "2002-09-11",
            "INSURANCE_VALUE": 9500000,
            "ITEM_CATEGORY": "Jewelry",
            "DIMENSIONS": "Length: 45cm",
            "CONDITION_SCORE": 9,
            "RARITY_SCORE": 8,
            "PROVENANCE_CLARITY": 9,
        },
    ],
    "data_schema": {
        "ITEM_ID": {"dtype": "string"},
        "ITEM_NAME": {"dtype": "string"},
        "ARTIST": {"dtype": "string"},
        "ACQUISITION_DATE": {"dtype": "date"},
        "INSURANCE_VALUE": {"dtype": "numeric"},
        "ITEM_CATEGORY": {"dtype": "string", "categories": ["Painting", "Sculpture", "Jewelry"]},
        "DIMENSIONS": {"dtype": "string"},
        "CONDITION_SCORE": {"dtype": "numeric", "range": [1, 10], "description": "1=Poor to 10=Pristine"},
        "RARITY_SCORE": {"dtype": "numeric", "range": [1, 10], "description": "1=Common to 10=Extremely Rare"},
        "PROVENANCE_CLARITY": {"dtype": "numeric", "range": [1, 10], "description": "1=Unknown to 10=Perfect Documentation"},
    },
}


def call_rpt1(payload: dict) -> str:
    """Call the SAP RPT-1 model to predict missing insurance values and item categories."""
    try:
        response = rpt1_client.predict(body=payload, model_name="sap-rpt-1-large")
        if response:
            return json.dumps(response.model_dump(), indent=2)
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error calling RPT-1: {str(e)}"


# Initialize the LLM via LiteLLM pointing to SAP Generative AI Hub
model = ChatLiteLLM(model="sap/amazon--nova-pro", temperature=0)

system_prompt = """You are an experienced Stolen Goods Loss Appraiser specializing in fine art and valuables.
Your goal is to assess the value of stolen items and provide a professional insurance appraisal report.
You receive predictions from RPT-1 and turn them into a clear appraisal summary — you never guess values yourself."""


def appraiser_node(state: AgentState) -> dict:
    print("\n🔍 Appraiser Agent starting...")

    rpt1_result = call_rpt1(payload)

    response = model.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Here are the RPT-1 predictions for the stolen items. Write a professional appraisal summary:\n\n{rpt1_result}"),
        ]
    )

    appraisal_result = response.content
    print("✅ Appraisal complete")

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

    result = app.invoke(
        {
            "appraisal_result": None,
            "messages": [],
        }
    )

    print("\n" + "=" * 50)
    print("Insurance Appraiser Report:")
    print("=" * 50)
    print(result["appraisal_result"])


if __name__ == "__main__":
    main()
