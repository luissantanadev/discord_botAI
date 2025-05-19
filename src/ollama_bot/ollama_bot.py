import discord
import asyncio
from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama

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

    def _setup_events(self):
        @self.client.event
        async def on_ready():
            print(f'🤖 Bot conectado como {self.client.user}')

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            comandos_validos = ("!flok", "!flok,", "!flok:", "!flok ")
            msg = message.content.strip()
            msg_lower = msg.lower()

            if msg_lower.startswith(comandos_validos):
                for comando in comandos_validos:
                    if msg_lower.startswith(comando):
                        pergunta = msg[len(comando):].strip()
                        break

                if not pergunta:
                    await message.channel.send("❓ Envie uma pergunta após `!Flok`.")
                    return

                await message.channel.send(f"🧠 {message.author.display_name} perguntou: `{pergunta}`\n🤔 Pensando...")

                resposta = await self.conversar_com_ollama_async(pergunta)

                embed = discord.Embed(
                    title=f"🧠 Resposta do Flok",
                    description=resposta[:4000],
                    color=discord.Color.blue()
                )

                # Procurar por uma thread já existente com o nome do usuário
                thread_nome = f"🧠 {message.author.display_name}"
                thread_existente = None
                for thread in message.channel.threads:
                    if thread.name == thread_nome and not thread.archived:
                        thread_existente = thread
                        break

                if thread_existente is None:
                    # Criar nova thread se não existir
                    thread_existente = await message.channel.create_thread(
                        name=thread_nome,
                        message=message
                    )

                await thread_existente.send(embed=embed)

                try:
                    await message.author.send(f"📬 Resposta do Flok para sua pergunta: `{pergunta}`", embed=embed)
                except discord.Forbidden:
                    await message.channel.send("⚠️ Não consegui enviar a resposta por DM (talvez esteja desativado).")

    def start(self):
        self.client.run(self.DISCORD_TOKEN)
        print("Bot iniciado!")

# Instância global para compatibilidade
ollama_bot = OllamaBot()
