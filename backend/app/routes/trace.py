from fastapi import APIRouter
import requests

router = APIRouter()

ALCHEMY_SEPOLIA_URL = "https://eth-sepolia.g.alchemy.com/v2/Ptov-ZXX5VTeL_67gBMMzJz3bdzcBeFx"

@router.get("/trace/{tx_hash}")
def trace_transaction(tx_hash: str):
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "debug_traceTransaction",
        "params": [tx_hash]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    try:
        response = requests.post(ALCHEMY_SEPOLIA_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
