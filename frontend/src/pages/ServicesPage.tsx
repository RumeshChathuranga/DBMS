import { useState, useEffect } from 'react';
import { MainLayout } from '../components/layout';
import { Card, Button, Modal, Input, Table } from '../components/common';
import { Plus, Utensils } from 'lucide-react';
import { serviceService, bookingService } from '../services';
import type { Service, ServiceUsageCreate, Booking } from '../types';
import { toast } from 'react-toastify';

const ServicesPage = () => {
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [bookingSearch, setBookingSearch] = useState('');
  const [selectedBooking, setSelectedBooking] = useState<Booking | null>(null);
  
  const [formData, setFormData] = useState<ServiceUsageCreate>({
    bookingID: 0,
    serviceID: 0,
    quantity: 1,
  });

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = async () => {
    try {
      setLoading(true);
      const data = await serviceService.getAllServices();
      setServices(data);
    } catch (error) {
      toast.error('Failed to fetch services');
    } finally {
      setLoading(false);
    }
  };

  const handleSearchBooking = async () => {
    if (!bookingSearch) {
      toast.warning('Please enter a booking ID');
      return;
    }

    try {
      const booking = await bookingService.getBookingById(Number(bookingSearch));
      if (booking.bookingStatus !== 'CheckedIn' && booking.bookingStatus !== 'Booked') {
        toast.error('Can only add services to active bookings');
        return;
      }
      setSelectedBooking(booking);
      setFormData({ ...formData, bookingID: booking.bookingID });
    } catch (error: any) {
      toast.error('Booking not found');
      setSelectedBooking(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedBooking) {
      toast.error('Please select a booking first');
      return;
    }

    if (!formData.serviceID) {
      toast.error('Please select a service');
      return;
    }

    try {
      await serviceService.createServiceUsage(formData);
      toast.success('Service added successfully');
      setShowModal(false);
      resetForm();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to add service');
    }
  };

  const resetForm = () => {
    setFormData({ bookingID: 0, serviceID: 0, quantity: 1 });
    setBookingSearch('');
    setSelectedBooking(null);
  };

  const columns = [
    {
      key: 'serviceType',
      header: 'Service Type',
    },
    {
      key: 'unit',
      header: 'Unit',
      render: (service: Service) => service.unit || 'N/A',
    },
    {
      key: 'ratePerUnit',
      header: 'Rate',
      render: (service: Service) => `LKR ${service.ratePerUnit.toLocaleString()}`,
    },
  ];

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Services</h1>
            <p className="text-gray-600 mt-1">Manage hotel services</p>
          </div>
          <Button
            variant="primary"
            icon={<Plus size={20} />}
            onClick={() => setShowModal(true)}
          >
            Add Service to Booking
          </Button>
        </div>

        {/* Available Services */}
        <Card title="Available Services">
          <Table
            data={services}
            columns={columns}
            loading={loading}
            emptyMessage="No services available"
          />
        </Card>

        {/* Add Service Modal */}
        <Modal
          isOpen={showModal}
          onClose={() => {
            setShowModal(false);
            resetForm();
          }}
          title="Add Service to Booking"
        >
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Booking Search */}
            <div>
              <label className="label">Find Booking</label>
              <div className="flex gap-2">
                <input
                  type="number"
                  placeholder="Enter Booking ID"
                  value={bookingSearch}
                  onChange={(e) => setBookingSearch(e.target.value)}
                  className="input-field"
                />
                <Button type="button" variant="secondary" onClick={handleSearchBooking}>
                  Search
                </Button>
              </div>
            </div>

            {/* Selected Booking Info */}
            {selectedBooking && (
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-sm font-medium text-green-900">
                  Booking #{selectedBooking.bookingID}
                </p>
                <p className="text-sm text-green-700">
                  Guest: {selectedBooking.firstName} {selectedBooking.lastName}
                </p>
                <p className="text-sm text-green-700">
                  Room: {selectedBooking.roomNo} - {selectedBooking.typeName}
                </p>
              </div>
            )}

            {/* Service Selection */}
            <div>
              <label className="label">Select Service</label>
              <select
                value={formData.serviceID}
                onChange={(e) => setFormData({ ...formData, serviceID: Number(e.target.value) })}
                className="input-field"
                required
              >
                <option value="">Choose a service...</option>
                {services.map((service) => (
                  <option key={service.serviceID} value={service.serviceID}>
                    {service.serviceType} - LKR {service.ratePerUnit} {service.unit && `per ${service.unit}`}
                  </option>
                ))}
              </select>
            </div>

            {/* Quantity */}
            <Input
              label="Quantity"
              type="number"
              min="1"
              value={formData.quantity}
              onChange={(e) => setFormData({ ...formData, quantity: Number(e.target.value) })}
              required
            />

            {/* Total Calculation */}
            {formData.serviceID > 0 && (
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm font-medium text-blue-900">
                  Total: LKR{' '}
                  {(
                    (services.find((s) => s.serviceID === formData.serviceID)?.ratePerUnit || 0) *
                    formData.quantity
                  ).toLocaleString()}
                </p>
              </div>
            )}

            <div className="flex gap-3 pt-4">
              <Button type="submit" variant="primary" className="flex-1">
                Add Service
              </Button>
              <Button
                type="button"
                variant="secondary"
                onClick={() => {
                  setShowModal(false);
                  resetForm();
                }}
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

export default ServicesPage;