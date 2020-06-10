# Generate a playlist of all of an artists songs
import json
import requests

from spotify_secrets import spotify_token, spotify_user_id


class CreatePlaylist:
    def __init__(self):
        self.artist_name = ""
        self.all_song_info = {}

    def create_playlist(self):
        """
        This function creates a Spotify playlist
        """
        playlist_name = "All songs of " + self.artist_name
        # playlist name and description
        request_body = json.dumps({
            "name": playlist_name,
            "description": "Generated from software",
            "public": True
        })
        query = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Context-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = (response.json())
        return response_json["id"]

    def add_song_to_playlist(self):
        """
        This function calls create_playlist to create a Spotify playlist and then adds all tracks contained in
        all_song_info to the playlist.
        """
        uris = list(self.all_song_info.values())

        # Create new playlist
        playlist_id = self.create_playlist()

        # Add all songs into new playlist
        request_data = json.dumps(uris)

        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id
        )

        response = requests.post(
            query,
            data = request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        if response.status_code != 200:
            print(response.status_code)

        response_json = response.json()
        return response_json


    def get_artist_uri(self, name):
        """
        Given artist name, this function returns the uri of the artist
        The api search is pretty poor with returning the correct artist when given the name
        name -- artist name (string)
        Returns uri (string)
        """
        query = "https://api.spotify.com/v1/search?q=" + name + "{}&type=artist&offset=20&limit=2"
        response = requests.get(
            query,
            headers={
                "Context-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        artist_id = response_json["artists"]["items"][0]["id"]
        artist_name = response_json["artists"]["items"][0]["name"]
        self.artist_name = artist_name
        print("Entered name: " + name + "\nFound artist: " + artist_name + "\n" + "Artist id is: " + artist_id)
        return artist_id

    def get_artist_albums(self, id):
        """
        Given an artist id, this functon returns the ids of all albums the artist appears on.
        id -- artist id
        returns dictionary, keys are album names and values are album ids
        """
        album_dict = {}
        query = "https://api.spotify.com/v1/artists/" + id + "/albums"
        response = requests.get(
            query,
            headers={
                "Context-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        for album in response_json["items"]:
            name = album["name"]
            uri = album["uri"]
            # print(album["name"], " ", album["uri"])
            album_dict[name] = uri

        return album_dict

    def get_album_tracks(self, album):
        """
        Given the id of an album, this function returns the ids of the tracks in the album.
        album -- id of the album
        Returns dictionary, keys are track names and values are track uris
        """
        track_dict = {}
        query = "https://api.spotify.com/v1/albums/"+album+"/tracks"
        response = requests.get(
            query,
            headers={
                "Context-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        try:
            for track in response_json["items"]:
                name = track["name"]
                uri = track["uri"]
                #track_dict[name] = uri
                self.all_song_info[name] = uri
        except KeyError as e:
            print ("KeyError", str(e))
        #return track_dict



if __name__ == '__main__':
    ### NOTE: for sake of demonstration I'm just using Hozier's artist ID, the search functionality is pretty inaccurate
    ### Similarly, artist_name has been set to Hozier.
    ### To change songs added to playlist change lines 152 and 154 accordingly.
    cp = CreatePlaylist()

    # Retrieve id of artist
    # artist_id = cp.get_artist_uri("input()")
    cp.artist_name = "Hozier"
    # Retrieve all album names, uris for given artist id
    albums = cp.get_artist_albums("2FXC3k01G6Gw61bmprjgqS")

    # Retrieve all track names, track ids for every track in every album
    for album_name, album_uri in albums.items():
        cp.get_album_tracks(album_uri[14:])

    # Add all tracks to created playlist
    cp.add_song_to_playlist()

    # print(cp.all_song_info)


