// User & Auth Types
export interface User {
  userID: number;
  username: string;
  userRole: 'Admin' | 'Manager' | 'Reception' | 'Staff';
  branchID: number | null;
  first_name: string;
  last_name: string;
  email: string | null;
  phone: string | null;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Guest Types
export interface Guest {
  guestID: number;
  firstName: string;
  lastName: string;
  phone: string;
  email: string | null;
  idNumber: string;
}

export interface GuestCreate {
  firstName: string;
  lastName: string;
  phone: string;
  email?: string;
  idNumber: string;
}

// Branch Types
export interface Branch {
  branchID: number;
  branchLocation: string;
  rating: number | null;
  phone: string;
  email: string;
}

// Room Types
export interface RoomType {
  typeID: number;
  typeName: string;
  capacity: number;
  currRate: number;
}

export interface Room {
  roomID: number;
  branchID: number;
  typeID: number;
  roomNo: number;
  roomStatus: 'Available' | 'Occupied';
  typeName?: string;
  capacity?: number;
  currRate?: number;
  branchLocation?: string;
}

// Booking Types
export type BookingStatus = 'Booked' | 'CheckedIn' | 'CheckedOut' | 'Cancelled';

export interface Booking {
  bookingID: number;
  guestID: number;
  branchID: number;
  roomID: number;
  rate: number;
  checkInDate: string;
  checkOutDate: string;
  numGuests: number;
  bookingStatus: BookingStatus;
  firstName?: string;
  lastName?: string;
  phone?: string;
  email?: string;
  roomNo?: number;
  typeName?: string;
  branchLocation?: string;
  nights?: number;
  bookingReference?: string;
}

export interface BookingCreate {
  guestID: number;
  branchID: number;
  roomID: number;
  checkInDate: string;
  checkOutDate: string;
  numGuests: number;
}

// Service Types
export interface Service {
  serviceID: number;
  serviceType: string;
  unit: string | null;
  ratePerUnit: number;
}

export interface ServiceUsage {
  usageID: number;
  bookingID: number;
  serviceID: number;
  rate: number;
  quantity: number;
  usedAt: string;
  serviceType?: string;
  unit?: string;
  totalCharge?: number;
}

export interface ServiceUsageCreate {
  bookingID: number;
  serviceID: number;
  quantity: number;
}

// Invoice & Payment Types
export type InvoiceStatus = 'Pending' | 'Partially Paid' | 'Paid' | 'Cancelled';
export type PaymentMethod = 'Cash' | 'Card' | 'Online' | 'Other';

export interface Invoice {
  invoiceID: number;
  bookingID: number;
  policyID: number | null;
  discountCode: number | null;
  paymentPlan: 'Full' | 'Installment';
  roomCharges: number;
  serviceCharges: number;
  taxAmount: number;
  discountAmount: number;
  settledAmount: number;
  invoiceStatus: InvoiceStatus;
  totalAmount?: number;
  balanceDue?: number;
}

export interface Payment {
  transactionID: number;
  invoiceID: number;
  transactionDate: string;
  paymentMethod: PaymentMethod;
  amount: number;
}

export interface PaymentCreate {
  invoiceID: number;
  paymentMethod: PaymentMethod;
  amount: number;
}

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
}

export interface PaginatedResponse<T> {
  items: T[];
  pagination: {
    current_page: number;
    page_size: number;
    total_items: number;
    total_pages: number;
    has_next: boolean;
    has_previous: boolean;
  };
}

// Report Types
export interface OccupancyReport {
  branchID: number;
  branchLocation: string;
  occupiedRooms: number;
  totalRooms: number;
  occupancyRate: number;
}

export interface RevenueReport {
  branchID: number;
  branchLocation: string;
  roomRevenue: number;
  serviceRevenue: number;
  totalRevenue: number;
  totalBookings: number;
}

export interface ServiceUsageReport {
  serviceType: string;
  unit: string;
  usageCount: number;
  totalQuantity: number;
  totalRevenue: number;
  avgRevenuePerUse: number;
}

// Form Validation Types
export interface ValidationError {
  field: string;
  message: string;
}

// Filter & Query Types
export interface BookingFilters {
  branchID?: number;
  status?: BookingStatus;
  page?: number;
  page_size?: number;
}

export interface DateRange {
  startDate: string;
  endDate: string;
}