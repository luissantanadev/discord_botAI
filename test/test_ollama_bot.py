from ollama_bot.ollama_bot import ollama_bot

def test_ollama_bot_has_start():
    assert hasattr(ollama_bot, "start"), "ollama_bot não possui o método 'start'"
