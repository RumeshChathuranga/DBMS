import api from './api';
import type { Invoice, Payment, PaymentCreate, ApiResponse } from '../types';

class BillingService {
  async generateInvoice(bookingId: number, paymentPlan = 'Full'): Promise<ApiResponse> {
    console.log('Generating invoice for booking:', bookingId);
    return await api.post<ApiResponse>(`/billing/invoice/generate/${bookingId}`, {
      payment_plan: paymentPlan,
    });
  }

  async getInvoiceById(id: number): Promise<Invoice> {
    console.log('Fetching invoice:', id);
    const result = await api.get<Invoice>(`/billing/invoice/${id}`);
    console.log('Invoice:', result);
    return result;
  }

  async getInvoiceByBooking(bookingId: number): Promise<Invoice> {
    console.log('Fetching invoice for booking:', bookingId);
    const result = await api.get<Invoice>(`/billing/invoice/booking/${bookingId}`);
    console.log('Invoice:', result);
    return result;
  }

  async processPayment(data: PaymentCreate): Promise<ApiResponse> {
    console.log('Processing payment:', data);
    return await api.post<ApiResponse>('/billing/payment', data);
  }

  async getPaymentsByInvoice(invoiceId: number): Promise<Payment[]> {
    console.log('Fetching payments for invoice:', invoiceId);
    const result = await api.get<Payment[]>(`/billing/payment/invoice/${invoiceId}`);
    console.log('Payments:', result);
    return result;
  }

  async getPendingInvoices(branchId: number): Promise<Invoice[]> {
    console.log('Fetching pending invoices for branch:', branchId);
    const result = await api.get<Invoice[]>(`/billing/pending/${branchId}`);
    console.log('Pending invoices:', result);
    return result;
  }
}

export default new BillingService();