import requests
import json

token = (
    "BQBmBqQKpezRq09pdJnHPN9uTuPQLK2NUcWzq5x53cxA9OsIkNi3dgtDfO-21tHpmqTdTBg_BDXm0G-K8WdqjibKyXJsTcm7yP4VCZYP4S-xUC_vY20EvJDnH08YdG-4tTKjsigZ5pkHo6lAjec83QrHf0YakAIN7uE0kG8sEQ-xNQwVH2NHcliNypWELSzVNgjxCu41p-DIi_RvPl10f4wfwkk0tUiV9K8V3vN0jPPbNW7T4g6xa6oS7O0mFcXOXBF-0Q3AcqgvSUtA"
)

user_id = "12134345639"
playlist_id = "48AowSPhgf7anhWlZvaGwd"

playlist_path = f"users/{user_id}/playlists/{playlist_id}/tracks"
# auth = (
#     "https://accounts.spotify.com/authorize"
#     "?client_id=264cae2f027f4108a507a659563ae92b"
#     "&redirect_uri=https:%2F%2Frequestb.in%2F1jipura1"
#     "&scope=user-library-read%20playlist-read-private%20playlist-modify-public%20playlist-modify-private"
#     "&response_type=token"
# )
# print(auth)

def get_spotify(path, method="GET", params=None, data=None):
    params = params or {}
    root = "https://api.spotify.com/v1/"
    headers = {
        "Authorization": f'Bearer {token}',
        "Content-Type": "application/json",
    }

    attributes = {
        "headers": headers,
        "params": params,
        "data": data,
    }

    if not data:
        del attributes['data']

    if not params:
        del attributes['params']

    resp = requests.request(
        method,
        root + path,
        **attributes
    )

    if resp.status_code > 299:
        import pdb; pdb.set_trace()
        raise Exception(resp.content)
    return resp


def get_100_tracks():
    resp = get_spotify("me/tracks", params={"limit": "50"}).json()
    tracks = resp['items']
    resp = get_spotify(
        "me/tracks", params={"limit": "50", "offset": "50"}).json()
    return tracks + resp['items']


def add_tracks():
    tracks = []

    for track in get_100_tracks():
        uri = track['track']['uri']
        tracks.append(uri)

    get_spotify(playlist_path, method="POST", data=json.dumps({
        'uris': tracks,
    }))


def delete_playlist_tracks():
    tracks = get_spotify(playlist_path).json()['items']
    uris = list(map(lambda x: x['track']['uri'], tracks))
    get_spotify(playlist_path, method="DELETE", data=json.dumps({
        'uris': uris,
    }))

delete_playlist_tracks()
add_tracks()


import pdb; pdb.set_trace()


