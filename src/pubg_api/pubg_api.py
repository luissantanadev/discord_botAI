import os
import requests

def buscar_dados_pubg(player_name):
    api_key = os.getenv("pubg_api_key")
    # 1. Buscar player_id
    url = f"https://api.pubg.com/shards/steam/players?filter[playerNames]={player_name}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.api+json"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return f"Erro ao buscar jogador: {resp.status_code} - {resp.text}"
    data = resp.json()
    if not data.get("data"):
        return "Jogador não encontrado."
    jogador = data["data"][0]
    player_id = jogador.get("id", None)
    nome = jogador.get("attributes", {}).get("name", "Desconhecido")

    # 2. Buscar temporada atual
    url_season = "https://api.pubg.com/shards/steam/seasons"
    resp_season = requests.get(url_season, headers=headers)
    if resp_season.status_code != 200:
        return f"Erro ao buscar temporada: {resp_season.status_code} - {resp_season.text}"
    data_season = resp_season.json()
    season_id = None
    for season in data_season.get("data", []):
        if season.get("attributes", {}).get("isCurrentSeason"):
            season_id = season.get("id")
            break
    if not season_id:
        return "Temporada atual não encontrada."

    # 3. Buscar estatísticas do jogador na temporada atual (endpoint correto)
    url_stats = f"https://api.pubg.com/shards/steam/players/{player_id}/seasons/{season_id}"
    resp_stats = requests.get(url_stats, headers=headers)
    if resp_stats.status_code != 200:
        return f"Erro ao buscar estatísticas: {resp_stats.status_code} - {resp_stats.text}"
    stats = resp_stats.json().get("data", {}).get("attributes", {}).get("gameModeStats", {})

    # 4. Extrair dados de modo SOLO, DUO e SQUAD
    modos = ["solo", "duo", "squad"]
    resposta = [f"📊 Estatísticas da temporada atual para {nome}:"]
    for modo in modos:
        modo_stats = stats.get(modo, {})
        partidas = modo_stats.get("roundsPlayed", 0)
        mortes = modo_stats.get("losses", 0)
        abates = modo_stats.get("kills", 0)
        nocautes = modo_stats.get("DBNOs", 0)
        colocacao_media = modo_stats.get("averageRank", 0)
        proporcao_mortes = modo_stats.get("killDeathRatio", 0)
        top10 = modo_stats.get("top10s", 0)
        vitorias = modo_stats.get("wins", 0)
        media_dano = modo_stats.get("damageDealt", 0)
        resposta.append(
            f"\n🔹 **{modo.upper()}**\n"
            f"Partidas: {partidas}\n"
            f"Mortes: {mortes}\n"
            f"Nocautes: {nocautes}\n"
            f"Abates: {abates}\n"
            f"Colocação média: {colocacao_media}\n"
            f"Proporção de mortes (K/D): {proporcao_mortes}\n"
            f"Top 10: {top10}\n"
            f"Vitórias: {vitorias}\n"
            f"Média de dano: {media_dano:.2f}"
        )
    return "\n".join(resposta)

if __name__ == "__main__":
    import json
    player_name = "ThanatosFull"
    api_key = os.getenv("pubg_api_key")
    url = f"https://api.pubg.com/shards/steam/players?filter[playerNames]={player_name}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.api+json"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"Erro ao buscar jogador: {resp.status_code} - {resp.text}")
        exit()
    data = resp.json()
    if not data.get("data"):
        print("Jogador não encontrado.")
        exit()
    jogador = data["data"][0]
    player_id = jogador.get("id", None)

    url_season = "https://api.pubg.com/shards/steam/seasons"
    resp_season = requests.get(url_season, headers=headers)
    if resp_season.status_code != 200:
        print(f"Erro ao buscar temporada: {resp_season.status_code} - {resp_season.text}")
        exit()
    data_season = resp_season.json()
    season_id = None
    for season in data_season.get("data", []):
        if season.get("attributes", {}).get("isCurrentSeason"):
            season_id = season.get("id")
            break
    if not season_id:
        print("Temporada atual não encontrada.")
        exit()

    url_stats = f"https://api.pubg.com/shards/steam/players/{player_id}/seasons/{season_id}"
    resp_stats = requests.get(url_stats, headers=headers)
    if resp_stats.status_code != 200:
        print(f"Erro ao buscar estatísticas: {resp_stats.status_code} - {resp_stats.text}")
        exit()
    print(json.dumps(resp_stats.json(), indent=2, ensure_ascii=False))