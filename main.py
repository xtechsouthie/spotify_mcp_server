from mcp.server.fastmcp import FastMCP
from src.tools.playlist_tools import add_playlist_tools
from src.auth import spotify_auth

mcp = FastMCP("spotify")

add_playlist_tools(mcp)

def main():
    if not spotify_auth.get_client():
        print("failed to authenticate with spotify")
        return
    
    print("Spotify MCP Server started with all features")
    mcp.run()

if __name__ == "__main__":
    main()

    