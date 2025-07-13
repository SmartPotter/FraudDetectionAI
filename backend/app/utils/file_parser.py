import pandas as pd
import io
from typing import List, Dict, Any
from datetime import datetime
import numpy as np

def parse_csv_file(file_contents: bytes) -> pd.DataFrame:
    """Parse CSV file contents into pandas DataFrame"""
    try:
        # Read CSV from bytes
        df = pd.read_csv(io.BytesIO(file_contents))
        
        # Basic validation
        if df.empty:
            raise ValueError("CSV file is empty")
        
        # Check for required columns (flexible)
        required_columns = ['transaction_id', 'user_id', 'amount']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        return df
        
    except Exception as e:
        raise ValueError(f"Failed to parse CSV file: {str(e)}")

def validate_transaction_data(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Validate and clean transaction data"""
    try:
        validated_data = []
        
        for index, row in df.iterrows():
            try:
                # Validate and convert data types
                transaction_record = {
                    "transaction_id": str(row.get("transaction_id", f"TXN_{index:06d}")),
                    "user_id": str(row.get("user_id", f"user_{index}")),
                    "amount": float(row.get("amount", 0)),
                    "timestamp": parse_timestamp(row.get("timestamp")),
                    "location": str(row.get("location", "Unknown")),
                    "device_id": str(row.get("device_id", "")) if pd.notna(row.get("device_id")) else None,
                    "payment_method": str(row.get("payment_method", "")) if pd.notna(row.get("payment_method")) else None,
                    "merchant_category": str(row.get("merchant_category", "")) if pd.notna(row.get("merchant_category")) else None
                }
                
                # Validate amount
                if transaction_record["amount"] < 0:
                    raise ValueError(f"Invalid amount: {transaction_record['amount']}")
                
                # Validate user_id
                if not transaction_record["user_id"] or transaction_record["user_id"] == "nan":
                    raise ValueError("Invalid user_id")
                
                validated_data.append(transaction_record)
                
            except Exception as e:
                print(f"Skipping invalid row {index}: {e}")
                continue
        
        if not validated_data:
            raise ValueError("No valid transaction records found")
        
        return validated_data
        
    except Exception as e:
        raise ValueError(f"Data validation failed: {str(e)}")

def parse_timestamp(timestamp_value) -> str:
    """Parse various timestamp formats into ISO format"""
    if pd.isna(timestamp_value):
        return datetime.now().isoformat()
    
    try:
        # Try to parse as datetime
        if isinstance(timestamp_value, str):
            # Common formats
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%d",
                "%m/%d/%Y %H:%M:%S",
                "%m/%d/%Y"
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(timestamp_value, fmt)
                    return dt.isoformat()
                except ValueError:
                    continue
            
            # If no format matches, try pandas parsing
            dt = pd.to_datetime(timestamp_value)
            return dt.isoformat()
        
        elif isinstance(timestamp_value, (int, float)):
            # Assume Unix timestamp
            dt = datetime.fromtimestamp(timestamp_value)
            return dt.isoformat()
        
        else:
            # Try pandas conversion
            dt = pd.to_datetime(timestamp_value)
            return dt.isoformat()
            
    except Exception:
        # Return current time if parsing fails
        return datetime.now().isoformat()

def generate_sample_csv_data() -> pd.DataFrame:
    """Generate sample CSV data for testing"""
    np.random.seed(42)
    
    n_records = 1000
    
    # Generate sample data
    data = {
        "transaction_id": [f"TXN_{i:06d}" for i in range(1, n_records + 1)],
        "user_id": [f"user_{np.random.randint(1, 500)}" for _ in range(n_records)],
        "amount": np.random.lognormal(mean=4, sigma=1, size=n_records).round(2),
        "timestamp": pd.date_range(start="2024-01-01", periods=n_records, freq="H"),
        "location": [f"Store {np.random.randint(1000, 9999)}" for _ in range(n_records)],
        "device_id": [f"device_{np.random.randint(1, 100):03d}" for _ in range(n_records)],
        "payment_method": np.random.choice(["credit_card", "debit_card", "mobile_pay"], size=n_records),
        "merchant_category": np.random.choice(["grocery", "electronics", "clothing", "pharmacy"], size=n_records)
    }
    
    return pd.DataFrame(data)

def export_sample_csv(filename: str = "sample_transactions.csv") -> str:
    """Export sample CSV data to file"""
    df = generate_sample_csv_data()
    df.to_csv(filename, index=False)
    return filename

def validate_csv_structure(df: pd.DataFrame) -> Dict[str, Any]:
    """Validate CSV structure and return analysis"""
    analysis = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.astype(str).to_dict(),
        "sample_data": df.head(3).to_dict(orient="records"),
        "issues": []
    }
    
    # Check for common issues
    if df.empty:
        analysis["issues"].append("Dataset is empty")
    
    # Check for required columns
    required_columns = ["transaction_id", "user_id", "amount"]
    missing_required = [col for col in required_columns if col not in df.columns]
    if missing_required:
        analysis["issues"].append(f"Missing required columns: {missing_required}")
    
    # Check for duplicate transaction IDs
    if "transaction_id" in df.columns:
        duplicates = df["transaction_id"].duplicated().sum()
        if duplicates > 0:
            analysis["issues"].append(f"Found {duplicates} duplicate transaction IDs")
    
    # Check for invalid amounts
    if "amount" in df.columns:
        try:
            amounts = pd.to_numeric(df["amount"], errors="coerce")
            negative_amounts = (amounts < 0).sum()
            if negative_amounts > 0:
                analysis["issues"].append(f"Found {negative_amounts} negative amounts")
            
            zero_amounts = (amounts == 0).sum()
            if zero_amounts > 0:
                analysis["issues"].append(f"Found {zero_amounts} zero amounts")
        except Exception:
            analysis["issues"].append("Amount column contains non-numeric values")
    
    return analysis