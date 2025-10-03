import { useState, useEffect } from 'react';
import { MainLayout } from '../components/layout';
import { Card, Button, Table, Badge, Modal, Input } from '../components/common';
import { Plus, Search, Calendar, CheckCircle, XCircle } from 'lucide-react';
import { bookingService, guestService, roomService } from '../services';
import type { Booking, BookingStatus, Guest, Room, RoomType } from '../types';
import { toast } from 'react-toastify';
import { format } from 'date-fns';

const ReservationsPage = () => {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<BookingStatus | 'All'>('All');
  const [selectedBooking, setSelectedBooking] = useState<Booking | null>(null);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [showNewBookingModal, setShowNewBookingModal] = useState(false);

  // New booking form state
  const [guests, setGuests] = useState<Guest[]>([]);
  const [roomTypes, setRoomTypes] = useState<RoomType[]>([]);
  const [availableRooms, setAvailableRooms] = useState<Room[]>([]);
  const [newBookingData, setNewBookingData] = useState({
    guestSearch: '',
    selectedGuest: null as Guest | null,
    branchID: 1,
    typeID: 0,
    roomID: 0,
    checkInDate: '',
    checkOutDate: '',
    numGuests: 1,
  });

  // Fetch bookings
  const fetchBookings = async () => {
    try {
      setLoading(true);
      const data = await bookingService.getBookings({
        status: statusFilter !== 'All' ? statusFilter : undefined,
      });
      console.log('Fetched bookings:', data);
      setBookings(data);
    } catch (error: any) {
      console.error('Error fetching bookings:', error);
      toast.error('Failed to fetch bookings');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookings();
  }, [statusFilter]);

  // Fetch room types when modal opens
  useEffect(() => {
    if (showNewBookingModal) {
      fetchRoomTypes();
    }
  }, [showNewBookingModal]);

  const fetchRoomTypes = async () => {
    try {
      const types = await roomService.getRoomTypes();
      setRoomTypes(types);
    } catch (error) {
      toast.error('Failed to fetch room types');
    }
  };

  // Search guest
  const handleGuestSearch = async () => {
    if (newBookingData.guestSearch.length < 2) {
      toast.warning('Enter at least 2 characters');
      return;
    }

    try {
      const results = await guestService.searchGuests(newBookingData.guestSearch);
      setGuests(results);
      if (results.length === 0) {
        toast.info('No guests found. Please create a new guest first.');
      }
    } catch (error) {
      toast.error('Failed to search guests');
    }
  };

  // Check availability
  const checkAvailability = async () => {
    if (!newBookingData.checkInDate || !newBookingData.checkOutDate || !newBookingData.typeID) {
      toast.warning('Please select dates and room type');
      return;
    }

    try {
      const rooms = await bookingService.checkAvailability(
        newBookingData.branchID,
        newBookingData.typeID,
        newBookingData.checkInDate,
        newBookingData.checkOutDate
      );
      setAvailableRooms(rooms);
      
      if (rooms.length === 0) {
        toast.warning('No rooms available for selected dates');
      } else {
        toast.success(`${rooms.length} rooms available`);
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to check availability');
    }
  };

  // Create booking
  const handleCreateBooking = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newBookingData.selectedGuest) {
      toast.error('Please select a guest');
      return;
    }

    if (!newBookingData.roomID) {
      toast.error('Please select a room');
      return;
    }

    try {
      await bookingService.createBooking({
        guestID: newBookingData.selectedGuest.guestID,
        branchID: newBookingData.branchID,
        roomID: newBookingData.roomID,
        checkInDate: newBookingData.checkInDate,
        checkOutDate: newBookingData.checkOutDate,
        numGuests: newBookingData.numGuests,
      });

      toast.success('Booking created successfully!');
      setShowNewBookingModal(false);
      resetNewBookingForm();
      fetchBookings();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to create booking');
    }
  };

  const resetNewBookingForm = () => {
    setNewBookingData({
      guestSearch: '',
      selectedGuest: null,
      branchID: 1,
      typeID: 0,
      roomID: 0,
      checkInDate: '',
      checkOutDate: '',
      numGuests: 1,
    });
    setGuests([]);
    setAvailableRooms([]);
  };

  // Handle check-in
  const handleCheckIn = async (bookingId: number) => {
    try {
      await bookingService.checkIn(bookingId);
      toast.success('Guest checked in successfully');
      fetchBookings();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Check-in failed');
    }
  };

  // Handle check-out
  const handleCheckOut = async (bookingId: number) => {
    try {
      await bookingService.checkOut(bookingId);
      toast.success('Guest checked out successfully');
      fetchBookings();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Check-out failed');
    }
  };

  // Handle cancel
  const handleCancel = async (bookingId: number) => {
    if (!confirm('Are you sure you want to cancel this booking?')) return;

    try {
      await bookingService.cancelBooking(bookingId);
      toast.success('Booking cancelled successfully');
      fetchBookings();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Cancellation failed');
    }
  };

  // Filter bookings
  const filteredBookings = bookings.filter((booking) => {
    const searchLower = searchQuery.toLowerCase();
    return (
      booking.firstName?.toLowerCase().includes(searchLower) ||
      booking.lastName?.toLowerCase().includes(searchLower) ||
      booking.phone?.includes(searchQuery) ||
      booking.roomNo?.toString().includes(searchQuery)
    );
  });

  // Get badge variant for status
  const getStatusBadge = (status: BookingStatus) => {
    const variants: Record<BookingStatus, 'success' | 'warning' | 'info' | 'danger'> = {
      Booked: 'info',
      CheckedIn: 'success',
      CheckedOut: 'warning',
      Cancelled: 'danger',
    };
    return <Badge variant={variants[status]}>{status}</Badge>;
  };

  // Table columns
  const columns = [
    {
      key: 'bookingID',
      header: 'Booking ID',
      render: (booking: Booking) => `#${booking.bookingID}`,
    },
    {
      key: 'guest',
      header: 'Guest Name',
      render: (booking: Booking) => `${booking.firstName} ${booking.lastName}`,
    },
    {
      key: 'phone',
      header: 'Phone',
    },
    {
      key: 'room',
      header: 'Room',
      render: (booking: Booking) => `${booking.roomNo} - ${booking.typeName}`,
    },
    {
      key: 'dates',
      header: 'Check-In / Check-Out',
      render: (booking: Booking) => (
        <div className="text-sm">
          <div>{format(new Date(booking.checkInDate), 'MMM dd, yyyy')}</div>
          <div className="text-gray-500">
            {format(new Date(booking.checkOutDate), 'MMM dd, yyyy')}
          </div>
        </div>
      ),
    },
    {
      key: 'status',
      header: 'Status',
      render: (booking: Booking) => getStatusBadge(booking.bookingStatus),
    },
    {
      key: 'actions',
      header: 'Actions',
      render: (booking: Booking) => (
        <div className="flex gap-2">
          <Button
            size="sm"
            variant="secondary"
            onClick={() => {
              setSelectedBooking(booking);
              setShowDetailsModal(true);
            }}
          >
            View
          </Button>
          {booking.bookingStatus === 'Booked' && (
            <Button
              size="sm"
              variant="success"
              onClick={() => handleCheckIn(booking.bookingID)}
              icon={<CheckCircle size={16} />}
            >
              Check In
            </Button>
          )}
          {booking.bookingStatus === 'CheckedIn' && (
            <Button
              size="sm"
              variant="primary"
              onClick={() => handleCheckOut(booking.bookingID)}
            >
              Check Out
            </Button>
          )}
          {booking.bookingStatus === 'Booked' && (
            <Button
              size="sm"
              variant="danger"
              onClick={() => handleCancel(booking.bookingID)}
              icon={<XCircle size={16} />}
            >
              Cancel
            </Button>
          )}
        </div>
      ),
    },
  ];

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Reservations</h1>
            <p className="text-gray-600 mt-1">Manage bookings and reservations</p>
          </div>
          <Button 
            variant="primary" 
            icon={<Plus size={20} />}
            onClick={() => setShowNewBookingModal(true)}
          >
            New Booking
          </Button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card className="bg-blue-50 border-blue-200">
            <div className="text-center">
              <p className="text-sm text-blue-700 font-medium">Total Bookings</p>
              <p className="text-3xl font-bold text-blue-900">{bookings.length}</p>
            </div>
          </Card>
          <Card className="bg-green-50 border-green-200">
            <div className="text-center">
              <p className="text-sm text-green-700 font-medium">Checked In</p>
              <p className="text-3xl font-bold text-green-900">
                {bookings.filter((b) => b.bookingStatus === 'CheckedIn').length}
              </p>
            </div>
          </Card>
          <Card className="bg-yellow-50 border-yellow-200">
            <div className="text-center">
              <p className="text-sm text-yellow-700 font-medium">Upcoming</p>
              <p className="text-3xl font-bold text-yellow-900">
                {bookings.filter((b) => b.bookingStatus === 'Booked').length}
              </p>
            </div>
          </Card>
          <Card className="bg-purple-50 border-purple-200">
            <div className="text-center">
              <p className="text-sm text-purple-700 font-medium">Checked Out</p>
              <p className="text-3xl font-bold text-purple-900">
                {bookings.filter((b) => b.bookingStatus === 'CheckedOut').length}
              </p>
            </div>
          </Card>
        </div>

        {/* Filters */}
        <Card>
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Search by guest name, phone, or room..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="input-field pl-10"
                />
              </div>
            </div>
            <div className="w-full md:w-48">
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value as BookingStatus | 'All')}
                className="input-field"
              >
                <option value="All">All Status</option>
                <option value="Booked">Booked</option>
                <option value="CheckedIn">Checked In</option>
                <option value="CheckedOut">Checked Out</option>
                <option value="Cancelled">Cancelled</option>
              </select>
            </div>
          </div>
        </Card>

        {/* Bookings Table */}
        <Card>
          <Table
            data={filteredBookings}
            columns={columns}
            loading={loading}
            emptyMessage="No bookings found"
          />
        </Card>

        {/* New Booking Modal */}
        <Modal
          isOpen={showNewBookingModal}
          onClose={() => {
            setShowNewBookingModal(false);
            resetNewBookingForm();
          }}
          title="Create New Booking"
          size="lg"
        >
          <form onSubmit={handleCreateBooking} className="space-y-4">
            {/* Guest Selection */}
            <div>
              <label className="label">Select Guest</label>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Search guest by name or phone"
                  value={newBookingData.guestSearch}
                  onChange={(e) => setNewBookingData({ ...newBookingData, guestSearch: e.target.value })}
                  className="input-field"
                />
                <Button type="button" variant="secondary" onClick={handleGuestSearch}>
                  Search
                </Button>
              </div>
              
              {guests.length > 0 && (
                <div className="mt-2 max-h-40 overflow-y-auto border rounded-lg">
                  {guests.map((guest) => (
                    <div
                      key={guest.guestID}
                      onClick={() => {
                        setNewBookingData({ ...newBookingData, selectedGuest: guest });
                        setGuests([]);
                      }}
                      className={`p-3 cursor-pointer hover:bg-gray-50 border-b ${
                        newBookingData.selectedGuest?.guestID === guest.guestID ? 'bg-primary-50' : ''
                      }`}
                    >
                      <p className="font-medium">{guest.firstName} {guest.lastName}</p>
                      <p className="text-sm text-gray-600">{guest.phone} • {guest.email}</p>
                    </div>
                  ))}
                </div>
              )}

              {newBookingData.selectedGuest && (
                <div className="mt-2 p-3 bg-green-50 border border-green-200 rounded-lg">
                  <p className="text-sm font-medium text-green-900">
                    Selected: {newBookingData.selectedGuest.firstName} {newBookingData.selectedGuest.lastName}
                  </p>
                </div>
              )}
            </div>

            {/* Branch & Room Type */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="label">Branch</label>
                <select
                  value={newBookingData.branchID}
                  onChange={(e) => setNewBookingData({ ...newBookingData, branchID: Number(e.target.value), roomID: 0 })}
                  className="input-field"
                >
                  <option value={1}>Colombo</option>
                  <option value={2}>Kandy</option>
                  <option value={3}>Galle</option>
                </select>
              </div>

              <div>
                <label className="label">Room Type</label>
                <select
                  value={newBookingData.typeID}
                  onChange={(e) => setNewBookingData({ ...newBookingData, typeID: Number(e.target.value), roomID: 0 })}
                  className="input-field"
                  required
                >
                  <option value={0}>Select room type</option>
                  {roomTypes.map((type) => (
                    <option key={type.typeID} value={type.typeID}>
                      {type.typeName} - LKR {type.currRate.toLocaleString()} / night
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Dates */}
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Check-In"
                type="datetime-local"
                value={newBookingData.checkInDate}
                onChange={(e) => setNewBookingData({ ...newBookingData, checkInDate: e.target.value, roomID: 0 })}
                required
              />
              <Input
                label="Check-Out"
                type="datetime-local"
                value={newBookingData.checkOutDate}
                onChange={(e) => setNewBookingData({ ...newBookingData, checkOutDate: e.target.value, roomID: 0 })}
                required
              />
            </div>

            <Input
              label="Number of Guests"
              type="number"
              min="1"
              value={newBookingData.numGuests}
              onChange={(e) => setNewBookingData({ ...newBookingData, numGuests: Number(e.target.value) })}
              required
            />

            {/* Check Availability Button */}
            <Button
              type="button"
              variant="secondary"
              onClick={checkAvailability}
              className="w-full"
              icon={<Calendar size={20} />}
            >
              Check Availability
            </Button>

            {/* Available Rooms */}
            {availableRooms.length > 0 && (
              <div>
                <label className="label">Select Room</label>
                <div className="grid grid-cols-3 gap-2 max-h-40 overflow-y-auto">
                  {availableRooms.map((room) => (
                    <div
                      key={room.roomID}
                      onClick={() => setNewBookingData({ ...newBookingData, roomID: room.roomID })}
                      className={`p-3 border-2 rounded-lg cursor-pointer text-center transition-all ${
                        newBookingData.roomID === room.roomID
                          ? 'border-primary-500 bg-primary-50'
                          : 'border-gray-200 hover:border-primary-300'
                      }`}
                    >
                      <p className="font-bold text-lg">Room {room.roomNo}</p>
                      <p className="text-xs text-gray-600">{room.typeName}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="flex gap-3 pt-4">
              <Button type="submit" variant="primary" className="flex-1">
                Create Booking
              </Button>
              <Button
                type="button"
                variant="secondary"
                onClick={() => {
                  setShowNewBookingModal(false);
                  resetNewBookingForm();
                }}
              >
                Cancel
              </Button>
            </div>
          </form>
        </Modal>

        {/* Details Modal */}
        {selectedBooking && (
          <Modal
            isOpen={showDetailsModal}
            onClose={() => {
              setShowDetailsModal(false);
              setSelectedBooking(null);
            }}
            title="Booking Details"
            size="lg"
          >
            <div className="space-y-6">
              {/* Guest Info */}
              <div>
                <h3 className="text-lg font-semibold mb-3">Guest Information</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Name</p>
                    <p className="font-medium">
                      {selectedBooking.firstName} {selectedBooking.lastName}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Phone</p>
                    <p className="font-medium">{selectedBooking.phone}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Email</p>
                    <p className="font-medium">{selectedBooking.email || 'N/A'}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Number of Guests</p>
                    <p className="font-medium">{selectedBooking.numGuests}</p>
                  </div>
                </div>
              </div>

              {/* Booking Info */}
              <div>
                <h3 className="text-lg font-semibold mb-3">Booking Information</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Booking ID</p>
                    <p className="font-medium">#{selectedBooking.bookingID}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Status</p>
                    <div>{getStatusBadge(selectedBooking.bookingStatus)}</div>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Room</p>
                    <p className="font-medium">
                      Room {selectedBooking.roomNo} - {selectedBooking.typeName}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Branch</p>
                    <p className="font-medium">{selectedBooking.branchLocation}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Check-In</p>
                    <p className="font-medium">
                      {format(new Date(selectedBooking.checkInDate), 'MMM dd, yyyy HH:mm')}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Check-Out</p>
                    <p className="font-medium">
                      {format(new Date(selectedBooking.checkOutDate), 'MMM dd, yyyy HH:mm')}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Rate per Night</p>
                    <p className="font-medium">LKR {selectedBooking.rate.toLocaleString()}</p>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-3 pt-4 border-t">
                {selectedBooking.bookingStatus === 'Booked' && (
                  <Button
                    variant="success"
                    onClick={() => {
                      handleCheckIn(selectedBooking.bookingID);
                      setShowDetailsModal(false);
                    }}
                    icon={<CheckCircle size={20} />}
                  >
                    Check In
                  </Button>
                )}
                {selectedBooking.bookingStatus === 'CheckedIn' && (
                  <Button
                    variant="primary"
                    onClick={() => {
                      handleCheckOut(selectedBooking.bookingID);
                      setShowDetailsModal(false);
                    }}
                  >
                    Check Out
                  </Button>
                )}
                <Button variant="secondary" onClick={() => setShowDetailsModal(false)}>
                  Close
                </Button>
              </div>
            </div>
          </Modal>
        )}
      </div>
    </MainLayout>
  );
};

export default ReservationsPage;