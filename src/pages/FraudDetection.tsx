import React, { useState } from 'react';
import { Shield, AlertCircle, Info, CheckCircle } from 'lucide-react';
import { scoreTransaction, explainFraudDecision, blockUser, logToBlockchain, ScoreRequest, ExplanationRequest, BlockUserRequest, BlockchainLogRequest } from '../services/api';

const FraudDetection: React.FC = () => {
  const [selectedTransaction, setSelectedTransaction] = useState<any>(null);
  const [isScoring, setIsScoring] = useState(false);
  const [isExplaining, setIsExplaining] = useState(false);
  const [isBlocking, setIsBlocking] = useState(false);
  const [explanation, setExplanation] = useState<any>(null);
  const [newTransactionData, setNewTransactionData] = useState({
    transaction_id: '',
    user_id: '',
    amount: '',
    location: '',
    device_id: ''
  });

  const transactions = [
    {
      id: 'TXN_001234',
      userId: 'user_789',
      amount: 2450.00,
      riskScore: 0.94,
      status: 'high-risk',
      location: 'Store 1523',
      timestamp: '2024-01-15 14:23:45',
      flags: ['Unusual amount', 'New device', 'High velocity'],
    },
    {
      id: 'TXN_001235',
      userId: 'user_456',
      amount: 89.99,
      riskScore: 0.23,
      status: 'low-risk',
      location: 'Store 0892',
      timestamp: '2024-01-15 14:25:12',
      flags: [],
    },
    {
      id: 'TXN_001236',
      userId: 'user_123',
      amount: 1200.00,
      riskScore: 0.67,
      status: 'medium-risk',
      location: 'Store 2156',
      timestamp: '2024-01-15 14:26:33',
      flags: ['Large refund', 'Weekend transaction'],
    },
  ];

  const getRiskColor = (score: number) => {
    if (score >= 0.8) return 'bg-red-100 text-red-800 border-red-200';
    if (score >= 0.5) return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    return 'bg-green-100 text-green-800 border-green-200';
  };

  const getRiskIcon = (score: number) => {
    if (score >= 0.8) return AlertCircle;
    if (score >= 0.5) return Info;
    return CheckCircle;
  };

  const handleScoreTransaction = async () => {
    if (!newTransactionData.transaction_id || !newTransactionData.user_id || !newTransactionData.amount) {
      alert('Please fill in all required fields');
      return;
    }

    setIsScoring(true);
    
    const scoreRequest: ScoreRequest = {
      transaction_id: newTransactionData.transaction_id,
      user_id: newTransactionData.user_id,
      amount: parseFloat(newTransactionData.amount),
      location: newTransactionData.location,
      device_id: newTransactionData.device_id || undefined,
      timestamp: new Date().toISOString()
    };

    const result = await scoreTransaction(scoreRequest);
    setIsScoring(false);

    if (result.error) {
      alert(`Scoring failed: ${result.error}`);
    } else {
      alert(`Risk Score: ${(result.data!.risk_score * 100).toFixed(1)}% (${result.data!.risk_level})`);
      // Add to transactions list
      const newTransaction = {
        id: newTransactionData.transaction_id,
        userId: newTransactionData.user_id,
        amount: parseFloat(newTransactionData.amount),
        riskScore: result.data!.risk_score,
        status: result.data!.risk_level + '-risk',
        location: newTransactionData.location,
        timestamp: new Date().toLocaleString(),
        flags: result.data!.flags,
      };
      // You could update the transactions state here
    }
  };

  const handleExplainTransaction = async (transaction: any) => {
    setIsExplaining(true);
    setSelectedTransaction(transaction);
    
    const explanationRequest: ExplanationRequest = {
      transaction_id: transaction.id,
      risk_score: transaction.riskScore,
      flags: transaction.flags,
      transaction_data: {
        amount: transaction.amount,
        user_id: transaction.userId,
        location: transaction.location,
        timestamp: transaction.timestamp
      }
    };

    const result = await explainFraudDecision(explanationRequest);
    setIsExplaining(false);

    if (result.error) {
      alert(`Explanation failed: ${result.error}`);
    } else {
      setExplanation(result.data);
    }
  };

  const handleBlockUser = async (transaction: any) => {
    setIsBlocking(true);
    
    const blockRequest: BlockUserRequest = {
      user_id: transaction.userId,
      device_id: transaction.deviceId,
      reason: `High risk transaction: ${transaction.flags.join(', ')}`,
      risk_score: transaction.riskScore,
      blocked_by: 'fraud_analyst',
      block_type: 'permanent'
    };

    const blockResult = await blockUser(blockRequest);
    
    if (blockResult.data) {
      // Log to blockchain
      const blockchainRequest: BlockchainLogRequest = {
        user_id_hash: `hash_${transaction.userId}`,
        risk_score: transaction.riskScore,
        action: 'USER_BLOCKED',
        metadata: {
          transaction_id: transaction.id,
          reason: blockRequest.reason
        }
      };
      
      await logToBlockchain(blockchainRequest);
    }
    
    setIsBlocking(false);
    
    if (blockResult.error) {
      alert(`Block failed: ${blockResult.error}`);
    } else {
      alert('User blocked successfully and logged to blockchain');
      setSelectedTransaction(null);
    }
  };
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Real-time Fraud Detection</h1>
        <p className="text-gray-600">Monitor and analyze transactions for fraudulent activity</p>
      </div>

      {/* Manual Transaction Scoring */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Score New Transaction</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <input
            type="text"
            placeholder="Transaction ID"
            value={newTransactionData.transaction_id}
            onChange={(e) => setNewTransactionData({...newTransactionData, transaction_id: e.target.value})}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-walmart-blue focus:border-transparent"
          />
          <input
            type="text"
            placeholder="User ID"
            value={newTransactionData.user_id}
            onChange={(e) => setNewTransactionData({...newTransactionData, user_id: e.target.value})}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-walmart-blue focus:border-transparent"
          />
          <input
            type="number"
            placeholder="Amount"
            value={newTransactionData.amount}
            onChange={(e) => setNewTransactionData({...newTransactionData, amount: e.target.value})}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-walmart-blue focus:border-transparent"
          />
          <input
            type="text"
            placeholder="Location"
            value={newTransactionData.location}
            onChange={(e) => setNewTransactionData({...newTransactionData, location: e.target.value})}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-walmart-blue focus:border-transparent"
          />
          <input
            type="text"
            placeholder="Device ID (optional)"
            value={newTransactionData.device_id}
            onChange={(e) => setNewTransactionData({...newTransactionData, device_id: e.target.value})}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-walmart-blue focus:border-transparent"
          />
          <button
            onClick={handleScoreTransaction}
            disabled={isScoring}
            className="px-4 py-2 bg-walmart-blue text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {isScoring ? 'Scoring...' : 'Score Transaction'}
          </button>
        </div>
      </div>
      {/* Real-time Feed */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <Shield className="h-5 w-5 mr-2 text-walmart-blue" />
            Live Transaction Feed
          </h3>
          <div className="flex items-center space-x-2">
            <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-500">Live</span>
          </div>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {transactions.map((transaction) => {
              const RiskIcon = getRiskIcon(transaction.riskScore);
              return (
                <div
                  key={transaction.id}
                  className={`p-4 rounded-lg border cursor-pointer transition-all hover:shadow-md ${getRiskColor(
                    transaction.riskScore
                  )}`}
                  onClick={() => handleExplainTransaction(transaction)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <RiskIcon className="h-6 w-6" />
                      <div>
                        <p className="font-semibold">{transaction.id}</p>
                        <p className="text-sm opacity-75">
                          {transaction.userId} • ${transaction.amount}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-lg">
                        {(transaction.riskScore * 100).toFixed(0)}%
                      </p>
                      <p className="text-sm opacity-75">Risk Score</p>
                    </div>
                  </div>
                  {transaction.flags.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-2">
                      {transaction.flags.map((flag) => (
                        <span
                          key={flag}
                          className="px-2 py-1 text-xs bg-white bg-opacity-50 rounded"
                        >
                          {flag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Explanation Modal */}
      {selectedTransaction && !isExplaining && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-lg w-full mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Fraud Analysis</h3>
              <button
                onClick={() => setSelectedTransaction(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                ×
              </button>
            </div>
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-gray-900">Transaction Details</h4>
                <div className="mt-2 space-y-1 text-sm text-gray-600">
                  <p>ID: {selectedTransaction.id}</p>
                  <p>Amount: ${selectedTransaction.amount}</p>
                  <p>Risk Score: {(selectedTransaction.riskScore * 100).toFixed(1)}%</p>
                  <p>Location: {selectedTransaction.location}</p>
                </div>
              </div>
              {explanation && (
                <div>
                  <h4 className="font-medium text-gray-900">AI Explanation</h4>
                  <p className="mt-2 text-sm text-gray-600">
                    {explanation.explanation}
                  </p>
                  <div className="mt-3">
                    <h5 className="font-medium text-gray-900">Key Factors:</h5>
                    <ul className="mt-1 text-sm text-gray-600">
                      {explanation.key_factors?.map((factor: string, index: number) => (
                        <li key={index}>• {factor}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => setSelectedTransaction(null)}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
                >
                  Close
                </button>
                <button 
                  onClick={() => handleBlockUser(selectedTransaction)}
                  disabled={isBlocking}
                  className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50"
                >
                  {isBlocking ? 'Blocking...' : 'Block User'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Loading Modal for Explanation */}
      {isExplaining && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-sm w-full mx-4 text-center">
            <div className="animate-spin h-8 w-8 border-4 border-walmart-blue border-t-transparent rounded-full mx-auto mb-4"></div>
            <p className="text-gray-600">Generating AI explanation...</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default FraudDetection;