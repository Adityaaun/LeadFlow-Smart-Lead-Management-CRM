import {
  LeadListItem,
  LeadDetail,
  CreateLeadPayload,
  LeadStatus,
  CreateDiscussionPayload,
  Discussion,
} from '@/types';

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorDetail = response.statusText;
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.detail || JSON.stringify(errorJson);
    } catch {
      // fallback to statusText
    }
    throw new ApiError(errorDetail, response.status);
  }

  return response.json();
}

export const api = {
  getLeads: async (status?: string, search?: string): Promise<LeadListItem[]> => {
    const params = new URLSearchParams();
    if (status && status !== 'All') {
      params.append('status', status);
    }
    if (search && search.trim()) {
      params.append('search', search.trim());
    }
    const query = params.toString() ? `?${params.toString()}` : '';
    return request<LeadListItem[]>(`/leads${query}`);
  },

  getTodayFollowUps: async (): Promise<LeadListItem[]> => {
    return request<LeadListItem[]>('/leads/today-followups');
  },

  getLead: async (id: number): Promise<LeadDetail> => {
    return request<LeadDetail>(`/leads/${id}`);
  },

  createLead: async (payload: CreateLeadPayload): Promise<LeadDetail> => {
    return request<LeadDetail>('/leads', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },

  updateLeadStatus: async (
    id: number,
    status: LeadStatus
  ): Promise<LeadDetail> => {
    return request<LeadDetail>(`/leads/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    });
  },

  addDiscussion: async (
    leadId: number,
    payload: CreateDiscussionPayload
  ): Promise<Discussion> => {
    return request<Discussion>(`/leads/${leadId}/discussions`, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },
};
