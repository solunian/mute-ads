import sys
import time
import json
import webbrowser
from requests_oauthlib import OAuth2Session


client_id = "fc6b57cc09ef4b98b4ae24ca1cd5a0c1"
client_secret = "cede8e4646944cc6b7d3888375314e07"
redirect_uri = "https://open.spotify.com"
authorization_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
endpoint_url = "https://api.spotify.com/v1/me/player/currently-playing"
scope = ["user-read-currently-playing"]
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


# os based code
os = sys.platform
if os == "win32":
    from winsound.win_sound import WinSound
elif os == "darwin":
    from mac_sound import MacSound
def os_mute():
    if os == "win32" and not WinSound.is_muted():
        WinSound.mute()
    elif os == "darwin":
        MacSound.mute()
def os_unmute():
    if os == "win32" and WinSound.is_muted():
        WinSound.mute()
    elif os == "darwin":
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


    while True:    
        temp = spotify.get(endpoint_url + "?market=US", headers={"Authorization": "Bearer " + curr_token})
        status = temp.status_code
    
        if status == 204: # no content found
            os_unmute()
            print("No music is being played or paused at the moment.")
            input("Play something and return to begin running...")
            continue
        elif status == 200: # okay
            result = temp.json()
            playing_type = result["currently_playing_type"]
            if playing_type == "ad":
                os_mute()
            elif playing_type == "track":
                os_unmute()
        else: # error?
            print(temp)
            break

        # avoids sending too many requests    
        time.sleep(0.5)


if __name__ == "__main__":
    main()
