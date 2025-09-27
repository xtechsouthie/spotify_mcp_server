from mcp.server.fastmcp import FastMCP
from ..auth import spotify_auth
from typing import Literal

def add_user_tools(mcp: FastMCP):

    @mcp.tool()
    async def get_current_user() -> str:
        """
        Get information about the current user (name, email, country, id, uri)
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            user = client.me()
            result = f"Username: '{user["display_name"]}', Email: {user["email"]}, Country code: {user["country"]}\n"
            result += f"User ID: '{user["id"]}', URI: '{user["uri"]}'\n"
            return result
        except Exception as e:
            return f"Error fetching current user data: {e}"
        
    @mcp.tool()
    async def get_current_users_top_artists(limit: int = 20, offset: int= 0, time_range: Literal['short_term', 'medium_term', 'long_term'] = 'medium_term') -> str:
        """
        Get the top artists of the current user for a given time period

        Args:
            limit: the limit on number of artists to return (default = 20)
            offset: the index of the first artist to return
            time_range: time frame for affinities - 'short_term' (~4 weeks), 'medium_term' (~6 months), 'long_term' (several years) (default: 'medium_term')
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            top_artists = client.current_user_top_artists(
                limit=limit,
                offset=offset,
                time_range=time_range
            )
            
            if not top_artists['items']:
                return f"no top artists found for time range: {time_range}"
            
            time_descriptions = {
                'short_term': 'last 4 weeks',
                'medium_term': 'last 6 months', 
                'long_term': 'all time'
            }
            time_desc = time_descriptions.get(time_range, time_range)
            
            result = f"your top {len(top_artists['items'])} artists ({time_desc}):\n\n"
            
            for i, artist in enumerate(top_artists['items'], 1):
                followers = artist['followers']['total']
                popularity = artist.get('popularity', 0)
                genres = ", ".join(artist['genres'][:3]) if artist['genres'] else "No genres"
                
                result += f"{i}. {artist['name']}\n"
                result += f"Popularity: {popularity}/100 | Followers: {followers:,}\n"
                result += f"Genres: {genres}\n"
                result += f"URI: `{artist['uri']}`\n---\n"
            
            return result
            
        except Exception as e:
            return f"Error getting top artists: {e}"
        
    @mcp.tool()
    async def get_current_users_top_tracks(limit: int = 20, offset: int = 0, time_range: Literal['short_term', 'medium_term', 'long_term'] = 'medium_term') -> str:
        """
        Get the top artists of the current user for a given time period

        Args:
            limit: the limit on number of artists to return (default = 20)
            offset: the index of the first artist to return
            time_range: time frame for affinities - 'short_term' (~4 weeks), 'medium_term' (~6 months), 'long_term' (several years) (default: 'medium_term')
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            top_tracks = client.current_user_top_tracks(
                limit=limit,
                offset=offset,
                time_range=time_range
            )
            
            if not top_tracks['items']:
                return f"No top tracks found for time range '{time_range}'"
            
            time_descriptions = {
                'short_term': 'last 4 weeks',
                'medium_term': 'last 6 months', 
                'long_term': 'all time'
            }
            time_desc = time_descriptions.get(time_range, time_range)
            
            result = f"your top {len(top_tracks['items'])} tracks ({time_desc}):\n\n"
            
            for i, track in enumerate(top_tracks['items'], 1):
                artists = ", ".join([artist['name'] for artist in track['artists']])
                album = track['album']['name']
                popularity = track.get('popularity', 0)
                
                result += f"{i}. {track['name']} by {artists}\n"
                result += f"Album: {album}, Popularity: {popularity}/100\n"
                result += f"URI: '{track['uri']}'\n---\n"
            
            return result  
        except Exception as e:
            return f"Error getting top tracks: {e}"
        
    @mcp.tool()
    async def get_current_users_followed_artists(limit: int = 20, after: str = None) -> str:
        """
        Get the artists followed by the current user

        Args:
            limit: number of artists to return (default = 20, max = 50)
            after: the last artist ID retrieved from the previous request (for pagination) (default = None) (kinda like offset)
        """
        client = spotify_auth.get_client()
        if not client:
            return "error with user authentication"
        
        try:
            followed_artists = client.current_user_followed_artists(limit=limit, after=after)

            if not followed_artists:
                return "You are not following any artists "
            
            artists = followed_artists["artists"]["items"]
            total = followed_artists["artists"]["total"]

            result= f"the artists you follow are (showing {len(artists)} of {total}):\n\n"
            for i, artist in enumerate(artists, 1):
                followers = artist['followers']['total']
                genres = ", ".join(artist['genres'][:3]) if artist['genres'] else "No genres"
                result += f"{i}. Artist: {artist["name"]}, Followers: {followers:,}, Genres: {genres}\n"
                result += f"aritst URI: '{artist["uri"]}', ID: '{artist["id"]}'\n---\n"

            if followed_artists["artists"]["next"]:
                result += f"to see the next artists, user after = '{followed_artists["artists"]["cursors"]["next"]}'\n"
            
            return result
        except Exception as e:
            return f"Error getting users followed artists: {e}"


    
    
