from app import app
from flask import render_template, flash, redirect, url_for, request, json, jsonify
from authlib.flask.client import OAuth
import simple_logger
import requests
from config import spotify_id,spotify_secret
class Tokens():
    expires_at = ""
    refresh_token = ""
    token_type = ""
    access_token = ""
    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type=self.token_type,
            refresh_token=self.refresh_token,
            expires_at=self.expires_at
        )

class Users():
    token = None

class ids():
    device_id = ""
    access_token = ""
    devicelist = {}


def update_token(name, token):
    if Users.token is not None:
        Users.token = None
    Users.token = token
    return Users.token
logs = simple_logger.log_handling("Main", 'logs.log')
oauth = OAuth(app, update_token=update_token)
oauth.init_app(app)

oauth.register('spotify',
        client_id = spotify_id,
        client_secret = spotify_secret,
        api_base_url = 'https://api.spotify.com/v1/',
        access_token_url = 'https://accounts.spotify.com/api/token',
        authorize_url = 'https://accounts.spotify.com/authorize',
        client_kwargs = {'scope': 'user-modify-playback-state user-read-currently-playing user-read-playback-state'},
)


@app.route("/login")
def login_page():
    redirect_uri = url_for('callback', _external=True)
    return oauth.spotify.authorize_redirect(redirect_uri)


@app.route("/home")
def home():
    return redirect(url_for('main_view'))


@app.route("/callback")
def callback():
    client = oauth.create_client('spotify')
    token = client.authorize_access_token(client_secret=client.client_secret)
    resp = client.get('me/player/devices').json()
    ids.access_token = token['access_token']
    Users.token = token
    ids.devicelist=resp['devices']
    return render_template('select_device.html', devices=resp['devices'])


@app.route('/devices/<device_id>')
def set_device(device_id):
    ids.device_id = device_id
    endpoint = "https://api.spotify.com/v1/me/player"
    headers = {"authorization": "Bearer " + Users.token['access_token'] + ""}
    data = { 'device_ids': []}
    data['device_ids'].append(device_id)
    json_data = json.dumps(data)
    resp = requests.put(endpoint,data=json_data,headers=headers)
    return redirect(url_for('main_view'))


@app.route('/devices')
@app.route('/device')
def list_device():
    client = oauth.create_client('spotify')
    resp = client.get('me/player/devices',token=Users.token).json()
    return render_template('select_device.html', devices=resp['devices'])


@app.route('/main')
def main_view():
    return render_template('main.html')



@app.route("/play")
def play():
    if Users.token is None:
        return redirect(url_for('login_page'))
    endpoint = "https://api.spotify.com/v1/me/player/play?device_id"+ids.device_id
    headers = {"authorization": "Bearer " + Users.token['access_token'] + ""}
    resp = requests.put(endpoint,headers=headers)
    return redirect(url_for('main_view'))


@app.route("/play/<song_uri>")
def play_uri(song_uri):
    if Users.token is None:
        return redirect(url_for('login_page'))
    endpoint = "https://api.spotify.com/v1/me/player/play?device_id"+ids.device_id
    headers = {"authorization": "Bearer " + Users.token['access_token'] + ""}
    data = { 'uris': []}
    data['uris'].append(song_uri)

    json_data = json.dumps(data)

    resp = requests.put(endpoint,data=json_data,headers=headers)
    return redirect(url_for('main_view'))


@app.route('/stop')
@app.route('/pause')
def pause_playback():
    if Users.token is None:
        return redirect(url_for('login_page'))
    endpoint = "https://api.spotify.com/v1/me/player/pause?device_id"+ids.device_id
    headers = {"authorization": "Bearer " + Users.token['access_token'] + ""}
    resp = requests.put(endpoint,headers=headers)
    return redirect(url_for('main_view'))


@app.route("/playlist/<song_uri>")
def playlist(song_uri):
    if Users.token is None:
        return redirect(url_for('login_page'))
    endpoint = "https://api.spotify.com/v1/me/player/play?device_id"+ids.device_id
    headers = {"authorization": "Bearer " + Users.token['access_token'] + ""}
    data = {}
    data['context_uri'] = song_uri
    json_data = json.dumps(data)
    resp = requests.put(endpoint,data=json_data,headers=headers)
    return redirect(url_for('main_view'))


@app.route('/next')
def skip():
    if Users.token is None:
        return redirect(url_for('login_page'))
    endpoint = "https://api.spotify.com/v1/me/player/next?device_id"+ids.device_id
    headers = {"authorization": "Bearer " + Users.token['access_token'] + ""}
    resp = requests.post(endpoint,headers=headers)
    return redirect(url_for('main_view'))


@app.route('/prev')
def prev():
    if Users.token is None:
        return redirect(url_for('login_page'))
    endpoint = "https://api.spotify.com/v1/me/player/previous?device_id"+ids.device_id
    headers = {"authorization": "Bearer " + Users.token['access_token'] + ""}
    resp = requests.post(endpoint,headers=headers)
    return redirect(url_for('main_view'))

@app.route('/volume/<volume_level>')
def set_volume(volume_level):
    if Users.token is None:
        return redirect(url_for('login_page'))
    endpoint = "https://api.spotify.com/v1/me/player/volume?device_id"+ids.device_id+"?volume_percent="+volume_level
    headers = {"authorization": "Bearer " + Users.token['access_token'] + ""}
    resp = requests.put(endpoint,headers=headers)
    return redirect(url_for('main_view'))


@app.route('/status')
def server_status():
    status_data = {}
    if Users.token is None:
        status_data['logged_in'] = "False"
    else:
        status_data['logged_in'] = "True"
        client = oauth.create_client('spotify')
        resp = client.get('me/player',token=Users.token).json()
        device = resp['device']
        status_data['device'] = device
        logs.debug(status_data)
    return status_data