import { api } from '@/lib/api';

export interface AuditItem {
  id: string;
  review_id: string;
  store_name: string;
  user_name: string;
  rating: number;
  content: string;
  platform: string;
  ai_reply: string;
  status: 'pending' | 'approved' | 'rejected' | 'sent';
  risk_level: string;
  scores: {
    realism: number;
    empathy: number;
    concreteness: number;
    consistency: number;
  };
  reject_reason?: string;
  auditor_name?: string;
  reviewed_at?: string;
  created_at: string;
}

export interface AuditStats {
  pending_count: number;
  approved_count: number;
  rejected_count: number;
  total_count: number;
  avg_processing_time: number;
}

export const auditApi = {
  getAuditList: async (params?: {
    status?: string;
    keyword?: string;
    page?: number;
    limit?: number;
  }): Promise<{ items: AuditItem[]; total: number; page: number; pageSize: number }> => {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
          searchParams.append(key, String(value));
        }
      });
    }
    const response = await api.get<any>(`/v1/audit/list?${searchParams.toString()}`);
    return response.data || response;
  },

  getAuditById: async (id: string): Promise<AuditItem> => {
    const response = await api.get<any>(`/v1/audit/${id}`);
    return response.data || response;
  },

  approveAudit: async (id: string): Promise<void> => {
    const response = await api.post(`/v1/audit/${id}/approve`);
    return response.data;
  },

  rejectAudit: async (id: string, reason: string): Promise<void> => {
    const response = await api.post(`/v1/audit/${id}/reject`, { reason });
    return response.data;
  },

  regenerateReply: async (id: string): Promise<void> => {
    const response = await api.post(`/v1/audit/${id}/regenerate`);
    return response.data;
  },

  getStats: async (): Promise<AuditStats> => {
    const response = await api.get<any>('/v1/audit/stats');
    return response.data || response;
  },
};
