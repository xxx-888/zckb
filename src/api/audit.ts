import { api } from '@/lib/api';

export interface AuditItem {
  id: string;
  review_id: string;
  store_name: string | null;
  store_id?: string;
  user_name: string | null;
  user_avatar?: string | null;
  rating: number | null;
  content: string | null;
  platform: string | null;
  ai_reply: string | null;
  status: 'pending' | 'approved' | 'rejected' | 'sent';
  risk_level: string | null;
  scores: {
    realism: number;
    empathy: number;
    concreteness: number;
    consistency: number;
  } | null;
  reject_reason?: string | null;
  auditor_name?: string | null;
  reviewed_at?: string | null;
  created_at: string | null;
}

export interface AuditStats {
  pending_count: number;
  approved_count: number;
  rejected_count: number;
  sent_count: number;
  total_count: number;
  avg_processing_time: number | null;
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

  approveAudit: async (id: string): Promise<any> => {
    const response = await api.post(`/v1/audit/${id}/approve`, {});
    return response.data || response;
  },

  rejectAudit: async (id: string, reason: string): Promise<any> => {
    const response = await api.post(`/v1/audit/${id}/reject`, { reason });
    return response.data || response;
  },

  regenerateReply: async (id: string): Promise<any> => {
    const response = await api.post(`/v1/audit/${id}/regenerate`, {});
    return response.data || response;
  },

  getStats: async (): Promise<AuditStats> => {
    const response = await api.get<any>('/v1/audit/stats');
    return response.data || response;
  },
};
