import discord
import asyncio
from dotenv import load_dotenv
import os
from langchain_community.chat_models import ChatOllama

# Carregar variáveis de ambiente
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

if not DISCORD_TOKEN:
    raise EnvironmentError("❌ DISCORD_TOKEN não definido no .env!")

# Inicializar modelo do Ollama
llm = ChatOllama(model="llama3.2")

# Inicializar cliente do Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Função para conversar com a IA
def conversar_com_ollama(pergunta):
    try:
        resposta = llm.invoke(pergunta)
        if hasattr(resposta, 'content'):
            return resposta.content
        return str(resposta)
    except Exception as e:
        print(f"[ERRO] Falha ao conectar com Ollama: {e}")
        return f"Erro ao conectar com Ollama: {e}"

async def conversar_com_ollama_async(pergunta):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, conversar_com_ollama, pergunta)

@client.event
async def on_ready():
    print(f'🤖 Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
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

        resposta = await conversar_com_ollama_async(pergunta)

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

def start():
    # Iniciar o bot
    client.run(DISCORD_TOKEN)
    print("Bot iniciado!")
