import sys

from streamlit.web import cli as stcli

if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        "./desk_copilot/main.py",
        "--server.port",
        "7561",
        "--server.headless",
        "true",
        "--global.developmentMode",
        "false",
    ]
    sys.exit(stcli.main())
