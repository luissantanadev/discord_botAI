import os
import openai

class OpenAIBot:
    def __init__(self, model="gpt-3.5-turbo"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY não encontrado no ambiente.")
        openai.api_key = self.api_key
        self.model = model

    def ask(self, prompt, temperature=0.7, max_tokens=512):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Erro ao consultar OpenAI: {e}"

# Exemplo de uso:
# bot = OpenAIBot()
# resposta = bot.ask("Explique o que é uma API.")
# print(resposta)
