from pymongo import MongoClient
import os

from datetime import datetime

import string
import random

MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI)
db = client.get_database('banking_bot')

def create_account(user_id, guild_id, username,guild_name):
    """Create a new account in the database"""
    accounts_collection = db["accounts"]    
    existing_account = accounts_collection.find_one({"user_id": user_id})

    if existing_account:
        return False # Account already exists

    accounts_collection.insert_one({
        "user_id": user_id,
        "username": username,
        "branch_id": guild_id,
        "branch_name": guild_name,
        "balance": 0,
        "created_at": datetime.now()
    })
    return True

def get_account(user_id):
    """Fetches the account of the user ID."""
    accounts_collection = db["accounts"]
    return accounts_collection.find_one({"user_id": user_id})

def update_balance(user_id, new_balance):
    """Updates the balance of the user ID."""
    accounts_collection = db["accounts"]
    accounts_collection.update_one({"user_id": user_id}, {"$set": {"balance": new_balance}})


def log_failed_kyc_attempt(user_id, provided_user_id, guild_id, provided_guild_id, reason):
    """Logs failed KYC attempts in database"""
    failed_kyc_collection = db["failed_kyc_attempts"]
    failed_kyc_collection.insert_one({
        "User_Id": user_id,
        "Provided_User_Id": provided_user_id,
        "Branch_Id": guild_id,
        "Provided_Branch_Id": provided_guild_id,
        "reason": reason,
        "timestamp": datetime.now()
    })

def log_transaction(user_id, txn_type, amount, receiver_id=None):
    """Logs a transaction in the database."""
    transactions_collection = db["transactions"]
    transaction = {
        "user_id": user_id,
        "type": txn_type,
        "amount": amount,
        "receiver_id": receiver_id,
        "timestamp": datetime.utcnow()
    }
    transactions_collection.insert_one(transaction)

def get_transactions(user_id):
    """
    Fetches the last transactions for a user.
    Returns a list of transactions.
    """
    transactions_collection = db["transactions"]
    return list(transactions_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(10))

def generate_upi_id(user_id):
    """Generates a unique UPI ID for the user."""
    bank_name = "quantumbank"  # Replace with your bank name
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"{user_id}@{bank_name}.{random_suffix}"

def set_upi_id(user_id):
    """Sets the UPI ID for the user in the database."""
    upi_id = generate_upi_id(user_id)
    accounts_collection = db["accounts"]

    accounts_collection.update_one({"user_id": user_id}, {"$set": {"upi_id": upi_id}})

    return upi_id

def get_leaderboard(branch_name):
    """Fetches the leaderboard based on balances for a specific branch."""
    return list(db.accounts.find({"branch_name": branch_name}).sort("balance", -1).limit(10))

def update_user_branch(user_id, branch_id, branch_name):
    """
    Updates the branch information for a user in the database.

    This function updates the `branch_id` and `branch_name` for the specified
    user in the database. It uses the user's `user_id` to find the correct
    record and then updates the associated branch details.

    Parameters:
        user_id (str): The unique identifier of the user whose branch information 
                       needs to be updated.
        branch_id (str): The ID of the new branch to be assigned to the user.
        branch_name (str): The name of the new branch to be assigned to the user.

    Returns:
        pymongo.results.UpdateResult: The result of the update operation,
        which provides details about the update, such as the number of modified documents.
    """
    result = db.accounts.update_one(
        {"user_id": user_id},
        {"$set": {"branch_id": branch_id, "branch_name": branch_name}}
    )
    return result.modified_count > 0

def toggle_command(guild_id, command_name, status):
    """Toggle a command's status for a specific guild"""
    commands_collection = db["guild_commands"]
    commands_collection.update_one(
        {"guild_id": guild_id},
        {"$set": {command_name: status}},
        upsert=True
    )

def get_command_status(guild_id, command_name):
    """Get the status of a command for a specific guild"""
    commands_collection = db["guild_commands"]
    guild_commands = commands_collection.find_one({"guild_id": guild_id})
    return guild_commands.get(command_name, True) if guild_commands else True


