import api from "./api";
import type {
  Booking,
  BookingCreate,
  BookingFilters,
  ApiResponse,
  Room,
} from "../types";

class BookingService {
  async getBookings(filters?: BookingFilters): Promise<Booking[]> {
    console.log("Fetching bookings with filters:", filters);
    const result = await api.get<Booking[]>("/reservations", filters);
    console.log("Bookings fetched:", result);
    return result;
  }

  async getBookingById(id: number): Promise<Booking> {
    return await api.get<Booking>(`/reservations/${id}`);
  }

  async createBooking(data: BookingCreate): Promise<ApiResponse> {
    return await api.post<ApiResponse>("/reservations", data);
  }

  async updateBooking(
    id: number,
    data: Partial<BookingCreate>
  ): Promise<ApiResponse> {
    return await api.put<ApiResponse>(`/reservations/${id}`, data);
  }

  async cancelBooking(id: number): Promise<ApiResponse> {
    return await api.delete<ApiResponse>(`/reservations/${id}`);
  }

  async checkIn(id: number): Promise<ApiResponse> {
    console.log("Checking in booking:", id);
    try {
      const result = await api.post<ApiResponse>(
        `/reservations/${id}/check-in`
      );
      console.log("Check-in result:", result);
      return result;
    } catch (error: any) {
      console.error("Check-in error:", error);
      console.error("Error response:", error.response?.data);
      throw error;
    }
  }

  async checkOut(id: number): Promise<ApiResponse> {
    console.log("Checking out booking:", id);
    console.log("Making POST request to:", `/reservations/${id}/check-out`);
    try {
      const result = await api.post<ApiResponse>(
        `/reservations/${id}/check-out`,
        {}
      );
      console.log("Check-out result:", result);
      return result;
    } catch (error: any) {
      console.error("Check-out error:", error);
      console.error("Error response:", error.response);
      console.error("Error data:", error.response?.data);
      console.error("Error status:", error.response?.status);
      throw error;
    }
  }

  async checkAvailability(
    branchID: number,
    typeID: number,
    checkInDate: string,
    checkOutDate: string
  ): Promise<Room[]> {
    console.log("Checking availability:", {
      branchID,
      typeID,
      checkInDate,
      checkOutDate,
    });
    const result = await api.post<Room[]>("/rooms/availability", {
      branchID,
      typeID,
      checkInDate,
      checkOutDate,
    });
    console.log("Available rooms:", result);
    return result;
  }

  async getTodaysCheckIns(branchId: number): Promise<Booking[]> {
    return await api.get<Booking[]>("/reservations/today/check-ins", {
      branch_id: branchId,
    });
  }

  async getTodaysCheckOuts(branchId: number): Promise<Booking[]> {
    return await api.get<Booking[]>("/reservations/today/check-outs", {
      branch_id: branchId,
    });
  }

  async getRecentActivities(
    limit: number = 10,
    branchId?: number
  ): Promise<any[]> {
    const params: any = { limit };
    if (branchId) params.branch_id = branchId;
    return await api.get<any[]>("/reports/recent-activities", params);
  }
}

export default new BookingService();
