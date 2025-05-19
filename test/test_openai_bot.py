from OpenAi_API import openai_bot

def test_openai_bot_has_start():
    assert hasattr(openai_bot, "start"), "openai_bot não possui o método 'start'"
