from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import HumanMessage

text = "你好"
messages = [HumanMessage(content=text)]

llm = ChatOpenAI(openai_api_key="xxx", openai_api_base="")

print(llm(messages))
