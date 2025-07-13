import React from 'react';
import { TrendingUp, Shield, AlertTriangle, Users } from 'lucide-react';

const Dashboard: React.FC = () => {
  const stats = [
    {
      name: 'Total Transactions',
      value: '2.4M',
      change: '+12%',
      changeType: 'positive',
      icon: TrendingUp,
    },
    {
      name: 'Fraud Detected',
      value: '1,247',
      change: '-3%',
      changeType: 'negative',
      icon: Shield,
    },
    {
      name: 'High Risk Alerts',
      value: '89',
      change: '+5%',
      changeType: 'positive',
      icon: AlertTriangle,
    },
    {
      name: 'Blocked Users',
      value: '342',
      change: '+8%',
      changeType: 'positive',
      icon: Users,
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Fraud Detection Dashboard</h1>
        <p className="text-gray-600">Real-time overview of fraud prevention metrics</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <stat.icon className="h-8 w-8 text-walmart-blue" />
              </div>
              <div className="ml-4 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">{stat.name}</dt>
                  <dd className="flex items-baseline">
                    <div className="text-2xl font-semibold text-gray-900">{stat.value}</div>
                    <div
                      className={`ml-2 flex items-baseline text-sm font-semibold ${
                        stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                      }`}
                    >
                      {stat.change}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Charts Placeholder */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Score Trends</h3>
          <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
            <span className="text-gray-500">Chart visualization will be implemented</span>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Regional Risk Analysis</h3>
          <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
            <span className="text-gray-500">Geographic heatmap will be implemented</span>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Recent Fraud Alerts</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {[1, 2, 3].map((item) => (
              <div key={item} className="flex items-center space-x-4 p-4 bg-red-50 rounded-lg">
                <div className="flex-shrink-0">
                  <AlertTriangle className="h-5 w-5 text-red-500" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">
                    High-risk transaction detected
                  </p>
                  <p className="text-sm text-gray-500">
                    User ID: usr_789, Amount: $2,450, Risk Score: 0.94
                  </p>
                </div>
                <div className="text-sm text-gray-500">2 min ago</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;