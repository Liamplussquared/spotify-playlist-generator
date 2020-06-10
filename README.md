# spotify-playlist-generator
Given the name and id of an artist, this app generates a Spotify playlist containing all tracks from their albums. <br/>

### Update spotify_secrets
**_spotify_token_** should contain an oauth token, which can be found here: <br/>
https://developer.spotify.com/console/post-playlists/?user_id=&body=%7B%22name%22%3A%22New%20Playlist%22%2C%22description%22%3A%22New%20playlist%20description%22%2C%22public%22%3Afalse%7D
<br/>
**_spotify_id_** is just your account ID. <br/>

### Requirements 
Only depencencies are on the requests and json libraries. <br/>
`pip install requests` <br/>
`pip install json` 
