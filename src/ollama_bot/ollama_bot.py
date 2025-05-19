import discord
import asyncio
from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama
import requests
import re

class OllamaBot:
    def __init__(self):
        load_dotenv()
        self.DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
        if not self.DISCORD_TOKEN:
            raise EnvironmentError("❌ DISCORD_TOKEN não definido no .env!")
        self.llm = ChatOllama(model="llama3.2")
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.historico = {}  # Novo: armazena histórico por usuário
        self._setup_events()

    def conversar_com_ollama(self, pergunta):
        try:
            resposta = self.llm.invoke(pergunta)
            if hasattr(resposta, 'content'):
                return resposta.content
            return str(resposta)
        except Exception as e:
            print(f"[ERRO] Falha ao conectar com Ollama: {e}")
            return f"Erro ao conectar com Ollama: {e}"

    async def conversar_com_ollama_async(self, pergunta):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.conversar_com_ollama, pergunta)

    def buscar_na_web(self, query):
        api_key = os.getenv("SERPAPI_KEY")
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "num": 5
        }
        resp = requests.get(url, params=params)
        data = resp.json()
        resultados = []
        for item in data.get("organic_results", []):
            titulo = item.get('title', '')
            link = item.get('link', '')
            snippet = item.get('snippet', '')
            resultados.append(f"{titulo}\n{snippet}\n{link}")
        return "\n\n".join(resultados) if resultados else "Nenhum resultado encontrado."

    def precisa_buscar_na_web(self, pergunta, resposta):
        # Frases típicas de desconhecimento
        frases_desconhecimento = [
            "não sei", "não tenho essa informação", "não possuo dados", "não posso responder", "não encontrei", "não tenho certeza",
            "não tenho acesso a informações", "não posso ajudar", "não sei dizer", "não tenho conhecimento", "não tenho dados",
            "não tenho informações", "não tenho certeza sobre isso", "não tenho acesso a essa informação", "não posso fornecer essa informação","não posso responder a isso", "não posso ajudar com isso"
        ]
        resposta_baixa = resposta.lower()
        if any(frase in resposta_baixa for frase in frases_desconhecimento):
            return True
        # Detecta perguntas com datas, nomes próprios ou eventos (simples)
        if re.search(r"\b(202\d|202[0-9]|hoje|ontem|amanhã|ano|mês|presidente|cotação|preço|valor|quem|quando|onde|como)\b", pergunta.lower()):
            return True
        return False

    def montar_prompt_com_resultados(self, resultados, pergunta):
        return (
            f"Contexto da web:\n{resultados}\n\n"
            f"Pergunta: {pergunta}\n"
            f"Responda usando apenas as informações acima. "
            f"Seja objetivo, cite as fontes se possível e responda no mesmo idioma da pergunta."
        )

    def _setup_events(self):
        @self.client.event
        async def on_ready():
            print(f'🤖 Bot conectado como {self.client.user}')
            # Criar canal de texto "chat-com-ia" se não existir
            for guild in self.client.guilds:
                canal_nome = "chat-com-ia"
                canal_existente = discord.utils.get(guild.text_channels, name=canal_nome)
                if not canal_existente:
                    await guild.create_text_channel(canal_nome)

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            if not hasattr(message.channel, "name") or message.channel.name != "chat-com-ia":
                await message.channel.send("💡 Por favor, converse com o Flok no canal #chat-com-ia.")
                return

            pergunta = message.content.strip()
            if not pergunta:
                await message.channel.send("❓ Envie uma mensagem com sua pergunta.")
                return

            user_id = str(message.author.id)
            historico_usuario = self.historico.get(user_id, "")

            # Monta o prompt com o histórico + nova pergunta
            prompt = (
                f"Histórico da conversa:\n{historico_usuario}\n"
                f"Usuário: {pergunta}\n"
                f"Responda no mesmo idioma da pergunta."
            )
            resposta = await self.conversar_com_ollama_async(prompt)

            # Decide se precisa buscar na web
            if self.precisa_buscar_na_web(pergunta, resposta):
                resultados = self.buscar_na_web(pergunta)
                prompt = self.montar_prompt_com_resultados(resultados, pergunta)
                resposta = await self.conversar_com_ollama_async(prompt)

            # Atualiza o histórico do usuário
            novo_historico = historico_usuario + f"\nUsuário: {pergunta}\nFlok: {resposta}\n"
            self.historico[user_id] = novo_historico[-4000:]  # Limita o histórico para não ficar muito grande

            embed = discord.Embed(
                title=f"🧠 Resposta do Flok",
                description=resposta[:4000],
                color=discord.Color.blue()
            )

            await message.channel.send(embed=embed)

    def start(self):
        self.client.run(self.DISCORD_TOKEN)
        print("Bot iniciado!")

# Instância global para compatibilidade
ollama_bot = OllamaBot()
