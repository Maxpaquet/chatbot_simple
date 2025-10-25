import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from chatbot.utils import get_model
from pydantic import BaseModel, Field
from datetime import date
from pathlib import Path
import base64
from langchain_core.messages import HumanMessage, SystemMessage

HERE = Path(__file__).parent


class Compte(BaseModel):
    description: str = Field(..., description="Description du compte")
    date_time: str = Field(..., description="Date du compte")
    amount: float = Field(..., description="Montant du compte")

    def __str__(self):
        # Format with fixed width for alignment
        return f"{self.description:<40}: Date={self.date_time:<15}, Amount={self.amount:>10.2f}"


class BalanceSheet(BaseModel):
    accounts: list[Compte] = Field(..., description="Liste des comptes du bilan")

    def __str__(self):
        accounts_str = "\n".join("  " + str(account) for account in self.accounts)
        return f"BalanceSheet(accounts=[\n{accounts_str}\n])"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def main(image_path):

    llm: ChatGoogleGenerativeAI = get_model("gemini-pro", temperature=0.0)
    llm_structure = llm.with_structured_output(BalanceSheet)

    base64_image = encode_image(image_path)
    message = SystemMessage(
        content="You are an expert for extracting accounts from balance sheet."
    )
    user_message = HumanMessage(
        content=[
            {"type": "text", "text": "describe the weather in this image"},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
            },
        ]
    )
    res = llm_structure.invoke([message, user_message])
    print(res)


if __name__ == "__main__":
    image_path = f"{HERE}/../images/balance-sheet.png"
    main(image_path)
