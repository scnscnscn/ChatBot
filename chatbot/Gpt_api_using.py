import openai

class GptAssistant:

    def __init__(self, api_key, api_base):
        self.client = openai.OpenAI(api_key=api_key, base_url=api_base)
        self.conversation_history = [
            {"role": "system", "content": "You are an AI assistant designed to engage in multi-turn conversations."}
        ]

    def chat(self, user_input):
        self.conversation_history.append({"role": "user", "content": user_input})
        try:
            response = self.client.chat.completions.create(model="yi-large", messages=self.conversation_history)
            ai_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            return ai_response
        except Exception as e:
            return f"Error: {e}"

