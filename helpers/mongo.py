from __main__ import connect
from motor.motor_asyncio import AsyncIOMotorClient


def connection():
    client = AsyncIOMotorClient(connect["host"], connect["port"])
    db = client[connect["db"]]
    return db


db = connection()
