from os import getenv
import sqlite3

from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from db_price import get_price

load_dotenv()


instruction = """
Тебя зовут Мария. Ты лучший консультант на СТО. У тебя отлично получается консультировать клиентов по ценам на услуги. 

Твой стиль:
- Отвечаешь на вопросы по услугам и ценам, используя только данные из предоставленного прайс-листа.
- Не придумываешь услуги и цены, которых нет в документе.
- Если информации не хватает, явно сообщаешь об этом без предложения альтернатив.
"""


USE_STUDIO = getenv("LANGGRAPH_STUDIO") == "1"
conn = sqlite3.connect("agent_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)


llm = ChatOpenAI(
    model="gpt-5-nano-2025-08-07",
    temperature=0.1,
    reasoning_effort="low",
)

kwargs = dict(
    model=llm,
    tools=[get_price],
    system_prompt=instruction,
)

if not USE_STUDIO:
    kwargs["checkpointer"] = SqliteSaver(conn) # type: ignore

agent = create_agent(**kwargs) # type: ignore


def ask(question: str):
    print(question)
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": "user_123"}},
    )

    for msg in reversed(result["messages"]):
        if msg.type == "ai":
            print(msg.content)
            return


if __name__ == "__main__":
    ask("Сколько стоит замена дизельного двигателя?")
    ask("А сколько это обычно по времени?")
