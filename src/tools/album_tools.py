from mcp.server.fastmcp import FastMCP
from ..auth import spotify_auth

def add_album_tools(mcp: FastMCP):

    @mcp.tool()
    async def get_album(album_id: str, market: str = None) -> str:
        """
        Gets album details (Name, Tracks(name, URI and ID), Artists and Release date) by album ID

        Args:
            album_id: the album ID, URI or URL
            market: an ISO 3166-1 alpha-2 country code (default: None)
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try: 
            album = client.album(album_id, market)
            result = "Spotify album: \n"
            if album:
                result += f"Album Name: {album["name"]}, Release Date: {album["release_date"]}\n"
                artists = ", ".join([artist["name"] for artist in album["artists"]])
                result += f"Album URI: {album["uri"]}, Album ID: {album["id"]}\n"
                result += f"Artists: {artists}\n\n"
                tracks = album["tracks"]
                result += "Tracks: \n"
                for i, track in enumerate(tracks["items"], 1):
                    artists = ", ".join([artist["name"] for artist in track["artists"]])
                    result += f"{i}. Track: {track["name"]}, Artists: {artists}, ID: '{track["id"]}', URI: '{track["uri"]}'.\n"
            else:
                result += "No album with given ID exists."
            
            return result
        except Exception as e:
            return f"Error fetching album: {e}"
        
    @mcp.tool()
    async def get_artist(artist_id: str) -> str:
        """
        returns a single artist details given the artist's ID, URI or URL

        Args:
            artist_id: an artist ID, URI or URL
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            artist = client.artist(artist_id)
            result = "" 
            if artist:
                result += f"Artist Name: {artist["name"]}, Followers: {artist["followers"]["total"]:,}.\n"
                result += f"Popularity: {artist["popularity"]}\n"
                result += f"URI: {artist["uri"]}"
            else:
                result += "No artist found for this ID"

            return result
        except Exception as e:
            return f"Error getting artist: {e}"
        
    @mcp.tool()
    async def get_artist_albums(artist_id: str, include_groups: str = "album", country: str = None, limit: int = 20, offset: int = 0) -> str:
        """
        Get an artist's albums

        Args:
            artist_id: the artist ID, URI or URL
            include_groups: types of items to return - 'album', 'single', 'appears_on', 'compilation' or combinations like 'album,single' (default: 'album')
            country: limit response to one particular country (ISO 3166-1 alpha-2 code) (default: None)
            limit: number of albums to return (default: 20, max: 50)
            offset: index of the first album to return (default: 0)
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            artist = client.artist(artist_id)
            artist_name = artist['name']
            
            albums = client.artist_albums(
                artist_id, 
                album_type=None,  # deprecated
                include_groups=include_groups,
                country=country,
                limit=limit,
                offset=offset
            )
            
            if not albums['items']:
                return f"No albums found for artist '{artist_name}' with the specified criteria."
            
            result = f"Albums by {artist_name} (showing {len(albums['items'])} of {albums['total']} total):\n\n"
            
            for i, album in enumerate(albums['items'], 1):
                album_type = album['album_type'].capitalize()
                release_date = album.get('release_date', 'Unknown')
                total_tracks = album.get('total_tracks', 0)
                
                other_artists = [artist['name'] for artist in album['artists'] if artist['name'] != artist_name]
                collab_text = f" (with {', '.join(other_artists)})" if other_artists else ""
                
                result += f"{i}. {album['name']}, {collab_text}\n"
                result += f"Type: {album_type} | Release: {release_date} | Tracks: {total_tracks}\n"
                result += f"URI: '{album['uri']}' | ID: '{album['id']}'\n\n"
            
            if albums['total'] > len(albums['items']) + offset:
                remaining = albums['total'] - len(albums['items']) - offset
                result += f"... and {remaining} more albums (use offset parameter to see more)"
            
            return result    
        except Exception as e:
            return f"Error getting artist albums: {e}"
        
    @mcp.tool()
    async def get_artist_top_tracks(artist_id: str, country: str = None) -> str:
        """
        Get the top tracks of a artist.

        Args:
            artist_id: the artist ID, URI or URL
            country: limit the response to one particular country (Default = None) (ISO 3166-1 alpha-2 code)
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            tracks = client.artist_top_tracks(artist_id, country)
            result = ""
            if not tracks["tracks"]:
                return "Artist does not have any tracks"
            
            for i, track in enumerate(tracks["tracks"][:20], 1):
                artists = ", ".join([artist["name"] for artist in track["artists"]])
                result += f"{i}. Track: {track["name"]}, Artist: {artists}, URI: '{track["uri"]}'.\n"

            return result
        except Exception as e:
            return f"Error getting artist's top tracks: {e}"
        

            
    
            
                
        

        
    
            

        
