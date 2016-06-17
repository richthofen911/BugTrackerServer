# my id: 43310476, lm's id: 43585380
import requests
import json


my_api_key = 'b7a22f82-b9d6-491a-9f10-b4446e228fa4'
url_base = 'https://na.api.pvp.net'

api_summoner = '/api/lol/%s/v1.4/summoner/by-name/%s'  # {region}, {summonerNames}
api_current_game = '/observer-mode/rest/consumer/getSpectatorGameInfo/%s/%s'  # {platformId}, {summonerId}


def call_api(api, *params):
    api_filled = api % (params)
    response = requests.get(url_base + api_filled + '?api_key=' + my_api_key)
    return response.text.encode('ascii', 'ignore')

current_game_json = call_api(api_summoner, 'NA1', '43310476')
participants = json.loads(current_game_json)
