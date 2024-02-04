import os
import dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import HumanMessagePromptTemplate
from langchain.schema.messages import SystemMessage

import constants as c


def refine_transcript(transcript: str) -> str:
    concepts_list = load_file("./concepts.txt")
    people_list = load_file("./people.txt")
    system_prompt = c.COPY_EDITOR_PROMPT.format(people_list=people_list, concepts_list=concepts_list)

    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=(system_prompt)),
            HumanMessagePromptTemplate.from_template("{text}")
        ]
    )

    dotenv.load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name="gpt-4",
        temperature=0.0
    )

    print("AI: Copy-editing transcript...")
    response = llm(chat_template.format_messages(text=transcript))
    return response.content


def load_file(file_path):
    """Load custom vocabulary from a text file and return as a list."""
    with open(file_path, 'r') as f:
        return f.read().splitlines()


if __name__ == "__main__":
    transcript = """
    Hey, it's my first recording of the day. How am I doing? I've just had lunch. Today has been a very exciting day for me because of the progress I've made on Langchain and SQL. Yes. So I've been using Chains Agent that transforms natural language into SQL queries. And that's awesome. That's awesome. That's amazing. So I've been playing around with that and it works so well, and I have the codes now, and I wish to deeply understand it. And then I believe it's going to completely transform the Woolworths project. So really the next step action items, the next step action items is to integrate it into Streamlit. Into a deployed streamlit application. Yeah. Because the problem is I need to still configure a way. I need to understand how Streamlit puts their SQL connection in the secrets.toml file. I need to understand how that's done. But if I can find a way to run those queries from a deployed Streamlit application, that's a massive success. That's awesome. And it's a success particularly for the Woolworths project, the Barcode scanner project. Okay, now that's not my main priority. Right now. My main priority is a chat bot for Hetty and it's due tomorrow. So the minimum viable product right now is to build a Streamlit application that perhaps lets me upload files and ask questions of them. So that's all Llama index stuff and it could be Lang chain stuff. We will see how we go. There's a part of me that really wants, deeply wants to succeed with Llama index, because I want to understand Llama Index, and yes, I want to understand Llama Index. So, yeah, that's what I'm going to do. I'm going to go to the Streamlit documentation and I'm going to process through how they created a chat bot that accesses a body of research. And the minimum viable product right now is I'm going to simply query an already existing knowledge vault of files sent from Hetty, and I'm going to try and make that code modular if I can, such that I can then create an upload button where you can upload a file and it saves that to a vector database. And then allows me to query that vector database. So that's what I'm going to do. I'm going to process through the documentation and I hope I can get it done and make a success of it.
    """
    refined_transcript = refine_transcript(transcript)
    print(refined_transcript)

