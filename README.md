## Playlist importer from json to youtube

Here is a way to export from spotify to json: https://github.com/Doskii/Spotify-playlist-to-JSON  
(make sure to check the issue for liked song playlist)

This script, simply takes the output of the spotify to json one and creates a new youtube playlist for it

Good luck for using it tho, google developer api is a disaster

## How to use

1. Create a project in google cloud console
2. Create a test user for it, you'll get a downloadable json file, name it secret.json and put in this projetc's root dir
3. Make sure to enable youtube api
4. Put the json playlist file in ./playlists, change the var 'playlist_name' in main.py:main
5. Run the script

If everything goes well, you'll see a new (private) playlist on your yt channel containing the songs in your json playlist file

I hope I never have to work with any google api ever again.


## Thx to
  https://stackoverflow.com/questions/72029929/create-playlist-by-youtube-data-api-python  
  https://stackoverflow.com/questions/61702338/adding-multiple-videos-to-youtube-playlist-via-api-python (even tho it diddn't work)
