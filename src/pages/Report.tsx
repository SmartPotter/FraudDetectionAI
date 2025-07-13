import React, { useState } from 'react';
import { FileText, Download, Calendar, Filter } from 'lucide-react';
import { generateReport, ReportRequest } from '../services/api';

const Report: React.FC = () => {
  const [dateRange, setDateRange] = useState('7d');
  const [reportType, setReportType] = useState('summary');
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateReport = async () => {
    setIsGenerating(true);
    setError(null);

    const request: ReportRequest = {
      report_type: reportType,
      date_range: dateRange,
      filters: {}
    };

    const result = await generateReport(request);
    setIsGenerating(false);

    if (result.error) {
      setError(result.error);
    } else {
      // Handle successful report generation
      alert(`Report generated successfully! Download URL: ${result.data?.download_url}`);
      // In a real app, you might trigger a download or show a success message
    }
  };
  const reports = [
    {
      id: 'RPT_001',
      name: 'Weekly Fraud Summary',
      type: 'summary',
      generatedAt: '2024-01-15 14:00:00',
      size: '2.3 MB',
      transactions: 15420,
      fraudDetected: 89,
    },
    {
      id: 'RPT_002',
      name: 'High-Risk User Analysis',
      type: 'analysis',
      generatedAt: '2024-01-15 10:30:00',
      size: '1.8 MB',
      transactions: 8960,
      fraudDetected: 156,
    },
    {
      id: 'RPT_003',
      name: 'Blockchain Audit Log',
      type: 'audit',
      generatedAt: '2024-01-14 18:45:00',
      size: '3.1 MB',
      transactions: 22340,
      fraudDetected: 234,
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Fraud Reports</h1>
        <p className="text-gray-600">Generate and download comprehensive fraud analysis reports</p>
      </div>

      {/* Report Generation */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Generate New Report</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Report Type
            </label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-walmart-blue focus:border-transparent"
            >
              <option value="summary">Fraud Summary</option>
              <option value="detailed">Detailed Analysis</option>
              <option value="blockchain">Blockchain Audit</option>
              <option value="user-risk">User Risk Assessment</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Date Range
            </label>
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-walmart-blue focus:border-transparent"
            >
              <option value="1d">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="90d">Last 90 Days</option>
              <option value="custom">Custom Range</option>
            </select>
          </div>
          <div className="flex items-end">
            <button 
              onClick={handleGenerateReport}
              disabled={isGenerating}
              className="w-full px-4 py-2 bg-walmart-blue text-white rounded-lg hover:bg-blue-700 flex items-center justify-center disabled:opacity-50"
            >
              <FileText className="h-4 w-4 mr-2" />
              {isGenerating ? 'Generating...' : 'Generate Report'}
            </button>
          </div>
        </div>
        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-700">Error: {error}</p>
          </div>
        )}
      </div>

      {/* Report Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <FileText className="h-8 w-8 text-walmart-blue" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Reports</p>
              <p className="text-2xl font-bold text-gray-900">124</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <Download className="h-8 w-8 text-green-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Downloads</p>
              <p className="text-2xl font-bold text-gray-900">89</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <Calendar className="h-8 w-8 text-blue-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">This Week</p>
              <p className="text-2xl font-bold text-gray-900">12</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <Filter className="h-8 w-8 text-purple-500" />
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Avg Size</p>
              <p className="text-2xl font-bold text-gray-900">2.1 MB</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Reports */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Recent Reports</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Report Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Transactions
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Fraud Detected
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Generated
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Size
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {reports.map((report) => (
                <tr key={report.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{report.name}</div>
                      <div className="text-sm text-gray-500">{report.id}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                      {report.type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {report.transactions.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {report.fraudDetected}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {report.generatedAt}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {report.size}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button className="text-walmart-blue hover:text-blue-700 flex items-center">
                      <Download className="h-4 w-4 mr-1" />
                      Download
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

export default Report;