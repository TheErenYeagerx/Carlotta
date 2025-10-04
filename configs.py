from os import getenv

class Config:
    # API Keys
    API_ID = int(getenv("API_ID", ""))
    API_HASH = getenv("API_HASH", "")

    # Bot Token
    BOT_TOKEN = getenv("BOT_TOKEN", "")

    # MongoDB URI
    MONGO_URI = getenv(
        "MONGO_URI",
        ""
    )

    # Bot Config
    BOT_USERNAME = getenv("BOT_USERNAME", "Carlotta_Robot")
    CHID = int(getenv("CHID", -00))

    # Sudo Users
    SUDO = list(map(int, getenv("SUDO", "5106602523").split()))

    # Start Image and Channel/Support URLs for better UI
    START_IMG = getenv("START_IMG", "https://i.ibb.co/Xxt4Ng9k/tmp06ygsqsu.jpg")
    CHANNEL_URL = getenv("CHANNEL_URL", "https://t.me/TheRadhaupdate")
    SUPPORT_URL = getenv("SUPPORT_URL", "https://t.me/RadhaSprt")

cfg = Config()
