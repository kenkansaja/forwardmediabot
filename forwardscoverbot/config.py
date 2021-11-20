from dotenv import load_dotenv
from os import path, getenv


if path.exists("local.env"):
    load_dotenv("local.env")
else:
    load_dotenv()


class Config:
    BOT_TOKEN = getenv("BOT_TOKEN", "1234:abcd")
    ADMINS = int(getenv("ADMINS", "1952053555"))
    DB_PATH = getenv("DB_PATH", None)


config = Config()

