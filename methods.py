import requests
from config import get_settings
from hashlib import sha1
from typing import Any
from cryptography.fernet import Fernet
import json

settings = get_settings()

def calculate_signature(app_key: str, secret_key: str, body_json: dict[str, Any]) -> str:
    return sha1(
        (secret_key + app_key + json.dumps(body_json, sort_keys=True)).encode("utf-8")
    ).hexdigest()

def create_withdrawal(data: dict[str, Any]) -> json:    
    signature = calculate_signature(settings.app_id, settings.api_secret, data)
    headers = {"Application-id": settings.app_id, "Signature": signature, "Content-Type": "application/json"}
    return requests.post(settings.base_url + "/withdrawals", headers=headers, json=data).json()

def get_withdrawal(uuid: str) -> json:
    signature = calculate_signature(settings.app_id, settings.api_secret, {})
    headers = {"Application-id": settings.app_id, "Signature": signature, "Accept": "application/json"}
    return requests.get(settings.base_url + f"/withdrawals/{uuid}", headers=headers).json()

def callback_withdrawal(uuid: str, data: dict[str, Any]) -> json:
    signature = calculate_signature(settings.app_id, settings.api_secret, data)
    headers = {"Application-id": settings.app_id, "Signature": signature, "Content-Type": "application/json", "Accept": "application/json"}
    return requests.put(settings.base_url + f"/withdrawals/{uuid}/callback", headers=headers, json=data).json()

def get_transaction(uuid: str) -> json:
    signature = calculate_signature(settings.app_id, settings.api_secret, {})
    headers = {"Application-id": settings.app_id, "Signature": signature, "Accept": "application/json"}
    return requests.get(settings.base_url + f"/transactions/{uuid}", headers=headers).json()

def update_transaction(uuid: str) -> json:
    signature = calculate_signature(settings.app_id, settings.api_secret, {})
    headers = {"Application-id": settings.app_id, "Signature": signature, "Accept": "application/json"}
    return requests.put(settings.base_url + f"/transactions/{uuid}", headers=headers).json()

def delete_transaction(uuid: str) -> json:
    signature = calculate_signature(settings.app_id, settings.api_secret, {})
    headers = {"Application-id": settings.app_id, "Signature": signature, "Accept": "application/json"}
    return requests.delete(settings.base_url + f"/transactions/{uuid}", headers=headers).json()

def add_transaction(data: dict[str, Any]) -> json:
    signature = calculate_signature(settings.app_id, settings.api_secret, data)
    headers = {"Application-id": settings.app_id, "Signature": signature, "Content-Type": "application/json", "Accept": "application/json"}
    return requests.post(settings.base_url + "/transactions", headers=headers, json=data).json()

def callback_transaction(uuid: str, data: dict[str, Any]) -> json:
    signature = calculate_signature(settings.app_id, settings.api_secret, data)
    headers = {"Application-id": settings.app_id, "Signature": signature, "Content-Type": "application/json", "Accept": "application/json"}
    return requests.put(settings.base_url + f"/transactions/{uuid}/callback", headers=headers, json=data).json()

def validate_user(data: dict[str, Any]) -> json:
    fernet_instance = Fernet(settings.crypt_key)
    signature = fernet_instance.encrypt(json.dumps(data).encode("utf-8")).decode("utf-8")
    headers = {"Signature": signature, "Content-Type": "application/json", "Accept": "application/json"}
    return requests.post(settings.base_url + "/integration/validation", headers=headers, json=data).json()

def dispute(data: dict[str, Any], file_data: Any) -> json:
    headers = {"Accept": "application/json"}
    return requests.post(settings.base_url + "/dispute", data=data, files=file_data, headers=headers).json()