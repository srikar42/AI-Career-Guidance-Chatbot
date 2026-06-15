from dotenv import load_dotenv
import warnings
import os

from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import LLMChain

warnings.filterwarnings("ignore")

# Load Environment Variables
load_dotenv()

# Memory
memory = ConversationBufferMemory(
    memory_key='history',
    return_messages=True
)

# Read Prompt Template
with open('prompts/career_template.txt', 'r', encoding='utf-8') as file:
    prompt_template = file.read()

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ('system', prompt_template),
    MessagesPlaceholder(variable_name='history'),
    ('human', '{input}')
])

# Gemini Model
llm = GoogleGenerativeAI(
    model='gemini-2.5-flash-lite',
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Chain
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory
)

# Response Function
def get_response(user_input):

    result = chain.invoke({
        'input': user_input
    })

    return result['text']