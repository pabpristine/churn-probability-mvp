import type { Client, ClientListParams, ClientListResponse, ClientAnalysisResponse } from '@/types';
import apiClient from './api/axios.instance';

export class ClientService {
  /**
   * Fetch paginated and filtered clients
   */
  static async getClients(params: ClientListParams): Promise<ClientListResponse> {
    const { data } = await apiClient.get<Client[]>('/clients', {
      params: {
        search: params.search,
        status: params.status,
        riskLevel: params.riskLevel,
        tier: params.tier,
        sortBy: params.sortBy,
        sortOrder: params.sortOrder,
      }
    });

    let filtered = [...data];

    // Pagination
    const page = params.page || 1;
    const pageSize = params.pageSize || 20;
    const total = filtered.length;
    const totalPages = Math.ceil(total / pageSize);
    const start = (page - 1) * pageSize;
    const paginatedData = filtered.slice(start, start + pageSize);

    return {
      data: paginatedData,
      total,
      page,
      pageSize,
      totalPages,
    };
  }

  /**
   * Fetch single client by ID
   */
  static async getClient(id: string): Promise<Client> {
    const { data } = await apiClient.get<Client>(`/clients/${id}`);
    return data;
  }

  /**
   * Fetch client KPIs
   */
  static async getKPIs(id: string): Promise<{ data: any[] }> {
    const { data } = await apiClient.get<any[]>(`/clients/${id}/kpis`);
    return { data };
  }

  /**
   * Fetch client Analysis
   */
  static async getAnalysis(id: string): Promise<{ data: any }> {
    const { data } = await apiClient.get<any>(`/clients/${id}/analysis`);
    return { data: data.data };
  }

  /**
   * Fetch client History
   */
  static async getHistory(id: string): Promise<{ data: any[] }> {
    const { data } = await apiClient.get<any[]>(`/clients/${id}/history`);
    return { data };
  }

  /**
   * Run full AI Churn analysis with a text query
   */
  static async runAnalysis(userQuery: string): Promise<ClientAnalysisResponse> {
    const { data } = await apiClient.post<ClientAnalysisResponse>('/client-analysis', {
      user_query: userQuery,
    });
    return data;
  }
}


