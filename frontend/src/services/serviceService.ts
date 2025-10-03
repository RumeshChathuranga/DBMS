import api from './api';
import type { Service, ServiceUsage, ServiceUsageCreate, ApiResponse } from '../types';

class ServiceService {
  async getAllServices(): Promise<Service[]> {
    return await api.get<Service[]>('/services');
  }

  async getServiceById(id: number): Promise<Service> {
    return await api.get<Service>(`/services/${id}`);
  }

  async createServiceUsage(data: ServiceUsageCreate): Promise<ApiResponse> {
    return await api.post<ApiResponse>('/services/usage', data);
  }

  async getServicesByBooking(bookingId: number): Promise<ServiceUsage[]> {
    return await api.get<ServiceUsage[]>(`/services/usage/booking/${bookingId}`);
  }
}

export default new ServiceService();