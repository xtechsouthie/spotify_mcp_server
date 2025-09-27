from mcp.server.fastmcp import FastMCP
from ..auth import spotify_auth
from typing import List

def add_playlist_tools(mcp: FastMCP):

    @mcp.tool()
    async def get_user_playlist(limit: int = 20) -> str:
        """
        Get current user's followed and owned spotify playlist

        Args:
            limit: Number of playlists to retrive (default = 20)
        """
        client = spotify_auth.get_client()
        if not client:
            return "Error with user authentication"
        
        try:
            playlists = client.current_user_playlists(limit=limit)

            result = f"Found total of {playlists["total"]} playlists. \n\n"

            for playlist in playlists["items"]:
                result += f"Playlist Name: {playlist["name"]}, Total tracks in this playlist: {playlist["tracks"]["total"]} tracks.\n"
                result += f"ID of the playlist: '{playlist["id"]}'\n---\n"
            return result
        except Exception as e:
            return f"Error in fetching playists: {e}"
    
    @mcp.tool()
    async def get_playlist_id_by_name(name: str, limit: int = 50) -> str:
        """
        Find the ID of the playlist given the name.

        Args:
            name: Name of the playlist to search for
            limit: Number of playlists limit in user's playlist to match search for (default = 50),
                    if playlist is not found, try increasing limit to increase search size
        """
        client = spotify_auth.get_client()
        if not client:
            return "Error with user authentication"
        
        try:
            playlists = client.current_user_playlists(limit=limit)
            
            result = ""
            for playlist in playlists["items"]:
                if name.lower() in playlist["name"].lower():
                    result += f"found playlist: {playlist["name"]} with ID: `{playlist["id"]}`\n"
            
            if not result:
                return f"no matching playlist found matching with {name}"
            return result
        except Exception as e:
            return f"Error searching playlist: {e}"
        
    @mcp.tool()
    async def get_playlist_tracks(playlist_id: str, limit: int = 50) -> str:
        """
        Get tracks from a specific playlist.
        
        Args:
            playlist_id: spotify playlist ID
            limit: limit on number of tracks to retrive (default = 50)
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            tracks = client.playlist_tracks(playlist_id, limit=limit)
            playlist_info = client.playlist(playlist_id)

            result = f"Playlist name: {playlist_info["name"]}\n"
            result += f"Playlist description: {playlist_info["description"]}\n---\n"

            result += f"Playlist Tracks:\n---\n"

            for i, item in enumerate(tracks["items"], 1):
                track = item["track"]
                if track:
                    artists = ", ".join([artist["name"] for artist in track["artists"]])
                    uri = track["uri"]
                    result += f"{i}. Track: {track["name"]}, Artists: {artists}, Track URI: '{uri}'.\n"

            return result
        except Exception as e:
            return f"Error in retriving tracks from album : {e}"
        
    @mcp.tool()
    async def create_playlists(name: str, description: str = "", public: bool = True) -> str:
        """
        Create a new playlist.

        Args:
            name: name of the playlist
            description: playlist discription (optional)
            public: whether the playlist should be public (default = True)
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            user = client.current_user()
            playlist = client.user_playlist_create(user["id"], name=name, description=description, public=public)
            return f"Created playlist with NAME: {name},  ID: {playlist["id"]}"
        except Exception as e:
            return f"Error while creating playlist: {e}"
    
    @mcp.tool()
    async def get_current_users_playlists(limit: int = 50, offset: int = 0) -> str:
        """
        Get the playlist's of the current user

        Args:
            limit: maximum number of items to return (default: 50) (Maximum value: 50)
            offset: the index of the first item to return (default: 0)
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            user = client.current_user()
            playlists = client.user_playlists(user["id"], limit, offset) #this dosent retun owned playlist
            result = ""
            for i, playlist in enumerate(playlists["items"], 1):
                result += f"{i}. Playlist Name: {playlist["name"]}, Playlist Description: {playlist["description"]}, Playlist ID: '{playlist["id"]}'.\n"
            if not result:
                return f"User has no playlists."
            return result
        except Exception as e:
            return f"Error fetching user playlist: {e}"

    @mcp.tool()
    async def get_users_owned_playlist(user_id: str, limit: int = 50, offset: int = 0) -> str:
        """
        Get the playlist's owned by an user, i.e. the playlists he can edit

        Args:
            user_id: user id of the user
            limit: maximum number of items to return (default: 50) (Maximum value: 50)
            offset: the index of the first item to return (default: 0)
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            playlists = client.user_playlists(user_id, limit, offset)
            current_user = client.current_user()
            current_user_id = current_user["id"]

            owned_playlists = []
            for p in playlists['items']:
                if playlist['owner']['id'] == current_user_id:
                    owned_playlists.append(p)
            
            if not owned_playlists:
                return f"User has no playlists."

            result = ""
            for i, playlist in enumerate(owned_playlists["items"], 1):
                result += f"{i}. Playlist Name: {playlist["name"]}, Playlist Description: {playlist["description"]}, Playlist ID: '{playlist["id"]}'.\n"

            total = playlists["total"]
            if offset < (total - limit):
                result += f"Try changing offset if you dont find the desired playlist, current offset: {offset}, total playlists: {total}, current limit: {limit}"
            return result
        except Exception as e:
            return f"Error fetching user playlist: {e}"

    @mcp.tool()
    async def playlist_add_items(playlist_id: str, items: List[str], position: int = None) -> str:
        """
        Add tracks or episodes to a spotify playlist.

        Args:
            playlist_id: the id of the spotify playlist to add items to
            items: a list of track/episode URIs or URLs
            position: the position in the playlist you want to add the item (default = None (it will add in the end))
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            playlist = client.playlist_add_items(playlist_id, items, position)
            return f"Successfully added items to playlist. Playlist snapshot id: {playlist["snapshot_id"]}"
        except Exception as e:
            return f"Error adding items to playlist: {e}"
        
    
    @mcp.tool()
    async def playlist_remove_items(playlist_id: str, items: List[str], snapshot_id: str = None) -> str:
        """
        Remove tracks or episodes from a given spotify playlist

        Args:
            playlist_id: id of playlist to remove items from
            items: a list of track/episode URIs or URLs
            snapshot_id: optional id of playlist snapshot (default: None)
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            playlist = client.playlist_remove_all_occurrences_of_items(playlist_id, items, snapshot_id)
            return f"Successfully removed items from playlist. Playlist snapshot id: {playlist["snapshot_id"]}"
        except Exception as e:
            return f"Error removing items from playlist: {e}"
        
    
        
