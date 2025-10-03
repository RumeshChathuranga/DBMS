import api from './api';
import type { Guest, GuestCreate, ApiResponse } from '../types';

class GuestService {
  async createGuest(data: GuestCreate): Promise<ApiResponse> {
    return await api.post<ApiResponse>('/guests', data);
  }

  async getGuestById(id: number): Promise<Guest> {
    return await api.get<Guest>(`/guests/${id}`);
  }

  async searchGuests(query: string, page = 1, pageSize = 20): Promise<Guest[]> {
    return await api.get<Guest[]>('/guests', { query, page, page_size: pageSize });
  }

  async updateGuest(id: number, data: Partial<GuestCreate>): Promise<ApiResponse> {
    return await api.put<ApiResponse>(`/guests/${id}`, data);
  }
}

export default new GuestService();