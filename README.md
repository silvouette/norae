# norae

## Todo
add more details and clean stuff, final styling.

## Desc
A web app that groups your saved tracks on spotify into separate playlist based on language by utilizing musixmatch API alongside Spotify's. Built with Python and Javascript.

![front page preview](https://github.com/silvouette/norae/blob/main/previews/frontpage.png)

The app will take the logged in user's last 20 saved tracks and get each track's lyrics from musixmatch and get the song's language based on language detection using textblob. The user will be sent to playlists page where the user can choose whether to save the language playlists to their spotify account. 

New playlist won't be created if the user already has a playlist with the same name in their spotify library, but instead will add new tracks from the list that aren't in the playlist yet. User will be notified if the same playlist with the same tracks already exists.

![playlists preview](https://github.com/silvouette/norae/blob/main/previews/playlists.png)

## Try the App
Clone this repo to your local directory and install the required packages in requirements.txt. 
Rename key_s.py to keys.py and provide your own user id, etc.
Export app.py as the flask app then enter 'flask run' on your terminal.

### credits
<a href='https://www.freepik.com/vectors/business'>front image</a>
