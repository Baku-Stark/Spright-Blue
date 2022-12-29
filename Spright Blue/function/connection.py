# ================================================================
# IMPORT [requests > Internet Connection]
import requests
from requests.exceptions import ConnectionError

# IMPORT [rich - dashboard(console)]
from rich import print
from rich.panel import Panel

# ================================================================
# CONFIGURE [run]
def connection_test():
    url_set = "https://discord.com/channels/633340730441728001/940470635971375114"
    try:
        test_connection = requests.get(url_set, timeout=10)
        test_connection.text
        test_connection.status_code

        print(Panel.fit("[bold black]Internet connection established!", border_style="green", title="Internet"))

        return True

    except ConnectionError as e:
        print(Panel.fit(f"[bold black]Internet connection not established... Please try again later.\n{e}", border_style="red", title="Internet"))
        
        return False

    except:
        print(Panel.fit("[bold black]Internet connection not established... Please try again later.", border_style="red", title="Internet"))

        return False