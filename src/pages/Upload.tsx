import React, { useState } from 'react';
import { Upload as UploadIcon, FileText, CheckCircle } from 'lucide-react';
import { uploadTransactionFile } from '../services/api';

const Upload: React.FC = () => {
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileUpload(e.target.files[0]);
    }
  };

  const handleFileUpload = async (file: File) => {
    setUploadedFile(file);
    setIsUploading(true);
    setError(null);
    setUploadResult(null);

    const result = await uploadTransactionFile(file);
    
    setIsUploading(false);
    
    if (result.error) {
      setError(result.error);
    } else {
      setUploadResult(result.data);
    }
  };

  const handleProcessData = async () => {
    if (!uploadResult) return;
    
    // Navigate to fraud detection page or trigger processing
    alert('Data processing started! Check the Fraud Detection page for results.');
  };
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Upload Transaction Data</h1>
        <p className="text-gray-600">Upload CSV files for fraud analysis and processing</p>
      </div>

      {/* Upload Area */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive
              ? 'border-walmart-blue bg-blue-50'
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          {isUploading ? (
            <div className="space-y-4">
              <div className="animate-spin h-12 w-12 border-4 border-walmart-blue border-t-transparent rounded-full mx-auto"></div>
              <div>
                <p className="text-lg font-medium text-gray-900">Processing file...</p>
                <p className="text-gray-500">Please wait while we analyze your data</p>
              </div>
            </div>
          ) : uploadedFile && uploadResult ? (
            <div className="space-y-4">
              <CheckCircle className="h-12 w-12 text-green-500 mx-auto" />
              <div>
                <p className="text-lg font-medium text-gray-900">File uploaded successfully</p>
                <p className="text-gray-500">{uploadedFile.name}</p>
                <p className="text-sm text-gray-400">
                  {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
                <p className="text-sm text-green-600 mt-2">
                  {uploadResult.total_records} records processed
                </p>
              </div>
            </div>
          ) : error ? (
            <div className="space-y-4">
              <div className="h-12 w-12 bg-red-100 rounded-full flex items-center justify-center mx-auto">
                <span className="text-red-600 text-xl">✕</span>
              </div>
              <div>
                <p className="text-lg font-medium text-red-900">Upload failed</p>
                <p className="text-red-600 text-sm">{error}</p>
              </div>
              <button
                onClick={() => {
                  setError(null);
                  setUploadedFile(null);
                  setUploadResult(null);
                }}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
              >
                Try Again
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <UploadIcon className="h-12 w-12 text-gray-400 mx-auto" />
              <div>
                <p className="text-lg font-medium text-gray-900">
                  Drag and drop your CSV file here
                </p>
                <p className="text-gray-500">or click to browse</p>
              </div>
              <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-walmart-blue hover:bg-blue-700 cursor-pointer"
              >
                Select File
              </label>
            </div>
          )}
        </div>
      </div>

      {/* Preview Section */}
      {uploadResult && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <FileText className="h-5 w-5 mr-2" />
              Data Preview
            </h3>
          </div>
          <div className="p-6">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    {uploadResult.columns?.map((column: string) => (
                      <th key={column} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        {column}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {uploadResult.preview?.map((row: any, index: number) => (
                    <tr key={index}>
                      {uploadResult.columns?.map((column: string) => (
                        <td key={column} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {row[column]}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="mt-4 flex justify-end space-x-3">
              <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50">
                Cancel
              </button>
              <button 
                onClick={handleProcessData}
                className="px-4 py-2 bg-walmart-blue text-white rounded-md hover:bg-blue-700"
              >
                Process Data
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Upload;