import React from 'react';
import { TrendingUp, Shield, AlertTriangle, Users } from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts';
import { ComposableMap, Geographies, Geography } from 'react-simple-maps';
import { feature } from 'topojson-client';
import worldData from 'world-atlas/countries-110m.json';

const geoFeatures = feature(
  worldData as any,
  (worldData as any).objects.countries
).features;

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

  const riskTrendData = [
    { time: '9 AM', score: 0.12 },
    { time: '10 AM', score: 0.25 },
    { time: '11 AM', score: 0.31 },
    { time: '12 PM', score: 0.48 },
    { time: '1 PM', score: 0.61 },
    { time: '2 PM', score: 0.72 },
    { time: '3 PM', score: 0.54 },
    { time: '4 PM', score: 0.43 },
  ];

  const regionRiskData: Record<string, number> = {
    IN: 0.85,
    US: 0.4,
    CN: 0.65,
    BR: 0.2,
    RU: 0.55,
  };

  const isoAlpha2Map: Record<number, string> = {
    356: 'IN',
    840: 'US',
    156: 'CN',
    76: 'BR',
    643: 'RU',
  };

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

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Score Trends</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={riskTrendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis domain={[0, 1]} />
                <Tooltip />
                <Line type="monotone" dataKey="score" stroke="#0D6EFD" strokeWidth={2} dot />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Regional Risk Analysis</h3>
          <div className="h-64">
            <ComposableMap projectionConfig={{ scale: 120 }}>
              <Geographies geography={geoFeatures}>
                {({ geographies }) =>
                  geographies.map((geo) => {
                    const numericCode = geo.id;
                    const alpha2 = isoAlpha2Map[numericCode];
                    const risk = alpha2 ? regionRiskData[alpha2] : undefined;
                    const fill = risk ? `rgba(255, 0, 0, ${risk})` : '#DDD';

                    return (
                      <Geography
                        key={geo.rsmKey}
                        geography={geo}
                        style={{
                          default: { fill, outline: 'none' },
                          hover: { fill: '#F53', outline: 'none' },
                          pressed: { fill: '#E42', outline: 'none' },
                        }}
                      />
                    );
                  })
                }
              </Geographies>
            </ComposableMap>
          </div>
        </div>
      </div>

      {/* Recent Alerts */}
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
                  <p className="text-sm font-medium text-gray-900">High-risk transaction detected</p>
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
