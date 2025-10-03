import api from './api';
import type { Invoice, Payment, PaymentCreate, ApiResponse } from '../types';

class BillingService {
  async generateInvoice(bookingId: number, paymentPlan = 'Full'): Promise<ApiResponse> {
    return await api.post<ApiResponse>(`/billing/invoice/generate/${bookingId}`, {
      payment_plan: paymentPlan,
    });
  }

  async getInvoiceById(id: number): Promise<Invoice> {
    return await api.get<Invoice>(`/billing/invoice/${id}`);
  }

  async getInvoiceByBooking(bookingId: number): Promise<Invoice> {
    return await api.get<Invoice>(`/billing/invoice/booking/${bookingId}`);
  }

  async processPayment(data: PaymentCreate): Promise<ApiResponse> {
    return await api.post<ApiResponse>('/billing/payment', data);
  }

  async getPaymentsByInvoice(invoiceId: number): Promise<Payment[]> {
    return await api.get<Payment[]>(`/billing/payment/invoice/${invoiceId}`);
  }

  async getPendingInvoices(branchId: number): Promise<Invoice[]> {
    return await api.get<Invoice[]>(`/billing/pending/${branchId}`);
  }
}

export default new BillingService();