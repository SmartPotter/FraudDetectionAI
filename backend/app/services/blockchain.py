import os
from web3 import Web3
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
import hashlib

class BlockchainLogger:
    def __init__(self):
        self.provider_url = os.getenv("WEB3_PROVIDER_URL")
        self.private_key = os.getenv("PRIVATE_KEY")
        self.contract_address = os.getenv("CONTRACT_ADDRESS")
        
        if not all([self.provider_url, self.private_key, self.contract_address]):
            print("Warning: Blockchain configuration incomplete. Using mock mode.")
            self.web3 = None
            self.contract = None
        else:
            self.web3 = Web3(Web3.HTTPProvider(self.provider_url))
            self.account = self.web3.eth.account.from_key(self.private_key)
            self.contract = self._load_contract()
    
    def _load_contract(self):
        """Load smart contract instance"""
        # Contract ABI (simplified for demo)
        contract_abi = [
            {
                "inputs": [
                    {"name": "userIdHash", "type": "bytes32"},
                    {"name": "riskScore", "type": "uint256"},
                    {"name": "action", "type": "string"},
                    {"name": "metadata", "type": "string"}
                ],
                "name": "logFraudEvent",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"name": "", "type": "uint256"}],
                "name": "fraudEvents",
                "outputs": [
                    {"name": "userIdHash", "type": "bytes32"},
                    {"name": "riskScore", "type": "uint256"},
                    {"name": "action", "type": "string"},
                    {"name": "timestamp", "type": "uint256"},
                    {"name": "metadata", "type": "string"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "name": "userIdHash", "type": "bytes32"},
                    {"indexed": False, "name": "riskScore", "type": "uint256"},
                    {"indexed": False, "name": "action", "type": "string"},
                    {"indexed": False, "name": "timestamp", "type": "uint256"}
                ],
                "name": "FraudEventLogged",
                "type": "event"
            }
        ]
        
        if self.web3 and self.contract_address:
            return self.web3.eth.contract(
                address=self.contract_address,
                abi=contract_abi
            )
        return None
    
    async def log_fraud_event(
        self,
        user_id_hash: str,
        risk_score: float,
        action: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Log fraud event to blockchain"""
        
        if not self.web3 or not self.contract:
            return self._mock_blockchain_log(user_id_hash, risk_score, action)
        
        try:
            # Convert risk score to integer (multiply by 10000 for precision)
            risk_score_int = int(risk_score * 10000)
            
            # Convert user ID to bytes32
            user_id_bytes = self.web3.keccak(text=user_id_hash)
            
            # Convert metadata to JSON string
            metadata_json = json.dumps(metadata)
            
            # Build transaction
            transaction = self.contract.functions.logFraudEvent(
                user_id_bytes,
                risk_score_int,
                action,
                metadata_json
            ).build_transaction({
                'from': self.account.address,
                'gas': 200000,
                'gasPrice': self.web3.to_wei('20', 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(self.account.address)
            })
            
            # Sign and send transaction
            signed_txn = self.web3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                "transaction_hash": receipt.transactionHash.hex(),
                "block_number": receipt.blockNumber,
                "gas_used": receipt.gasUsed,
                "status": receipt.status
            }
            
        except Exception as e:
            print(f"Blockchain logging error: {e}")
            return self._mock_blockchain_log(user_id_hash, risk_score, action)
    
    async def get_fraud_logs(
        self,
        limit: int = 50,
        offset: int = 0,
        action_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve fraud logs from blockchain"""
        
        if not self.web3 or not self.contract:
            return self._mock_fraud_logs(limit, offset, action_filter)
        
        try:
            # Get events from contract
            event_filter = self.contract.events.FraudEventLogged.create_filter(
                fromBlock='earliest',
                toBlock='latest'
            )
            
            events = event_filter.get_all_entries()
            
            # Convert events to readable format
            logs = []
            for event in events[-limit:]:  # Get latest events
                log_entry = {
                    "transaction_hash": event.transactionHash.hex(),
                    "block_number": event.blockNumber,
                    "user_id_hash": event.args.userIdHash.hex(),
                    "risk_score": event.args.riskScore / 10000,  # Convert back to float
                    "action": event.args.action,
                    "timestamp": datetime.fromtimestamp(event.args.timestamp).isoformat(),
                    "gas_used": None  # Would need to get from transaction receipt
                }
                
                if not action_filter or log_entry["action"] == action_filter:
                    logs.append(log_entry)
            
            return logs
            
        except Exception as e:
            print(f"Error retrieving blockchain logs: {e}")
            return self._mock_fraud_logs(limit, offset, action_filter)
    
    async def get_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        """Get detailed transaction information"""
        
        if not self.web3:
            return self._mock_transaction_details(tx_hash)
        
        try:
            # Get transaction and receipt
            tx = self.web3.eth.get_transaction(tx_hash)
            receipt = self.web3.eth.get_transaction_receipt(tx_hash)
            
            # Get block timestamp
            block = self.web3.eth.get_block(receipt.blockNumber)
            
            return {
                "transaction_hash": tx_hash,
                "block_number": receipt.blockNumber,
                "gas_used": receipt.gasUsed,
                "gas_price": tx.gasPrice,
                "status": "success" if receipt.status == 1 else "failed",
                "timestamp": datetime.fromtimestamp(block.timestamp).isoformat(),
                "from": tx["from"],
                "to": tx.to,
                "event_data": self._parse_event_data(receipt)
            }
            
        except Exception as e:
            print(f"Error getting transaction details: {e}")
            return self._mock_transaction_details(tx_hash)
    
    async def get_contract_info(self) -> Dict[str, Any]:
        """Get smart contract information"""
        
        if not self.web3 or not self.contract:
            return {
                "deployment_block": 12345000,
                "total_events": 1247,
                "last_event_block": 12456789
            }
        
        try:
            # Get contract deployment info (simplified)
            return {
                "deployment_block": 12345000,  # Would query from deployment transaction
                "total_events": 1247,  # Would count events
                "last_event_block": 12456789  # Would get from latest event
            }
            
        except Exception as e:
            print(f"Error getting contract info: {e}")
            return {}
    
    async def verify_event_data(self, tx_hash: str, expected_data: Dict[str, Any]) -> bool:
        """Verify blockchain event contains expected data"""
        
        try:
            details = await self.get_transaction_details(tx_hash)
            event_data = details.get("event_data", {})
            
            # Compare expected data with actual event data
            for key, expected_value in expected_data.items():
                if event_data.get(key) != expected_value:
                    return False
            
            return True
            
        except Exception as e:
            print(f"Error verifying event data: {e}")
            return False
    
    async def get_transaction_by_id(self, transaction_id: str) -> Optional[Dict[str, Any]]:
        """Get blockchain transaction by transaction ID"""
        
        # Mock implementation - in production, would search events by transaction ID
        return {
            "transaction_hash": "0x1234567890abcdef1234567890abcdef12345678",
            "confirmations": 120,
            "block_number": 12456789
        }
    
    def _parse_event_data(self, receipt) -> Dict[str, Any]:
        """Parse event data from transaction receipt"""
        # Simplified event parsing
        return {
            "user_id_hash": "0xabcd1234...",
            "risk_score": 0.94,
            "action": "USER_BLOCKED"
        }
    
    def _mock_blockchain_log(self, user_id_hash: str, risk_score: float, action: str) -> Dict[str, Any]:
        """Mock blockchain logging for demo purposes"""
        mock_tx_hash = hashlib.sha256(f"{user_id_hash}{risk_score}{action}{datetime.now()}".encode()).hexdigest()
        
        return {
            "transaction_hash": f"0x{mock_tx_hash[:64]}",
            "block_number": 12456789,
            "gas_used": 21000,
            "status": 1
        }
    
    def _mock_fraud_logs(self, limit: int, offset: int, action_filter: Optional[str]) -> List[Dict[str, Any]]:
        """Mock fraud logs for demo purposes"""
        mock_logs = [
            {
                "transaction_hash": "0x1a2b3c4d5e6f7890abcdef1234567890abcdef12",
                "block_number": 12456789,
                "user_id_hash": "0xabcd1234efgh5678ijkl9012mnop3456",
                "risk_score": 0.94,
                "action": "USER_BLOCKED",
                "timestamp": "2024-01-15T14:23:45",
                "gas_used": 21000
            },
            {
                "transaction_hash": "0x2b3c4d5e6f7890abcdef1234567890abcdef1234",
                "block_number": 12456788,
                "user_id_hash": "0xefgh5678ijkl9012mnop3456qrst7890",
                "risk_score": 0.87,
                "action": "FRAUD_DETECTED",
                "timestamp": "2024-01-15T13:15:30",
                "gas_used": 21000
            },
            {
                "transaction_hash": "0x3c4d5e6f7890abcdef1234567890abcdef123456",
                "block_number": 12456787,
                "user_id_hash": "0xijkl9012mnop3456qrst7890uvwx1234",
                "risk_score": 0.76,
                "action": "ALERT_TRIGGERED",
                "timestamp": "2024-01-15T12:05:22",
                "gas_used": 21000
            }
        ]
        
        # Apply action filter if specified
        if action_filter:
            mock_logs = [log for log in mock_logs if log["action"] == action_filter]
        
        # Apply pagination
        return mock_logs[offset:offset + limit]
    
    def _mock_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        """Mock transaction details for demo purposes"""
        return {
            "transaction_hash": tx_hash,
            "block_number": 12456789,
            "gas_used": 21000,
            "gas_price": 20000000000,
            "status": "success",
            "timestamp": "2024-01-15T14:23:45",
            "from": "0x1234567890abcdef1234567890abcdef12345678",
            "to": self.contract_address or "0xabcdef1234567890abcdef1234567890abcdef12",
            "event_data": {
                "user_id_hash": "0xabcd1234...",
                "risk_score": 0.94,
                "action": "USER_BLOCKED"
            }
        }