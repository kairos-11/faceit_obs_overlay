from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests
import time
from obswebsocket import obsws, requests as obs_requests
import threading
import json, os

app = Flask(__name__, static_folder="../frontend")
CORS(app)

# Constants
API_KEY = "f3e9b199-425a-4c6d-8dd7-8a447566ee42"
PLAYER_NICKNAME = "DJ_SNIP"
OBS_HOST = "localhost"
OBS_PORT = 4455
OBS_PASSWORD = "EOKYunCgKTn5KjlG"
ELO_DATA_FILE = "elo_data.json"

BASE_URL = "https://open.faceit.com/data/v4"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

# OBS WebSocket setup
ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)

@app.route('/base-stats', methods=['GET'])
def base_stats():
    stats = get_player_stats(PLAYER_NICKNAME)
    return jsonify(stats)

@app.route('/last-match', methods=['GET'])
def last_match():
    match_stats = get_last_match_stat(PLAYER_NICKNAME)
    return jsonify(match_stats)

@app.route('/', methods=['GET'])
def serve_frontend():
    return send_from_directory("../frontend", "index.html")

@app.route('/images/<filename>')
def serve_images(filename):
    return send_from_directory("../backend/images", filename)

def get_player_stats(nickname):
    player_response = requests.get(f"{BASE_URL}/players?nickname={nickname}", headers=HEADERS)
    player_data = player_response.json()
    stats_response = requests.get(f"{BASE_URL}/players/{player_data['player_id']}/stats/cs2", headers=HEADERS)
    stats_data = stats_response.json()
    lifetime_stats = stats_data.get("lifetime", {})
    kd = lifetime_stats["Average K/D Ratio"]
    wr = lifetime_stats["Win Rate %"]
    hs = lifetime_stats['Average Headshots %']
    return {
        "nickname": nickname,
        "elo": player_data["games"]["cs2"]["faceit_elo"],
        "level": player_data["games"]["cs2"]["skill_level"],
        "kd": kd,
        "wr": wr,
        "hs": hs,
    }

def save_previous_elo(elo):
    with open(ELO_DATA_FILE, "w") as file:
        json.dump({"previous_elo": elo}, file)

def load_previous_elo():
    if not os.path.exists(ELO_DATA_FILE):
        return None
    with open(ELO_DATA_FILE, "r") as file:
        data = json.load(file)
        return data.get("previous_elo")

def calculate_elo_delta(current_elo, previous_elo):
    if previous_elo is None:
        return 0  # No previous data, assume no delta
    return current_elo - previous_elo


def get_last_match_stat(nickname):
    player_response = requests.get(f"{BASE_URL}/players?nickname={nickname}", headers=HEADERS)
    player_data = player_response.json()
    match_response = requests.get(f"{BASE_URL}/players/{player_data['player_id']}/history?game=cs2", headers=HEADERS)
    match_data = match_response.json()
    current_match = match_data["items"][0]
    match_id = current_match["match_id"]
    match_stats = requests.get(f"{BASE_URL}/matches/{match_id}/stats", headers=HEADERS).json()
    return_dict = {}
    for team in match_stats['rounds'][0]['teams']:
        for player in team['players']:
            if player['nickname'] == nickname:
                return_dict = player['player_stats']
                break
    overall_stats = get_player_stats(nickname)
    return_dict["nickname"] = overall_stats["nickname"]
    return_dict["elo"] = overall_stats["elo"]
    return_dict["level"] = overall_stats["level"]

    previous_elo = load_previous_elo()
    elo_delta = calculate_elo_delta(overall_stats["elo"], previous_elo)
    return_dict["elo_delta"] = elo_delta

    save_previous_elo(overall_stats["elo"])
    return return_dict


def monitor_new_matches(nickname):
    previous_game_count = len(get_player_history(nickname))
    trigger_obs_overlay()

    while True:
        time.sleep(5)

        current_game_count = len(get_player_history(nickname))
        if current_game_count > previous_game_count:
            previous_game_count = current_game_count
            trigger_obs_overlay()

def get_player_history(nickname):
    player_response = requests.get(f"{BASE_URL}/players?nickname={nickname}", headers=HEADERS)
    player_data = player_response.json()
    match_response = requests.get(f"{BASE_URL}/players/{player_data['player_id']}/history?game=cs2", headers=HEADERS)
    return match_response.json()["items"]

def trigger_obs_overlay():
    try:

        #stats = get_last_match_stat(PLAYER_NICKNAME)
        #print(f"Refreshed stats: {stats}")

        ws.connect()
        print("Connected to OBS WebSocket")


        scene_items = ws.call(obs_requests.GetSceneItemList(sceneName="Scene"))
        overlay_item = next(item for item in scene_items.getSceneItems() if item["sourceName"] == "Overlay")


        ws.call(obs_requests.SetSceneItemEnabled(sceneName="Scene", sceneItemId=overlay_item["sceneItemId"], sceneItemEnabled=True))
        print("Overlay enabled")

        time.sleep(20)

        ws.call(obs_requests.SetSceneItemEnabled(sceneName="Scene", sceneItemId=overlay_item["sceneItemId"], sceneItemEnabled=False))
        print("Overlay disabled")

        ws.disconnect()
    except Exception as e:
        print(f"OBS ERROR: {e}")



if __name__ == "__main__":
    # Start the Flask app in a separate thread (without debug mode)
    flask_thread = threading.Thread(target=lambda: app.run(debug=False, use_reloader=False), daemon=True)
    flask_thread.start()

    # Start monitoring matches in the main thread
    monitor_new_matches(PLAYER_NICKNAME)
