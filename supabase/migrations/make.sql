-- Walmart AI Fraud Prevention Platform - Supabase Schema
-- Run this SQL in your Supabase SQL Editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_id VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    location VARCHAR(255),
    device_id VARCHAR(255),
    payment_method VARCHAR(100),
    merchant_category VARCHAR(100),
    risk_score DECIMAL(3,2) DEFAULT 0.0,
    flagged BOOLEAN DEFAULT FALSE,
    file_id VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create blocklist table
CREATE TABLE IF NOT EXISTS blocklist (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255) NOT NULL,
    device_id VARCHAR(255),
    reason TEXT NOT NULL,
    risk_score DECIMAL(3,2),
    blocked_by VARCHAR(255) NOT NULL,
    block_type VARCHAR(50) DEFAULT 'permanent',
    status VARCHAR(50) DEFAULT 'active',
    blocked_at TIMESTAMPTZ DEFAULT NOW(),
    removed_at TIMESTAMPTZ,
    removal_reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create fraud_logs table
CREATE TABLE IF NOT EXISTS fraud_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_id VARCHAR(255),
    user_id VARCHAR(255) NOT NULL,
    user_id_hash VARCHAR(255),
    action VARCHAR(100) NOT NULL,
    risk_score DECIMAL(3,2),
    blockchain_tx VARCHAR(255),
    block_number BIGINT,
    gas_used INTEGER,
    metadata JSONB,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create receipts table
CREATE TABLE IF NOT EXISTS receipts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    receipt_hash VARCHAR(255) UNIQUE NOT NULL,
    transaction_id VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    store VARCHAR(255) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    blockchain_hash VARCHAR(255),
    verification_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create fraud_scores table
CREATE TABLE IF NOT EXISTS fraud_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_id VARCHAR(255) NOT NULL,
    risk_score DECIMAL(3,2) NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    flags TEXT[],
    confidence DECIMAL(3,2),
    model_version VARCHAR(50),
    explanation TEXT,
    key_factors TEXT[],
    recommendations TEXT[],
    scored_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create fraud_explanations table
CREATE TABLE IF NOT EXISTS fraud_explanations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_id VARCHAR(255) NOT NULL,
    explanation TEXT NOT NULL,
    key_factors TEXT[],
    recommendations TEXT[],
    generated_by VARCHAR(100) DEFAULT 'groq_ai',
    generated_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp);
CREATE INDEX IF NOT EXISTS idx_transactions_risk_score ON transactions(risk_score);
CREATE INDEX IF NOT EXISTS idx_transactions_flagged ON transactions(flagged);

CREATE INDEX IF NOT EXISTS idx_blocklist_user_id ON blocklist(user_id);
CREATE INDEX IF NOT EXISTS idx_blocklist_status ON blocklist(status);
CREATE INDEX IF NOT EXISTS idx_blocklist_blocked_at ON blocklist(blocked_at);

CREATE INDEX IF NOT EXISTS idx_fraud_logs_user_id ON fraud_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_fraud_logs_action ON fraud_logs(action);
CREATE INDEX IF NOT EXISTS idx_fraud_logs_timestamp ON fraud_logs(timestamp);

CREATE INDEX IF NOT EXISTS idx_receipts_hash ON receipts(receipt_hash);
CREATE INDEX IF NOT EXISTS idx_receipts_transaction_id ON receipts(transaction_id);
CREATE INDEX IF NOT EXISTS idx_receipts_verified ON receipts(verified);

CREATE INDEX IF NOT EXISTS idx_fraud_scores_transaction_id ON fraud_scores(transaction_id);
CREATE INDEX IF NOT EXISTS idx_fraud_scores_risk_level ON fraud_scores(risk_level);
CREATE INDEX IF NOT EXISTS idx_fraud_scores_scored_at ON fraud_scores(scored_at);

-- Insert sample data for testing
INSERT INTO transactions (transaction_id, user_id, amount, timestamp, location, device_id, payment_method, merchant_category, risk_score, flagged) VALUES
('TXN_001234', 'user_789', 2450.00, '2024-01-15 14:23:45', 'Store 1523', 'device_abc123', 'credit_card', 'electronics', 0.94, true),
('TXN_001235', 'user_456', 89.99, '2024-01-15 14:25:12', 'Store 0892', 'device_def456', 'debit_card', 'grocery', 0.23, false),
('TXN_001236', 'user_123', 1200.00, '2024-01-15 14:26:33', 'Store 2156', 'device_ghi789', 'mobile_pay', 'clothing', 0.67, true);

INSERT INTO blocklist (user_id, device_id, reason, risk_score, blocked_by, block_type) VALUES
('user_789', 'device_abc123', 'Fraudulent transaction pattern', 0.94, 'fraud_analyst', 'permanent'),
('user_456', 'device_def456', 'Multiple failed payment attempts', 0.87, 'auto_system', 'temporary'),
('user_123', 'device_ghi789', 'Suspicious refund activity', 0.76, 'fraud_analyst', 'under_review');

INSERT INTO fraud_logs (transaction_id, user_id, user_id_hash, action, risk_score, blockchain_tx, metadata) VALUES
('TXN_001234', 'user_789', 'hash_user_789', 'USER_BLOCKED', 0.94, '0x1a2b3c4d5e6f7890', '{"reason": "High risk transaction"}'),
('TXN_001235', 'user_456', 'hash_user_456', 'FRAUD_DETECTED', 0.87, '0x2b3c4d5e6f789012', '{"flags": ["unusual_amount", "new_device"]}'),
('TXN_001236', 'user_123', 'hash_user_123', 'ALERT_TRIGGERED', 0.76, '0x3c4d5e6f78901234', '{"alert_type": "medium_risk"}');

INSERT INTO receipts (receipt_hash, transaction_id, amount, store, timestamp, verified, blockchain_hash) VALUES
('hash_001234', 'TXN_001234', 89.99, 'Store 1523', '2024-01-15 14:23:45', true, '0x1234567890abcdef'),
('hash_001235', 'TXN_001235', 156.78, 'Store 0892', '2024-01-15 13:15:30', true, '0x2345678901bcdefg'),
('hash_001236', 'TXN_001236', 234.56, 'Store 2156', '2024-01-15 12:05:22', false, '0x3456789012cdefgh');

-- Enable Row Level Security (RLS) if needed
-- ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE blocklist ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE fraud_logs ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE receipts ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE fraud_scores ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE fraud_explanations ENABLE ROW LEVEL SECURITY;

-- Create policies for RLS (uncomment if using authentication)
-- CREATE POLICY "Enable read access for authenticated users" ON transactions FOR SELECT USING (auth.role() = 'authenticated');
-- CREATE POLICY "Enable insert access for authenticated users" ON transactions FOR INSERT WITH CHECK (auth.role() = 'authenticated');

COMMENT ON TABLE transactions IS 'Stores all transaction data for fraud analysis';
COMMENT ON TABLE blocklist IS 'Manages blocked users and devices';
COMMENT ON TABLE fraud_logs IS 'Immutable log of fraud events and actions';
COMMENT ON TABLE receipts IS 'Receipt verification data with blockchain hashes';
COMMENT ON TABLE fraud_scores IS 'ML model scoring results';
COMMENT ON TABLE fraud_explanations IS 'AI-generated explanations for fraud decisions';