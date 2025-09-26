from mcp.server.fastmcp import FastMCP
from ..auth import spotify_auth
from typing import Literal

def add_search_tools(mcp: FastMCP):

    @mcp.tool()
    async def search_spotify(query: str, search_type: Literal["track", "artist", "album", "playlist", "all"] = "all", limit: int = 10) -> str:
        """
        Search spotify for any content type

        Args:
            query: Search query 
            search_type: What to search for - track, artist, album, playlist or all (default = all)
            limit: number of results to be shown (default = 10)
        """

        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            if search_type == "all":
                api_types = "track,artist,album,playlist"
            else:
                api_types = search_type
            
            results = client.search(q=query, type=api_types, limit=limit)
            result = f"Search results for '{query}':\n\n"

            for result_type in api_types.split(','):
                items = results[f"{result_type}s"]["items"]

                if not items:
                    continue

                headers = {
                    "track": "TRACKS:\n",
                    "artist": "ARTISTS:\n", 
                    "album": "ALBUMS:\n",
                    "playlist": "PLAYLISTS:\n"
                }

                result += f"{headers[result_type]}"

                for i, item in enumerate(items ,1):
                    if result_type == "track":
                        artists = ", ".join([artist['name'] for artist in item['artists']])
                        result += f"{i}. Track: {item['name']}, Artists: {artists}, URI: '{item['uri']}'\n"
                        
                    elif result_type == "artist":
                        followers = item['followers']['total']
                        result += f"{i}. Artist: {item['name']} ({followers:,} followers), URI: '{item['uri']}'\n"
                        
                    elif result_type == "album":
                        artists = ", ".join([artist['name'] for artist in item['artists']])
                        result += f"{i}. Album: {item['name']}, Artists: {artists}, URI: '{item['uri']}'\n"
                        
                    elif result_type == "playlist":
                        owner = item['owner']['display_name']
                        result += f"{i}. {item['name']} by {owner}, URI: '{item['uri']}', ID: '{item["id"]}'\n"

                result += "\n"

            return result if result.strip() != f"Search results for '{query}':" else f"No results found for '{query}'"
        
        except Exception as e:
            return f"Error while searching: {e}"