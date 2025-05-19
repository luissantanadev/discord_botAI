from OpenAi_API import openai_bot

def test_openai_bot_imported():
    assert openai_bot is not None, "openai_bot não foi importado corretamente"
