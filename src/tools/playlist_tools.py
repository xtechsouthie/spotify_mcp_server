from mcp.server.fastmcp import FastMCP
from ..auth import spotify_auth

def add_playlist_tools(mcp: FastMCP):

    @mcp.tool()
    async def get_user_playlist(limit: int = 20) -> str:
        """
        Get user's spotify playlist

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
                result += f"ID of the playlist: `{playlist['id']}`\n---\n"
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
                    result += f"{i}. Track: {track["name"]}, Artists: {artists}.\n"

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
