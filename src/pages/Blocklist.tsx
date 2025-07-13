import React, { useState } from 'react';
import { UserX, Search, AlertTriangle, Clock } from 'lucide-react';

const Blocklist: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const blockedUsers = [
    {
      id: 'user_789',
      reason: 'Fraudulent transaction pattern',
      blockedAt: '2024-01-15 14:23:45',
      riskScore: 0.94,
      deviceId: 'device_abc123',
      lastActivity: '2024-01-15 14:20:12',
      status: 'permanent',
    },
    {
      id: 'user_456',
      reason: 'Multiple failed payment attempts',
      blockedAt: '2024-01-15 13:15:30',
      riskScore: 0.87,
      deviceId: 'device_def456',
      lastActivity: '2024-01-15 13:10:45',
      status: 'temporary',
    },
    {
      id: 'user_123',
      reason: 'Suspicious refund activity',
      blockedAt: '2024-01-15 12:05:22',
      riskScore: 0.76,
      deviceId: 'device_ghi789',
      lastActivity: '2024-01-15 12:00:11',
      status: 'under_review',
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'permanent':
        return 'bg-red-100 text-red-800';
      case 'temporary':
        return 'bg-yellow-100 text-yellow-800';
      case 'under_review':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredUsers = blockedUsers.filter(
    (user) =>
      user.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.reason.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Blocked Users & Devices</h1>
        <p className="text-gray-600">Manage and monitor blocked users and devices</p>
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center space-x-4">
          <div className="flex-1 relative">
            <Search className="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search by user ID or reason..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-walmart-blue focus:border-transparent"
            />
          </div>
          <button className="px-4 py-2 bg-walmart-blue text-white rounded-lg hover:bg-blue-700">
            Add to Blocklist
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <UserX className="h-8 w-8 text-red-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Blocked</p>
              <p className="text-2xl font-bold text-gray-900">342</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <AlertTriangle className="h-8 w-8 text-yellow-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Under Review</p>
              <p className="text-2xl font-bold text-gray-900">23</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <Clock className="h-8 w-8 text-blue-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Temporary Blocks</p>
              <p className="text-2xl font-bold text-gray-900">67</p>
            </div>
          </div>
        </div>
      </div>

      {/* Blocklist Table */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Blocked Users</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  User ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Reason
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Risk Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Blocked At
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredUsers.map((user) => (
                <tr key={user.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{user.id}</div>
                      <div className="text-sm text-gray-500">{user.deviceId}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-900">{user.reason}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {(user.riskScore * 100).toFixed(1)}%
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(
                        user.status
                      )}`}
                    >
                      {user.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {user.blockedAt}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button className="text-walmart-blue hover:text-blue-700 mr-3">
                      Review
                    </button>
                    <button className="text-red-600 hover:text-red-700">
                      Unblock
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Blocklist;