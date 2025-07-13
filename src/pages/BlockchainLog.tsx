import React from 'react';
import { Link as ChainIcon, ExternalLink, Clock, Shield } from 'lucide-react';

const BlockchainLog: React.FC = () => {
  const blockchainLogs = [
    {
      id: '0x1a2b3c4d5e6f',
      userIdHash: '0xabcd1234...',
      riskScore: 0.94,
      action: 'USER_BLOCKED',
      timestamp: '2024-01-15 14:23:45',
      blockNumber: 12345678,
      gasUsed: '21000',
      txHash: '0x9876543210abcdef...',
    },
    {
      id: '0x2b3c4d5e6f7a',
      userIdHash: '0xefgh5678...',
      riskScore: 0.87,
      action: 'FRAUD_DETECTED',
      timestamp: '2024-01-15 13:15:30',
      blockNumber: 12345677,
      gasUsed: '21000',
      txHash: '0x1234567890fedcba...',
    },
    {
      id: '0x3c4d5e6f7a8b',
      userIdHash: '0xijkl9012...',
      riskScore: 0.76,
      action: 'ALERT_TRIGGERED',
      timestamp: '2024-01-15 12:05:22',
      blockNumber: 12345676,
      gasUsed: '21000',
      txHash: '0xabcdef1234567890...',
    },
  ];

  const getActionColor = (action: string) => {
    switch (action) {
      case 'USER_BLOCKED':
        return 'bg-red-100 text-red-800';
      case 'FRAUD_DETECTED':
        return 'bg-yellow-100 text-yellow-800';
      case 'ALERT_TRIGGERED':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Blockchain Transaction Log</h1>
        <p className="text-gray-600">Immutable record of fraud events stored on-chain</p>
      </div>

      {/* Blockchain Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <ChainIcon className="h-8 w-8 text-walmart-blue" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Logs</p>
              <p className="text-2xl font-bold text-gray-900">1,247</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <Shield className="h-8 w-8 text-green-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Verified</p>
              <p className="text-2xl font-bold text-gray-900">100%</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <Clock className="h-8 w-8 text-blue-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Latest Block</p>
              <p className="text-2xl font-bold text-gray-900">12345678</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <ExternalLink className="h-8 w-8 text-purple-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Network</p>
              <p className="text-lg font-bold text-gray-900">Polygon</p>
            </div>
          </div>
        </div>
      </div>

      {/* Blockchain Logs Table */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Recent Blockchain Entries</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Transaction Hash
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  User Hash
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Action
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Risk Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Block Number
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Timestamp
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  View
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {blockchainLogs.map((log) => (
                <tr key={log.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-mono text-gray-900">
                      {log.txHash.slice(0, 16)}...
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-mono text-gray-500">
                      {log.userIdHash.slice(0, 12)}...
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getActionColor(
                        log.action
                      )}`}
                    >
                      {log.action.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {(log.riskScore * 100).toFixed(1)}%
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{log.blockNumber}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {log.timestamp}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button className="text-walmart-blue hover:text-blue-700 flex items-center">
                      <ExternalLink className="h-4 w-4 mr-1" />
                      Explorer
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Contract Info */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Smart Contract Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Contract Address</h4>
            <p className="text-sm font-mono text-gray-600 bg-gray-50 p-2 rounded">
              0x1234567890abcdef1234567890abcdef12345678
            </p>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Network</h4>
            <p className="text-sm text-gray-600">Polygon Mumbai Testnet</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlockchainLog;