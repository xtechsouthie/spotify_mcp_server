from mcp.server.fastmcp import FastMCP
from ..auth import spotify_auth
from typing import List

def add_playback_tools(mcp: FastMCP):

    @mcp.tool()
    async def get_current_playback() -> str:
        """
        Get current users active device ID and currently playing song.
        """
        client = spotify_auth.get_client()
        if not client:
            return "Error with user authentication"
        
        try:
            playback = client.current_playback()
            result = ""
            if playback.get("device"):
                if playback["device"]["is_active"]:
                    device_id = playback["device"]["id"]
                    result += f"Current active device ID: '{device_id}'\n"
                else:
                    result += "No active device"

            if playback.get("item"):
                track = playback["item"]
                artists = ", ".join([artist["name"] for artist in track["artists"]])
                result += f"Current playback item: {track["name"]}, Artists: {artists}.\n"
            else:
                result += "No item in playback currently"
            
            return result
        except Exception as e:
            return f"Error in fetching current playback: {e}"
                
    @mcp.tool()
    async def pause_playback(device_id: str = None) -> str:
        """
        Pause user playback / currently playing item.

        Args:
            device_id: target device id for playback (default: None), if set to None, it will pause playback on the currently active device
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            response = client.pause_playback(device_id)
            return "Paused the playback on device"
        except Exception as e:
            return f"Error with pausing playback: {e}"
        
    @mcp.tool()
    async def next_track(device_id: str = None) -> str:
        """
        Skip user's playback to next track.

        Args:
            device_id: target device id for playback (default: None), if set to None, it will pause playback on the currently active device
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            response = client.next_track(device_id)
            return "Skipped to next track"
        except Exception as e:
            return f"Error with skipping to next track: {e}"
        
    @mcp.tool()
    async def previous_track(device_id: str = None) -> str: 
        """
        Changes user's playback to previous track.

        Args:
            device_id: target device id for playback (default: None), if set to None, it will pause playback on the currently active device
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            response = client.previous_track(device_id)
            return "Moved to previous track"
        except Exception as e:
            return f"Error with moving to previous track: {e}"
        
    @mcp.tool()
    async def get_queue() -> str:
        """
        Gets the current user's queue
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            queue = client.queue()
            result = "Current queue: \n\n"
            if queue.get("currently_playing"):
                track = queue["currently_playing"]
                artists = ", ".join([artist["name"] for artist in track["artists"]])
                result += f"Now playing: {track["name"]}, Artists: {artists}, URI: '{track["uri"]}'.\n\n"

            if queue.get("queue"):
                result += "UP NEXT: \n"
                for i, track in enumerate(queue["queue"][:50], 1):
                    artists = ", ".join([artist["name"] for artist in track["artists"]])
                    result += f"{i}. Track: {track["name"]}, Artists: {artists}, URI: '{track["uri"]}'.\n"
            else:
                result += "Queue is empty"

            return result
        except Exception as e:
            return f"Error with getting queue: {e}"
        

    @mcp.tool()
    async def start_playback(device_id: str = None, context_uri: str = None, uris: List[str] = None, offset: dict = None) -> str:
        """
        Start or resume user's playback.

        Args:
            device_id: target device id for playback (default: None), if set to None, it will pause playback on the currently active device
            context_uri:  spotify URI of the context to play (album, artist, playlist) (its optional)
            uris: list of spotify track URIs to play (optional)
            offset: indicates from where in the context playback should start (optional)
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            kwargs = {}
            if device_id:
                kwargs['device_id'] = device_id
            if context_uri:
                kwargs['context_uri'] = context_uri
            if uris:
                kwargs['uris'] = uris
            if offset:
                kwargs['offset'] = offset
            
            response = client.start_playback(**kwargs)

            if context_uri:
                return f"started playback from context: {context_uri}"
            elif uris:
                return f"started playback with {len(uris)} tracks"
            else:
                return "Resumed playback"
                
        except Exception as e:
            return f"Error with starting playback: {e}"
        
    @mcp.tool()
    async def resume_playback(device_id: str = None) -> str:
        """
        Resume the paused playback.

        Args:
            device_id: target device id for playback (default: None), if set to None, it will pause playback on the currently active device
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            response = client.start_playback(device_id=device_id)
            return "Resumed playback"
        except Exception as e:
            return f"Error with resuming playback: {e}"
        
    @mcp.tool()
    async def add_to_queue(uri: str, device_id: str = None) -> str:
        """
        Add song to the queue of the user.

        Args:
            uri: song uri, id, or url
            device_id: target device id for playback (default: None), if set to None, it will pause playback on the currently active device
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            response = client.add_to_queue(uri=uri, device_id=device_id)
            return "Song added to queue"
        except Exception as e:
            return f"Error in adding song to queue: {e}"
        
    
        