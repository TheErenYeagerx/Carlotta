from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
from configs import cfg

# --- MongoDB client ---
client = MongoClient(cfg.MONGO_URI)

# Database and collections
db = client["main"]
users = db["users"]
groups = db["groups"]

# --- Ensure indexes for fast lookups ---
users.create_index([("user_id", ASCENDING)], unique=True)
groups.create_index([("chat_id", ASCENDING)], unique=True)


# --- User functions ---
def add_user(user_id: int) -> None:
    """
    Add a user to the database.
    Uses upsert to avoid duplicates efficiently.
    """
    try:
        users.update_one(
            {"user_id": str(user_id)},
            {"$set": {"user_id": str(user_id)}},
            upsert=True
        )
    except DuplicateKeyError:
        pass


def remove_user(user_id: int) -> None:
    """Remove a user from the database."""
    users.delete_one({"user_id": str(user_id)})


def already_db(user_id: int) -> bool:
    """Check if a user exists in the database."""
    return users.find_one({"user_id": str(user_id)}) is not None


def all_users() -> int:
    """Return the total number of users."""
    return users.count_documents({})


# --- Group functions ---
def add_group(chat_id: int) -> None:
    """
    Add a group to the database.
    Uses upsert to avoid duplicates efficiently.
    """
    try:
        groups.update_one(
            {"chat_id": str(chat_id)},
            {"$set": {"chat_id": str(chat_id)}},
            upsert=True
        )
    except DuplicateKeyError:
        pass


def already_dbg(chat_id: int) -> bool:
    """Check if a group exists in the database."""
    return groups.find_one({"chat_id": str(chat_id)}) is not None


def all_groups() -> int:
    """Return the total number of groups."""
    return groups.count_documents({})