import api from './api';
import type { Service, ServiceUsage, ServiceUsageCreate, ApiResponse } from '../types';

class ServiceService {
  async getAllServices(): Promise<Service[]> {
    console.log('Fetching all services');
    const result = await api.get<Service[]>('/services');
    console.log('Services fetched:', result);
    return result;
  }

  async getServiceById(id: number): Promise<Service> {
    return await api.get<Service>(`/services/${id}`);
  }

  async createServiceUsage(data: ServiceUsageCreate): Promise<ApiResponse> {
    console.log('Creating service usage:', data);
    return await api.post<ApiResponse>('/services/usage', data);
  }

  async getServicesByBooking(bookingId: number): Promise<ServiceUsage[]> {
    console.log('Fetching services for booking:', bookingId);
    const result = await api.get<ServiceUsage[]>(`/services/usage/booking/${bookingId}`);
    console.log('Service usages:', result);
    return result;
  }
}

export default new ServiceService();