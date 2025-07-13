import React, { useState } from 'react';
import { QrCode, Search, CheckCircle, AlertCircle, Camera } from 'lucide-react';
import { verifyReceipt, VerifyReceiptRequest } from '../services/api';

const ReceiptVerification: React.FC = () => {
  const [verificationMethod, setVerificationMethod] = useState<'qr' | 'manual'>('qr');
  const [receiptHash, setReceiptHash] = useState('');
  const [verificationResult, setVerificationResult] = useState<any>(null);
  const [isVerifying, setIsVerifying] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleVerification = async () => {
    if (!receiptHash.trim()) {
      setError('Please enter a receipt hash or transaction ID');
      return;
    }

    setIsVerifying(true);
    setError(null);
    setVerificationResult(null);

    const request: VerifyReceiptRequest = {
      receipt_hash: receiptHash.startsWith('TXN_') ? undefined : receiptHash,
      transaction_id: receiptHash.startsWith('TXN_') ? receiptHash : undefined,
    };

    const result = await verifyReceipt(request);
    setIsVerifying(false);

    if (result.error) {
      setError(result.error);
    } else {
      setVerificationResult(result.data);
    }
  };

  const handleQRScan = async (qrData: string) => {
    setIsVerifying(true);
    setError(null);
    setVerificationResult(null);

    const request: VerifyReceiptRequest = {
      qr_data: qrData,
    };

    const result = await verifyReceipt(request);
    setIsVerifying(false);

    if (result.error) {
      setError(result.error);
    } else {
      setVerificationResult(result.data);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Receipt Verification</h1>
        <p className="text-gray-600">Verify purchase authenticity using blockchain technology</p>
      </div>

      {/* Verification Method Selection */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Verification Method</h3>
        <div className="flex space-x-4">
          <button
            onClick={() => setVerificationMethod('qr')}
            className={`flex items-center px-4 py-2 rounded-lg border ${
              verificationMethod === 'qr'
                ? 'bg-walmart-blue text-white border-walmart-blue'
                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
            }`}
          >
            <QrCode className="h-5 w-5 mr-2" />
            QR Code Scan
          </button>
          <button
            onClick={() => setVerificationMethod('manual')}
            className={`flex items-center px-4 py-2 rounded-lg border ${
              verificationMethod === 'manual'
                ? 'bg-walmart-blue text-white border-walmart-blue'
                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
            }`}
          >
            <Search className="h-5 w-5 mr-2" />
            Manual Entry
          </button>
        </div>
      </div>

      {/* Verification Interface */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        {verificationMethod === 'qr' ? (
          <div className="text-center space-y-6">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-12">
              <Camera className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h4 className="text-lg font-medium text-gray-900 mb-2">
                Scan Receipt QR Code
              </h4>
              <p className="text-gray-500 mb-6">
                Position the QR code within the camera frame
              </p>
              <button 
                onClick={() => {
                  // Mock QR scan for demo
                  const mockQRData = JSON.stringify({
                    transaction_id: 'TXN_001234',
                    amount: 89.99,
                    timestamp: '2024-01-15T14:23:45Z',
                    store: 'Store 1523',
                    hash: '0x1234567890abcdef...'
                  });
                  handleQRScan(mockQRData);
                }}
                disabled={isVerifying}
                className="px-6 py-3 bg-walmart-blue text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {isVerifying ? 'Scanning...' : 'Start Camera (Demo)'}
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Receipt Hash or Transaction ID
              </label>
              <div className="flex space-x-4">
                <input
                  type="text"
                  value={receiptHash}
                  onChange={(e) => setReceiptHash(e.target.value)}
                  placeholder="Enter receipt hash or transaction ID..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-walmart-blue focus:border-transparent"
                />
                <button
                  onClick={handleVerification}
                  disabled={isVerifying}
                  className="px-6 py-2 bg-walmart-blue text-white rounded-lg hover:bg-blue-700"
                >
                  {isVerifying ? 'Verifying...' : 'Verify'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-white rounded-lg shadow-sm border border-red-200 p-6">
          <div className="flex items-center mb-4">
            <AlertCircle className="h-8 w-8 text-red-500 mr-3" />
            <h3 className="text-lg font-semibold text-red-900">Verification Error</h3>
          </div>
          <p className="text-red-700">{error}</p>
          <button
            onClick={() => {
              setError(null);
              setReceiptHash('');
            }}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            Try Again
          </button>
        </div>
      )}

      {/* Verification Result */}
      {verificationResult && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center mb-4">
            {verificationResult.is_valid ? (
              <CheckCircle className="h-8 w-8 text-green-500 mr-3" />
            ) : (
              <AlertCircle className="h-8 w-8 text-red-500 mr-3" />
            )}
            <h3 className="text-lg font-semibold text-gray-900">
              {verificationResult.is_valid ? 'Receipt Verified' : 'Verification Failed'}
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-3">Transaction Details</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Transaction ID:</span>
                  <span className="font-mono">{verificationResult.transaction_id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Amount:</span>
                  <span>${verificationResult.amount}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Store:</span>
                  <span>{verificationResult.store}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Timestamp:</span>
                  <span>{verificationResult.timestamp}</span>
                </div>
              </div>
            </div>

            <div>
              <h4 className="font-medium text-gray-900 mb-3">Blockchain Verification</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Status:</span>
                  <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                    verificationResult.is_valid ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {verificationResult.status}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Blockchain Hash:</span>
                  <span className="font-mono text-xs">
                    {verificationResult.blockchain_hash?.slice(0, 16)}...
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Network:</span>
                  <span>Polygon</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Confirmations:</span>
                  <span>{verificationResult.confirmations}</span>
                </div>
              </div>
            </div>
          </div>

          {verificationResult.is_valid && (
            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="flex">
                  <CheckCircle className="h-5 w-5 text-green-400 mt-0.5" />
                  <div className="ml-3">
                    <h4 className="text-sm font-medium text-green-800">
                      Verification Successful
                    </h4>
                    <p className="text-sm text-green-700 mt-1">
                      This receipt is authentic and has been verified on the blockchain.
                      The transaction details match the immutable record.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Recent Verifications */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Recent Verifications</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {[1, 2, 3].map((item) => (
              <div key={item} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-4">
                  <CheckCircle className="h-5 w-5 text-green-500" />
                  <div>
                    <p className="font-medium">TXN_00{item}234</p>
                    <p className="text-sm text-gray-500">Store 152{item} • $89.99</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-green-600">Verified</p>
                  <p className="text-xs text-gray-500">2 hours ago</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReceiptVerification;