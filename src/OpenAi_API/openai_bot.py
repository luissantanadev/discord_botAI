import discord
import asyncio
from dotenv import load_dotenv
import os
import openai

class OpenAIBot:
    def __init__(self, model="gpt-3.5-turbo"):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY não encontrado no ambiente.")
        self.model = model
        self.DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self._setup_events()

    def perguntar_openai(self, prompt, temperature=0.7, max_tokens=512):
        try:
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[ERRO] Falha ao conectar com OpenAI: {e}")
            return f"Erro ao consultar OpenAI: {e}"

    async def perguntar_openai_async(self, prompt, temperature=0.7, max_tokens=512):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.perguntar_openai, prompt, temperature, max_tokens)

    def _setup_events(self):
        @self.client.event
        async def on_ready():
            print(f'🤖 OpenAIBot conectado como {self.client.user}')

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            comandos_validos = ("!openai", "!openai,", "!openai:", "!openai ")
            msg = message.content.strip()
            msg_lower = msg.lower()

            if msg_lower.startswith(comandos_validos):
                for comando in comandos_validos:
                    if msg_lower.startswith(comando):
                        pergunta = msg[len(comando):].strip()
                        break

                if not pergunta:
                    await message.channel.send("❓ Envie uma pergunta após `!openai`.")
                    return

                await message.channel.send(f"🤖 {message.author.display_name} perguntou: `{pergunta}`\n🤔 Pensando...")

                resposta = await self.perguntar_openai_async(pergunta)

                embed = discord.Embed(
                    title=f"🤖 Resposta do OpenAI",
                    description=resposta[:4000],
                    color=discord.Color.green()
                )

                # Procurar por uma thread já existente com o nome do usuário
                thread_nome = f"🤖 {message.author.display_name}"
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
                    await message.author.send(f"📬 Resposta do OpenAI para sua pergunta: `{pergunta}`", embed=embed)
                except discord.Forbidden:
                    await message.channel.send("⚠️ Não consegui enviar a resposta por DM (talvez esteja desativado).")

    def start(self):
        self.client.run(self.DISCORD_TOKEN)
        print("OpenAIBot iniciado!")

# Instância global para compatibilidade
openai_bot = OpenAIBot()
