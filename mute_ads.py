import sys
import time
import json
import socket
import webbrowser
from requests_oauthlib import OAuth2Session

from secret import *

# platform-based code
platform = sys.platform
if platform == "win32":
    from win.win_sound import WinSound
elif platform == "darwin":
    from mac.mac_sound import MacSound
    from mac import mac_util
elif platform == "linux":
    from linux.linux_sound import LinuxSound


redirect_uri = "https://open.spotify.com"
authorization_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
currently_playing_url = "https://api.spotify.com/v1/me/player/currently-playing"
devices_url = "https://api.spotify.com/v1/me/player/devices"
scope = ["user-read-currently-playing", "user-read-playback-state"]
curr_token = ""
extra = {
    "client_id": client_id,
    "client_secret": client_secret
}


# authorization functions
def get_auth_token(client): 
    auth_url, state = client.authorization_url(authorization_url)
    webbrowser.open(auth_url)
    authorization_response = input("Paste redirect url here: ")
 
    token = client.fetch_token(token_url, client_secret=client_secret, authorization_response=authorization_response)
    return token
def store_token_info(token):
    with open("token.json", "w") as data:
        json.dump(token, data)
def get_stored_token_info():
    with open("token.json") as json_file:
        data = json_file.read()
        if data == "\{\}" or data == "":
            return {}
        return json.loads(data)
def set_info(token):
    curr_token = str(token["access_token"])
    store_token_info(token)


# win and mac muting
def os_mute():
    if platform == "win32" and not WinSound.is_muted():
        WinSound.mute()
    elif platform == "darwin":
        MacSound.mute()
def os_unmute():
    if platform == "win32" and WinSound.is_muted():
        WinSound.mute()
    elif platform == "darwin":
        MacSound.unmute()


def main():
    # creates a token.json file if it does not exist
    open("token.json", "a").close()

    token_info = get_stored_token_info()
    spotify = OAuth2Session(client_id, 
                        redirect_uri=redirect_uri,
                        scope=scope, 
                        token=token_info,
                        auto_refresh_url=token_url,
                        auto_refresh_kwargs=extra,
                        token_updater=store_token_info)

    if token_info == {}:
        set_info(get_auth_token(spotify))
        token_info = get_stored_token_info()
    count = 0

    while True:

        # check if Spotify is playing from this device
        if count % 3 == 0: # every 3 seconds, it checks the devices (only for desktop app currently)
            response = spotify.get(devices_url, headers={"Authorization": "Bearer " + curr_token})   
            status = response.status_code 
            if status == 200:
                response_info = response.json()

                # get host name
                hostname = ""
                if platform == "win32":
                    hostname = socket.gethostname().lower()
                elif platform == "darwin":
                    hostname = mac_util.get_computername().lower()

                foundDevice = False
                for device in response_info["devices"]:
                    if device["name"].lower() == hostname or device["name"][:10] == "Web Player":
                        foundDevice = True
                        break
                if not foundDevice:
                    print("Spotify is not open on this device.")
                    break
            else:
                print(response)
                break
        count += 1


        # get currently playing
        response = spotify.get(currently_playing_url + "?market=US", headers={"Authorization": "Bearer " + curr_token})
        status = response.status_code
    
        if status == 204: # no content found
            os_unmute()
            print("No music is being played or paused at the moment.")
            input("Play something and return to begin running...")
            continue
        elif status == 200: # okay
            result = response.json()
            playing_type = result["currently_playing_type"]
            if playing_type == "ad":
                os_mute()
            elif playing_type == "track":
                os_unmute()
        else: # error?
            print(response)
            break

        # avoids sending too many requests    
        time.sleep(1.5)


if __name__ == "__main__":
    main()
