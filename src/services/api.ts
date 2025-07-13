const API_BASE_URL = 'http://localhost:8000/api';

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

// Upload API
export const uploadTransactionFile = async (file: File): Promise<ApiResponse<any>> => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'Upload failed' };
  }
};

// Scoring API
export interface ScoreRequest {
  transaction_id: string;
  user_id: string;
  amount: number;
  location: string;
  device_id?: string;
  timestamp?: string;
}

export interface ScoreResponse {
  transaction_id: string;
  risk_score: number;
  risk_level: 'low' | 'medium' | 'high';
  flags: string[];
  confidence: number;
  model_version: string;
}

export const scoreTransaction = async (request: ScoreRequest): Promise<ApiResponse<ScoreResponse>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/score`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'Scoring failed' };
  }
};

// Explanation API
export interface ExplanationRequest {
  transaction_id: string;
  risk_score: number;
  flags: string[];
  transaction_data: Record<string, any>;
}

export interface ExplanationResponse {
  transaction_id: string;
  explanation: string;
  key_factors: string[];
  recommendations: string[];
  generated_at: string;
}

export const explainFraudDecision = async (request: ExplanationRequest): Promise<ApiResponse<ExplanationResponse>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/explain`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'Explanation failed' };
  }
};

// Blocklist API
export interface BlockUserRequest {
  user_id: string;
  device_id?: string;
  reason: string;
  risk_score: number;
  blocked_by: string;
  block_type?: string;
}

export const blockUser = async (request: BlockUserRequest): Promise<ApiResponse<any>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/block-user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'Block user failed' };
  }
};

export const getBlocklist = async (params?: { limit?: number; offset?: number; search?: string }): Promise<ApiResponse<any[]>> => {
  try {
    const queryParams = new URLSearchParams();
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.offset) queryParams.append('offset', params.offset.toString());
    if (params?.search) queryParams.append('search', params.search);

    const response = await fetch(`${API_BASE_URL}/blocklist?${queryParams}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'Get blocklist failed' };
  }
};

// Blockchain API
export interface BlockchainLogRequest {
  user_id_hash: string;
  risk_score: number;
  action: string;
  metadata?: Record<string, any>;
}

export const logToBlockchain = async (request: BlockchainLogRequest): Promise<ApiResponse<any>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/log-to-blockchain`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'Blockchain logging failed' };
  }
};

export const getBlockchainLogs = async (params?: { limit?: number; offset?: number }): Promise<ApiResponse<any[]>> => {
  try {
    const queryParams = new URLSearchParams();
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.offset) queryParams.append('offset', params.offset.toString());

    const response = await fetch(`${API_BASE_URL}/blockchain/logs?${queryParams}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'Get blockchain logs failed' };
  }
};

// Report API
export interface ReportRequest {
  report_type: string;
  date_range: string;
  start_date?: string;
  end_date?: string;
  filters?: Record<string, any>;
}

export const generateReport = async (request: ReportRequest): Promise<ApiResponse<any>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/generate-report`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'Report generation failed' };
  }
};

// Receipt Verification API
export interface VerifyReceiptRequest {
  receipt_hash?: string;
  transaction_id?: string;
  qr_data?: string;
}

export const verifyReceipt = async (request: VerifyReceiptRequest): Promise<ApiResponse<any>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/verify-receipt`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { data };
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'Receipt verification failed' };
  }
};