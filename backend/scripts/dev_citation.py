import re
from typing import List

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from chatbot.utils import _create_model_gemini


def get_llm() -> ChatGoogleGenerativeAI:
    return _create_model_gemini("gemini", temperature=0)


class Citation(BaseModel):

    start: int = Field(..., description="The starting sentence index of the citation.")
    end: int = Field(..., description="The esentence nding index of the citation.")


class Citations(BaseModel):
    citations: List[Citation] = Field(..., description="A list of citation ranges.")


class SplitText(BaseModel):
    text_id: str
    text: str
    sentences: List[str]

    def get_text_with_ids(self) -> str:
        """Returns the original text with sentence IDs prefixed."""
        result = ""
        for idx, sentence in enumerate(self.sentences):
            result += f"id {idx} : {sentence}\n"
        return result.strip()

    def get_cited_text(self, citations: Citations) -> List[str]:
        """Returns the text corresponding to the given citation."""
        cited_indices = set()
        for citation in citations.citations:
            for idx in range(citation.start, citation.end + 1):
                if 0 <= idx < len(self.sentences):
                    cited_indices.add(idx)
        return [self.sentences[idx] for idx in sorted(cited_indices)]


def split_text_by_sentences(text: str) -> List[str]:
    """Splits the input text into sentences based on periods."""
    # Split on sentence-ending punctuation, and also before each bullet or numbered bullet at the start of a line
    pattern = r"(?<=[.!?])\s+|(?<=:)\n\s*(?=-|\d+\.)"
    sentences = [s.strip() for s in re.split(pattern, text) if s.strip()]
    return sentences


def process(
    query: str, text_to_display: str, model: ChatGoogleGenerativeAI
) -> Citations:
    messages = [
        SystemMessage(
            content="You are an expert at identifying citations in text to answer a question. Analyze the question and the provided text and return the start and end indices of the sentences to be cited. Return them as a JSON array following the provided schema."
        ),
        HumanMessage(
            content=f"Here is a question: {query}.\nHere is the text from which you have to identify citations:\n{text_to_display}"
        ),
    ]
    response = model.with_structured_output(Citations).invoke(messages)
    if isinstance(response, Citations):
        return response
    else:
        return Citations.model_validate(response)


if __name__ == "__main__":
    text_id = "some-id"
    text = """Paris is the capital of France. It is known for the Eiffel Tower!
    In addition, it has a rich history dating back centuries. Many tourists visit every year.
    There are around 30 million visitors annually.
    Let's explore more about this beautiful city. Here are some interesting facts:
    - The Louvre is the world's largest art museum.
    - Notre-Dame Cathedral is a masterpiece of French Gothic architecture.
    - The Seine River flows through the heart of Paris."""

    sentences: List[str] = split_text_by_sentences(text)

    split_text = SplitText(text_id=text_id, text=text, sentences=sentences)

    text_to_display: str = split_text.get_text_with_ids()
    print(text_to_display)
    query: str = "What is the world's largest art museum?"
    res: Citations = process(query, text_to_display, get_llm())
    print(res)

    citations: List[str] = split_text.get_cited_text(res)
    for citation in citations:
        print(citation)
