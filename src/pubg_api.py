import os
import requests

def buscar_dados_pubg(player_name):
    api_key = os.getenv("pubg_api_key")
    url = f"https://api.pubg.com/shards/steam/players?filter[playerNames]={player_name}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.api+json"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("data"):
            return data["data"][0]  # Dados do jogador
        else:
            return "Jogador não encontrado."
    else:
        return f"Erro ao buscar dados: {resp.status_code} - {resp.text}"

# Exemplo de uso:
player_name = "LordThanatos"
dados = buscar_dados_pubg(player_name)
print(dados)