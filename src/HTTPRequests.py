from requests.auth import HTTPBasicAuth
import requests
import json
import os

settings_path = os.path.join(os.path.dirname(__file__), '../settings.txt')
api_key_path = os.path.join(os.path.dirname(__file__), '../api_key.txt')
api_key_file = open(api_key_path, 'r')
api_key = api_key_file.read()
print(api_key)
headers = {'Accept': 'application/json'}

#TODO remove global
champion_ids = {}

#get most recent version
def get_version():
    url = 'https://ddragon.leagueoflegends.com/api/versions.json'
    response = requests.get(url, headers=headers)
    content = json.loads(response.content.decode('utf-8'))
    version = content[0]
    return version

#get list of champion ids
def get_champion_ids():
    url = 'http://ddragon.leagueoflegends.com/cdn/11.15.1/data/en_US/champion.json'
    response = requests.get(url, headers=headers)
    content = json.loads(response.content.decode('utf-8'))
    ids = {}
    champions = content['data']
    for champion in champions:
        id = champions[champion]['key']
        ids[id] = champion
    return ids

#get list of all current champions
def get_champion_names():
    url = 'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(get_version())
    response = requests.get(url, headers=headers)
    content = json.loads(response.content.decode('utf-8'))
    champions = content['data'].keys()
    return champions


#get detailed description for given champion
def get_champion_details(champion):
    url = 'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion/{}.json'.format(get_version(), champion)
    response = requests.get(url, headers=headers)
    content = json.loads(response.content.decode('utf-8'))
    detail = content['data'][champion]
    return detail

def get_champion_abilities(champion):
    detail = get_champion_details(champion)
    abilities = detail['spells']
    abilities.insert(0, detail['passive'])
    return abilities

#get encrypted summonerId by summoner name
def get_encrypted_summoner_id_by_name(name):
    url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'.format(name, api_key)
    response = requests.get(url, headers=headers)
    content = json.loads(response.content.decode('utf-8'))
    if 'id' in content:
        id = content['id']
        return id
    else:
        return None

#get champions in the current game
def get_current_game_champions(encrypted_summoner_id):
    global champion_ids
    url = 'https://na1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{}?api_key={}'.format(encrypted_summoner_id, api_key)
    response = requests.get(url, headers=headers)
    content = json.loads(response.content.decode('utf-8'))
    participants = content['participants']
    champions = []
    if not champion_ids:
        champion_ids = get_champion_ids()
    for participant in participants:
        champion_id = str(participant['championId'])
        if champion_id in champion_ids:
            champions.append(champion_ids[champion_id])
    return champions
