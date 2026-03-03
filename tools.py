from langchain_core.tools import tool

@tool
def menu():
    """Send the restaurant menu link when the user asks to see the menu."""
    
    return (
        "Here is our full menu:\n"
        "https://shorturl.at/OyS5q\n\n"
        "Let me know if you'd like recommendations!"
    )

@tool
def today_deals():
    """Return current specials"""
    
    return "Today's deal is the Hot Gates burger with a free drink."