import { api } from './api';

export interface CampaignCreatePayload {
  name: string;
  client_id: string;
  type: string;
  status?: string;
  start_date?: string;
  end_date?: string;
  budget?: number;
  spent_amount?: number;
  target_audience?: string;
  description?: string;
  manager_id?: string;
}

export interface CampaignUpdatePayload extends Partial<CampaignCreatePayload> {}

export interface CampaignRead {
  id: string;
  name: string;
  client_id: string;
  type: string;
  status: string;
  start_date: string | null;
  end_date: string | null;
  budget: number | null;
  spent_amount: number;
  target_audience: string | null;
  description: string | null;
  manager_id: string | null;
  created_at: string;
  updated_at: string;
}

export const campaignService = {
  getAll: async (params?: {
    page?: number;
    page_size?: number;
    search?: string;
    status?: string;
    type?: string;
    client_id?: string;
    manager_id?: string;
  }) => {
    const { data } = await api.get('/campaigns', { params });
    return data;
  },

  getById: async (id: string): Promise<CampaignRead> => {
    const { data } = await api.get(`/campaigns/${id}`);
    return data;
  },

  create: async (payload: CampaignCreatePayload): Promise<CampaignRead> => {
    const { data } = await api.post('/campaigns', payload);
    return data;
  },

  update: async (id: string, payload: CampaignUpdatePayload): Promise<CampaignRead> => {
    const { data } = await api.put(`/campaigns/${id}`, payload);
    return data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/campaigns/${id}`);
  },

  getPlatforms: async (campaignId: string) => {
    const { data } = await api.get(`/campaigns/${campaignId}/platforms`);
    return data;
  },

  addPlatform: async (campaignId: string, payload: {
    platform_name: string;
    account_id?: string;
    status?: string;
    budget_allocation?: number;
  }) => {
    const { data } = await api.post(`/campaigns/${campaignId}/platforms`, payload);
    return data;
  },

  getAssets: async (campaignId: string) => {
    const { data } = await api.get(`/campaigns/${campaignId}/assets`);
    return data;
  },

  addAsset: async (campaignId: string, payload: {
    name: string;
    asset_type: string;
    file_url?: string;
    status?: string;
  }) => {
    const { data } = await api.post(`/campaigns/${campaignId}/assets`, payload);
    return data;
  },

  getMetrics: async (campaignId: string) => {
    const { data } = await api.get(`/campaigns/${campaignId}/metrics`);
    return data;
  },

  addMetric: async (campaignId: string, payload: {
    date: string;
    impressions?: number;
    clicks?: number;
    conversions?: number;
    spend?: number;
  }) => {
    const { data } = await api.post(`/campaigns/${campaignId}/metrics`, payload);
    return data;
  },
};
