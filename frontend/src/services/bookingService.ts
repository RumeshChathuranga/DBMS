import api from './api';
import type { Booking, BookingCreate, BookingFilters, ApiResponse, Room } from '../types';

class BookingService {
  async getBookings(filters?: BookingFilters): Promise<Booking[]> {
    return await api.get<Booking[]>('/reservations', filters);
  }

  async getBookingById(id: number): Promise<Booking> {
    return await api.get<Booking>(`/reservations/${id}`);
  }

  async createBooking(data: BookingCreate): Promise<ApiResponse> {
    return await api.post<ApiResponse>('/reservations', data);
  }

  async updateBooking(id: number, data: Partial<BookingCreate>): Promise<ApiResponse> {
    return await api.put<ApiResponse>(`/reservations/${id}`, data);
  }

  async cancelBooking(id: number): Promise<ApiResponse> {
    return await api.delete<ApiResponse>(`/reservations/${id}`);
  }

  async checkIn(id: number): Promise<ApiResponse> {
    return await api.post<ApiResponse>(`/reservations/${id}/check-in`);
  }

  async checkOut(id: number): Promise<ApiResponse> {
    return await api.post<ApiResponse>(`/reservations/${id}/check-out`);
  }

  async checkAvailability(
    branchID: number,
    typeID: number,
    checkInDate: string,
    checkOutDate: string
  ): Promise<Room[]> {
    return await api.post<Room[]>('/rooms/availability', {
      branchID,
      typeID,
      checkInDate,
      checkOutDate,
    });
  }

  async getTodaysCheckIns(branchId: number): Promise<Booking[]> {
    return await api.get<Booking[]>('/reservations/today/check-ins', { branch_id: branchId });
  }

  async getTodaysCheckOuts(branchId: number): Promise<Booking[]> {
    return await api.get<Booking[]>('/reservations/today/check-outs', { branch_id: branchId });
  }
}

export default new BookingService();