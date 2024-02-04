import os, dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import constants as c

dotenv.load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

class Interactions(BaseModel):
    """A class to represent interactions between people within a text."""
    people: list[str] | None = Field(description="A list of all the people mentioned in the text. If no persons are mentioned, return None.")
    interactions: list[str] | None = Field(description="A list of descriptions of the context in which the people are mentioned in the text. If no interactions take place, return None.")

def create_md_file(file_name, date, content):
    with open(f"./interactions/{file_name}.md", "w") as f:
        f.write("---\n")
        f.write(f"date: {date}\n")
        f.write("---\n\n")
        f.write(brackets)

def highlight_people_in_interactions(interactions, people):
    """Surround occurrences of people's names with double square brackets."""
    highlighted_interactions = []
    for interaction in interactions:
        for person in people:
            interaction = interaction.replace(person, f"[[{person}]]")
        highlighted_interactions.append(interaction)
    return highlighted_interactions


def extract_interactions(transcript, people_list):
    llm = ChatOpenAI(openai_api_key=c.OPENAI_API_KEY, model_name=c.OPENAI_MODEL)
    parser = PydanticOutputParser(pydantic_object=Interactions)

    message = HumanMessagePromptTemplate.from_template(template=c.INTERACTION_EXTRACTION_PROMPT)
    chat_prompt = ChatPromptTemplate.from_messages(messages=[message])

    chat_prompt_with_values = chat_prompt.format_prompt(
        people_list=people_list,
        transcript=transcript,
        format_instructions=parser.get_format_instructions(),
    )

    response = llm(chat_prompt_with_values.to_messages())
    interactions = parser.parse(response.content)
    return interactions

people_list = ['Hettie Brittz', 'Hettie', 'Mama V', 'Lerey', 'Thembani', 'Renate', 'ArjanCodes', 'James Briggs', 'Ciaran', 'Marcel', 'Charise', 'Douw', 'Oselu', 'Gustav', 'Dan Shipper']
date = "2023-11-02"

with open("./stations/station-3--polished-transcripts/Transcript 20231103232429.md", "r") as f:
    transcript = f.read()
interactions = extract_interactions(transcript, people_list)
print(interactions)

if interactions.people is not None:
    for person in interactions.people:
        print(f"[[{person}]]")

if interactions.interactions is not None:
    interactions_w_brackets = highlight_people_in_interactions(
        interactions.interactions, 
        interactions.people
    )
    for i, inter in enumerate(interactions_w_brackets):
        create_md_file(interactions.interactions[i], date, inter)


