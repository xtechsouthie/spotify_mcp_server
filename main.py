from mcp.server.fastmcp import FastMCP
from src.tools.playlist_tools import add_playlist_tools
from src.tools.playback_tools import add_playback_tools
from src.tools.search_tools import add_search_tools
from src.tools.album_tools import add_album_tools
from src.tools.user_tools import add_user_tools
from src.auth import spotify_auth

mcp = FastMCP("spotify")
#add scopes

add_playlist_tools(mcp)
add_playback_tools(mcp)
add_search_tools(mcp)
add_album_tools(mcp)
add_user_tools(mcp)

def main():
    if not spotify_auth.get_client():
        print("failed to authenticate with spotify")
        return
    
    print("Spotify MCP Server started with all features")
    mcp.run()

if __name__ == "__main__":
    main()

