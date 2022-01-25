import os

from os import getenv

from dotenv import load_dotenv

load_dotenv()

    STRING_SESSION = os.environ.get("STRING_SESSION", "")

    API_ID = int(getenv("API_ID"))

    API_HASH = getenv("API_HASH")

    OWNER_ID = getenv("OWNER_ID")

    SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
