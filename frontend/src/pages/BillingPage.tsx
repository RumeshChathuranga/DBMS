import { useEffect, useMemo, useState } from "react";
import { MainLayout } from "../components/layout";
import { Card, Button, Input, Modal, Badge } from "../components/common";
import { DollarSign, FileText, CreditCard } from "lucide-react";
import { billingService, bookingService } from "../services";
import type { Invoice, Payment, PaymentMethod } from "../types";
import { toast } from "react-toastify";
import { format } from "date-fns";
import { useLocation } from "react-router-dom";

const BillingPage = () => {
  const [bookingSearch, setBookingSearch] = useState("");
  const [invoice, setInvoice] = useState<Invoice | null>(null);
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(false);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const location = useLocation();
  const bookingIdFromQuery = useMemo(() => {
    const params = new URLSearchParams(location.search);
    const id = params.get("bookingId");
    return id ? Number(id) : undefined;
  }, [location.search]);

  const [paymentData, setPaymentData] = useState<{
    invoiceID: number;
    paymentMethod: PaymentMethod;
    amount: string;
  }>({
    invoiceID: 0,
    paymentMethod: "Cash",
    amount: "",
  });

  const handleSearchInvoice = async (overrideId?: number | string) => {
    const idToSearch = overrideId ?? bookingSearch;
    if (!idToSearch) {
      toast.warning("Please enter a booking ID");
      return;
    }

    try {
      setLoading(true);

      // Get booking to verify it exists and is checked out
      const booking = await bookingService.getBookingById(Number(idToSearch));

      if (
        booking.bookingStatus !== "CheckedOut" &&
        booking.bookingStatus !== "CheckedIn"
      ) {
        toast.warning(
          "Invoice can only be generated for checked-in or checked-out bookings"
        );
        return;
      }

      // Try to get existing invoice or generate new one
      try {
        const invoiceData = await billingService.getInvoiceByBooking(
          Number(idToSearch)
        );
        setInvoice(invoiceData);

        // Get payments
        const paymentsData = await billingService.getPaymentsByInvoice(
          invoiceData.invoiceID
        );
        setPayments(paymentsData);
      } catch (error: any) {
        if (error.response?.status === 404) {
          // Generate invoice if it doesn't exist
          await billingService.generateInvoice(Number(idToSearch));
          const invoiceData = await billingService.getInvoiceByBooking(
            Number(idToSearch)
          );
          setInvoice(invoiceData);
          setPayments([]);
          toast.success("Invoice generated successfully");
        } else {
          throw error;
        }
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "Failed to fetch invoice");
      setInvoice(null);
      setPayments([]);
    } finally {
      setLoading(false);
    }
  };

  // If a bookingId is provided in the query string, auto load the invoice
  useEffect(() => {
    if (bookingIdFromQuery) {
      const idStr = String(bookingIdFromQuery);
      if (bookingSearch !== idStr) setBookingSearch(idStr);
      // Trigger load when query changes
      (async () => {
        await handleSearchInvoice(bookingIdFromQuery);
      })();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [bookingIdFromQuery]);

  const handleProcessPayment = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!invoice) {
      toast.error("No invoice selected");
      return;
    }

    const amount = parseFloat(paymentData.amount);
    if (isNaN(amount) || amount <= 0) {
      toast.error("Please enter a valid amount");
      return;
    }

    if (amount > (invoice.balanceDue || 0)) {
      toast.error("Payment amount cannot exceed balance due");
      return;
    }

    try {
      await billingService.processPayment({
        invoiceID: invoice.invoiceID,
        paymentMethod: paymentData.paymentMethod,
        amount: amount,
      });

      toast.success("Payment processed successfully");
      setShowPaymentModal(false);
      setPaymentData({ invoiceID: 0, paymentMethod: "Cash", amount: "" });

      // Refresh invoice
      handleSearchInvoice();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || "Payment failed");
    }
  };

  const getStatusBadge = (status: string) => {
    const variants: Record<string, "success" | "warning" | "danger" | "info"> =
      {
        Paid: "success",
        "Partially Paid": "warning",
        Pending: "info",
        Cancelled: "danger",
      };
    return <Badge variant={variants[status] || "info"}>{status}</Badge>;
  };

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Billing</h1>
          <p className="text-gray-600 mt-1">
            Process payments and manage invoices
          </p>
        </div>

        {/* Search */}
        <Card>
          <div className="flex gap-4">
            <div className="flex-1">
              <Input
                type="number"
                placeholder="Enter Booking ID to view/generate invoice"
                value={bookingSearch}
                onChange={(e) => setBookingSearch(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSearchInvoice()}
              />
            </div>
            <Button
              variant="primary"
              onClick={() => handleSearchInvoice()}
              loading={loading}
            >
              Search
            </Button>
          </div>
        </Card>

        {/* Invoice Details */}
        {invoice && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Invoice Summary */}
            <Card className="lg:col-span-2">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">
                    Invoice #{invoice.invoiceID}
                  </h2>
                  <p className="text-gray-600">Booking #{invoice.bookingID}</p>
                </div>
                {getStatusBadge(invoice.invoiceStatus)}
              </div>

              <div className="space-y-4">
                {/* Charges Breakdown */}
                <div className="space-y-2">
                  <div className="flex justify-between py-2 border-b">
                    <span className="text-gray-600">Room Charges:</span>
                    <span className="font-medium">
                      LKR {invoice.roomCharges.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between py-2 border-b">
                    <span className="text-gray-600">Service Charges:</span>
                    <span className="font-medium">
                      LKR {invoice.serviceCharges.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between py-2 border-b">
                    <span className="text-gray-600">Tax Amount:</span>
                    <span className="font-medium">
                      LKR {invoice.taxAmount.toLocaleString()}
                    </span>
                  </div>
                  {invoice.discountAmount > 0 && (
                    <div className="flex justify-between py-2 border-b text-green-600">
                      <span>Discount:</span>
                      <span className="font-medium">
                        - LKR {invoice.discountAmount.toLocaleString()}
                      </span>
                    </div>
                  )}
                  <div className="flex justify-between py-3 border-t-2 border-gray-800">
                    <span className="text-lg font-bold">Total Amount:</span>
                    <span className="text-lg font-bold">
                      LKR {invoice.totalAmount?.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between py-2 bg-blue-50 px-3 rounded">
                    <span className="text-blue-900">Amount Paid:</span>
                    <span className="font-medium text-blue-900">
                      LKR {invoice.settledAmount.toLocaleString()}
                    </span>
                  </div>
                  <div className="flex justify-between py-2 bg-red-50 px-3 rounded">
                    <span className="text-red-900 font-medium">
                      Balance Due:
                    </span>
                    <span className="font-bold text-red-900">
                      LKR {invoice.balanceDue?.toLocaleString()}
                    </span>
                  </div>
                </div>

                {/* Action Button */}
                {invoice.invoiceStatus !== "Paid" &&
                  invoice.invoiceStatus !== "Cancelled" && (
                    <Button
                      variant="primary"
                      size="lg"
                      className="w-full mt-4"
                      onClick={() => {
                        setPaymentData({
                          ...paymentData,
                          invoiceID: invoice.invoiceID,
                          amount: invoice.balanceDue?.toString() || "0",
                        });
                        setShowPaymentModal(true);
                      }}
                      icon={<CreditCard size={20} />}
                    >
                      Process Payment
                    </Button>
                  )}
              </div>
            </Card>

            {/* Payment History */}
            <Card>
              <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                <FileText size={20} />
                Payment History
              </h3>
              {payments.length === 0 ? (
                <p className="text-gray-500 text-center py-8">
                  No payments yet
                </p>
              ) : (
                <div className="space-y-3">
                  {payments.map((payment) => (
                    <div
                      key={payment.transactionID}
                      className="p-3 bg-gray-50 rounded-lg"
                    >
                      <div className="flex justify-between items-start mb-1">
                        <span className="text-sm font-medium">
                          {payment.paymentMethod}
                        </span>
                        <span className="font-bold text-green-600">
                          LKR {payment.amount.toLocaleString()}
                        </span>
                      </div>
                      <p className="text-xs text-gray-600">
                        {format(
                          new Date(payment.transactionDate),
                          "MMM dd, yyyy"
                        )}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </Card>
          </div>
        )}

        {/* Payment Modal */}
        <Modal
          isOpen={showPaymentModal}
          onClose={() => setShowPaymentModal(false)}
          title="Process Payment"
        >
          <form onSubmit={handleProcessPayment} className="space-y-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-900 font-medium">
                Balance Due: LKR {invoice?.balanceDue?.toLocaleString()}
              </p>
            </div>

            <div>
              <label className="label">Payment Method</label>
              <select
                value={paymentData.paymentMethod}
                onChange={(e) =>
                  setPaymentData({
                    ...paymentData,
                    paymentMethod: e.target.value as PaymentMethod,
                  })
                }
                className="input-field"
                required
              >
                <option value="Cash">Cash</option>
                <option value="Card">Credit/Debit Card</option>
                <option value="Online">Online Transfer</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <Input
              label="Payment Amount (LKR)"
              type="number"
              step="0.01"
              min="0.01"
              max={invoice?.balanceDue}
              value={paymentData.amount}
              onChange={(e) =>
                setPaymentData({ ...paymentData, amount: e.target.value })
              }
              required
            />

            <div className="flex gap-3 pt-4">
              <Button
                type="submit"
                variant="success"
                className="flex-1"
                icon={<DollarSign size={20} />}
              >
                Confirm Payment
              </Button>
              <Button
                type="button"
                variant="secondary"
                onClick={() => setShowPaymentModal(false)}
              >
                Cancel
              </Button>
            </div>
          </form>
        </Modal>
      </div>
    </MainLayout>
  );
};

export default BillingPage;
