import getpass
import os
import requests
from dotenv import load_dotenv, set_key
from langchain_huggingface import HuggingFaceEndpoint
import asyncio
from langchain_core.messages import AIMessage, HumanMessage
import json


class History:
    def __init__(self, session_id: str) -> None:
        self.session_id = session_id
        self.__messages = []

    def add_user_message(self, message: str):
        self.__messages.append(HumanMessage(content=message))

    def add_ai_message(self, message: str):
        self.__messages.append(AIMessage(content=message))

    def get_messages(self) -> list[AIMessage | HumanMessage]:
        return self.__messages


class Search:
    def __init__(self, env_file: str = ".env"):
        self.__env_file = env_file
        load_dotenv(self.__env_file)
        self.__saper_api_key = self.__getAPIKey(var="SAPER_API_KEY")

        self.url = "https://google.serper.dev/search"
        self.headers = {
            "X-API-KEY": self.__saper_api_key,
            "Content-Type": "application/json",
        }

    def __getAPIKey(self, var: str = None) -> str:
        if not var:
            raise ValueError("The environment variable is not correctly indicated")

        api_key = os.environ.get(var)

        if not api_key:
            api_key = getpass.getpass(f'Enter {var.split("_")}: ')
            os.environ[var] = api_key
            set_key(self.__env_file, var, api_key)

        return api_key

    def request(self, keywords) -> dict:
        payload = json.dumps({"q": keywords, "limit": 3, "page": 1})

        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload
        )

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {"Error": f"{response.status_code}, {response.text}", "organic": []}


class ChatBot:
    __llm: HuggingFaceEndpoint = None
    __history: History = None
    __search: Search = None

    def __init__(self, env_file: str = ".env") -> None:
        self.__env_file = env_file
        load_dotenv(self.__env_file)
        self.__huggingface_api_key = self.__getAPIKey(var="HUGGINGFACEHUB_API_KEY")

        self.__initModel(model="microsoft/Phi-3-mini-4k-instruct")

    def __getAPIKey(self, var: str = None) -> str:
        if not var:
            raise ValueError("The environment variable is not correctly indicated")

        api_key = os.environ.get(var)

        if not api_key:
            api_key = getpass.getpass(f'Enter {var.split("_")}: ')
            os.environ[var] = api_key
            set_key(self.__env_file, var, api_key)

        return api_key

    def __initModel(self, model: str = "gpt2"):
        self.__history = History(session_id="user_123")
        self.__search = Search()

        self.__llm = HuggingFaceEndpoint(
            repo_id=model,
            task="text-generation",
            max_new_tokens=100,
            do_sample=True,
            repetition_penalty=1.03,
            huggingfacehub_api_token=self.__huggingface_api_key,
            streaming=True,
            verbose=True,
        )

    async def __request(self, prompt: str):
        search_response = "\n".join(
            [
                f"RRESULT NUMBER {i}: TITLE: {result['title']}; LINK: {result['link']}; SNIPPET: {result['snippet']}"
                for i, result in enumerate(
                    self.__search.request(keywords=prompt)["organic"]
                )
            ]
        )
        chat_history = "\n".join(
            [
                (
                    f"User: {msg.content}"
                    if isinstance(msg, HumanMessage)
                    else f"AI: {msg.content}"
                )
                for msg in self.__history.get_messages()
            ]
        )

        full_prompt = f"Chat history (USER and AI): {chat_history}\n\nUser's new prompt: {prompt}\n\nSearch results: {search_response}\n\nCONDITION: Respond to the user's new prompt based on the search results and the chat history. If there is no useful information in the history or search results, respond directly to the prompt."
        self.__history.add_user_message(prompt)

        response = self.__llm.stream(input=full_prompt)
        save_response = ""
        print("\nAI: ")
        for chunk in response:
            save_response += chunk
            print(chunk, end="")

        self.__history.add_ai_message(save_response)

    def runSession(self):
        asyncio.run(self.__runAsyncron())

    async def __runAsyncron(self):
        while True:
            await self.__request(prompt=input("\nEnter your prompt: "))


if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.runSession()
