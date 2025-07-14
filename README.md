# AI-Powered Fraud Detection & Prevention Platform

A next-gen fraud prevention and trust platform for enterprise retailers (like Walmart) that leverages AI, blockchain, and real-time risk scoring to detect, explain, and block fraudulent transactions — all in a sleek, enterprise-grade UI.

---

## Demo

[Demo Video](https://drive.google.com/file/d/1D3hOtacD0jWKbgTKsrJ9WJpgQCDFlG11/view?usp=sharing)

---

## Features

### Real-Time Fraud Detection
- Upload transaction CSVs via the UI or API
- Backend ML model (e.g. XGBoost or LSTM) scores each transaction
- Flags high-risk or suspicious activity instantly

### Explainable AI (via Groq)
- Human-readable explanations for each flagged transaction
- Powered by Groq LLMs (e.g., Mixtral)
- Example:  
  > “This transaction was flagged due to a sudden drop in origin balance and destination previously associated with fraud.”

### Blockchain Logging
- Immutable record of flagged fraud using a Solidity smart contract
- Includes timestamp, transaction ID, IPFS hash for future audits

### Visual Dashboards (React + Tailwind)
- Metrics: Total transactions, fraud detected, high-risk alerts, blocked users
- Charts:  
  - **Risk Score Trends** (Line Chart)
  - **Regional Risk Heatmap** (Map using `react-simple-maps`)

### Supabase Integration
- Stores user uploads, transaction data, and explanations
- Secure role-based access to view and manage fraud data

---

# Tech Stack

| Layer       | Tech Used                             |
|------------|----------------------------------------|
| Frontend   | React, TailwindCSS, Lucide Icons       |
| Backend    | FastAPI, Pydantic, Pandas, Uvicorn     |
| ML/AI      | XGBoost (or custom model) + Groq       |
| Storage    | Supabase (Postgres, Storage API)       |
| Blockchain | Solidity Smart Contract + IPFS (WIP)   |

---

## Local Development

### 1. Clone and setup
```bash
git clone https://github.com/yourname/fraud-detector.git
cd fraud-detector
```
### 2. Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```
### 3. Frontend (React)
```bash
cd frontend
npm install
npm run dev
```
---

## Sample Transaction CSV Format
```arduino
transaction_id,user_id,step,type,amount,nameOrig,oldbalanceOrg,newbalanceOrig,nameDest,oldbalanceDest,newbalanceDest,isFraud,isFlaggedFraud
txn_001,usr_001,1,TRANSFER,4500.00,C123456789,12000.00,7500.00,C987654321,0.00,4500.00,1,0
```
Columns transaction_id and user_id are required by backend parser

## API Endpoints
Method	Endpoint	Description
POST	/api/upload	Upload and process CSV file
GET	/api/upload/status/{id}	Check upload processing status
DELETE	/api/upload/{id}	Delete an uploaded file

## Solidity Smart Contract (Logging Fraud)
Example logging interface:

```solidity
function logFraud(
    string memory transactionId,
    string memory userId,
    string memory ipfsHash,
    string memory explanation
) public onlyFraudLogger {
    ...
}
```
More: /contracts/FraudLog.sol

## Groq Prompt Template
```text
Explain why this transaction is suspicious:
- Amount: $2,450
- Origin Account Balance Before: $10,000
- After: $7,550
- Destination Account: acct_XYZ
- Flagged: Yes
```
---

## Future Roadmap
✅ Role-based user access

✅ LLM-powered fraud explanations

✅ Blockchain + IPFS logging

⏳ Live websocket alerts

⏳ Confidence score thresholds

⏳ Mobile optimization

⏳ Real-time model retraining

## License
MIT License. Free to use, modify, and deploy.
