import logging
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Optional
from Bot import MONGO_DB as DB_URL, BOT_NAME, OWNER_ID

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

# MongoDB setup for PyMongo
cluster = MongoClient(DB_URL)
db = cluster['Encoding']
users = db[BOT_NAME]

def check_user_mdb(user_id: int) -> Optional[int]:
    try:
        got = users.find_one({'user_id': int(user_id)})
        if got is not None:
            return int(got['user_id'])
        return None
    except PyMongoError as e:
        logging.error(f"Error checking user {user_id}: {e}")
        raise

def check_crf_mdb(user_id: int) -> Optional[int]:
    try:
        got = users.find_one({'user_id': int(user_id)})
        if got is not None:
            return int(got.get('crf', 30))  # Default to 26
        return None
    except PyMongoError as e:
        logging.error(f"Error fetching CRF for user {user_id}: {e}")
        raise

def check_resolution_settings(user_id: int) -> Optional[str]:
    try:
        got = users.find_one({'user_id': int(user_id)})
        if got is not None:
            return got.get('resolution', '480p')  # Default to 480p
        return None
    except PyMongoError as e:
        logging.error(f"Error fetching resolution for user {user_id}: {e}")
        raise

def check_preset_settings(user_id: int) -> Optional[str]:
    try:
        got = users.find_one({'user_id': int(user_id)})
        if got is not None:
            return got.get('preset', 'fast')  # Default to fast
        return None
    except PyMongoError as e:
        logging.error(f"Error fetching preset for user {user_id}: {e}")
        raise

def check_vcodec_settings(user_id: int) -> Optional[str]:
    try:
        got = users.find_one({'user_id': int(user_id)})
        if got is not None:
            return got.get('vcodec', 'x264')  # Default to x264
        return None
    except PyMongoError as e:
        logging.error(f"Error fetching vcodec for user {user_id}: {e}")
        raise

def check_audio_type_mdb(user_id: int) -> Optional[str]:
    try:
        got = users.find_one({'user_id': int(user_id)})
        if got is not None:
            return str(got.get('audio_type', 'aac'))  # Default to aac
        return None
    except PyMongoError as e:
        logging.error(f"Error fetching audio type for user {user_id}: {e}")
        raise

def update_resolution_settings(user_id: int, new: str) -> str:
    try:
        result = users.update_one({'user_id': int(user_id)}, {'$set': {'resolution': new}})
        if result.modified_count > 0 or result.matched_count > 0:
            return 'Success'
        logging.warning(f"No update performed for resolution of user {user_id}")
        return 'Success'
    except PyMongoError as e:
        logging.error(f"Error updating resolution for user {user_id}: {e}")
        raise

def update_preset_settings(user_id: int, new: str) -> str:
    try:
        result = users.update_one({'user_id': int(user_id)}, {'$set': {'preset': new}})
        if result.modified_count > 0 or result.matched_count > 0:
            return 'Success'
        logging.warning(f"No update performed for preset of user {user_id}")
        return 'Success'
    except PyMongoError as e:
        logging.error(f"Error updating preset for user {user_id}: {e}")
        raise

def update_vcodec_settings(user_id: int, new: str) -> str:
    try:
        result = users.update_one({'user_id': int(user_id)}, {'$set': {'vcodec': new}})
        if result.modified_count > 0 or result.matched_count > 0:
            return 'Success'
        logging.warning(f"No update performed for vcodec of user {user_id}")
        return 'Success'
    except PyMongoError as e:
        logging.error(f"Error updating vcodec for user {user_id}: {e}")
        raise

def update_audio_type_mdb(user_id: int, new: str) -> str:
    try:
        result = users.update_one({'user_id': int(user_id)}, {'$set': {'audio_type': new}})
        if result.modified_count > 0 or result.matched_count > 0:
            return 'Success'
        logging.warning(f"No update performed for audio type of user {user_id}")
        return 'Success'
    except PyMongoError as e:
        logging.error(f"Error updating audio type for user {user_id}: {e}")
        raise

def update_crf(user_id: int, new: int) -> str:
    try:
        result = users.update_one({'user_id': int(user_id)}, {'$set': {'crf': new}})
        if result.modified_count > 0 or result.matched_count > 0:
            return 'Success'
        logging.warning(f"No update performed for CRF of user {user_id}")
        return 'Success'
    except PyMongoError as e:
        logging.error(f"Error updating CRF for user {user_id}: {e}")
        raise

def get_uptype(user_id: int) -> str:
    try:
        user = users.find_one({'_id': int(user_id)})
        return user.get('uptype', 'document') if user else 'document'
    except PyMongoError as e:
        logging.error(f"Error fetching uptype for user {user_id}: {e}")
        raise

def set_uptype(user_id: int, uptype: str) -> None:
    if uptype not in ['video', 'document']:
        logging.error(f"Invalid uptype {uptype} for user {user_id}")
        raise ValueError(f"Invalid uptype: {uptype}")
    try:
        users.update_one({'_id': int(user_id)}, {'$set': {'uptype': uptype}})
    except PyMongoError as e:
        logging.error(f"Error setting uptype for user {user_id}: {e}")
        raise

def owner_check():
    try:
        check = check_user_mdb(OWNER_ID)
        check2 = check_user_mdb(953362604)  # DEV ID
        if check is None:
            users.insert_one({
                'user_id': OWNER_ID,
                'resolution': '480p',
                'preset': 'fast',
                'audio_type': 'aac',
                'vcodec': 'x264',
                'crf': 30,
                'uptype': 'document'
            })
            logging.info(f"Initialized owner {OWNER_ID} in database")
        if check2 is None:
            users.insert_one({
                'user_id': 953362604,
                'resolution': '480p',
                'preset': 'fast',
                'audio_type': 'aac',
                'vcodec': 'x264',
                'crf': 30,
                'uptype': 'document'
            })
            logging.info(f"Initialized dev 953362604 in database")
    except PyMongoError as e:
        logging.error(f"Error in owner_check: {e}")
        raise

