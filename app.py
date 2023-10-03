import autogen
import yfinance as yf
from datetime import date, datetime

# Configurations for AutoGen API
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={"model": ["gpt-4", "gpt-4-0314", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"]},
)

# Defining the AssistantAgent
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "temperature": 0,
        "request_timeout": 600,
        "seed": 42,
        "model": "gpt-4-0613",
        "config_list": autogen.config_list_openai_aoai(exclude="aoai"),
    }
)

# Defining the UserProxyAgent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "planning"},
)

# Function to get stock information
def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        historical_data = stock.history(period="1d")
        return historical_data['Close'][0]
    except Exception as e:
        print(e)
        return None

# Ultimate Chatbot class that integrates all features
class UltimateChatbot:
    def __init__(self, assistant, user_proxy):
        self.assistant = assistant
        self.user_proxy = user_proxy
        self.assistant_state = None

    def save_assistant_state(self):
        self.assistant_state = self.assistant.save_state()

    def load_assistant_state(self):
        if self.assistant_state:
            self.assistant.restore_state(self.assistant_state)

    def dynamic_converse(self, query):
        response = self.assistant.generate_code(query)
        return response

    def learn_from_interaction(self, query, feedback):
        self.assistant.learn(query, feedback)

    def ultimate_response(self, query, feedback=None):
        response = self.dynamic_converse(query)
        if feedback:
            self.learn_from_interaction(query, feedback)

        # Check if the response is a code snippet
        if isinstance(response, str) and response.startswith("```"):
            try:
                output = exec(response, globals(), locals())
                return output
            except Exception as e:
                print(e)
                return response
        else:
            return response

# Instantiating the Ultimate Chatbot
ultimate_chatbot = UltimateChatbot(assistant, user_proxy)

# Loading the assistant's state
ultimate_chatbot.load_assistant_state()

# The Final Dialogue - Engaging with the Ultimate Chatbot
while True:
    query = input("You: ")
    if query.lower() == 'exit':
        print("Ultimate Chatbot: Farewell, esteemed enchanter!")
        break

    response = ultimate_chatbot.ultimate_response(query)
    print("Ultimate Chatbot:", response)

# Saving the assistant's state
ultimate_chatbot.save_assistant_state()
