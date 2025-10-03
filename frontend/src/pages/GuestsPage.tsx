import { useState, useEffect } from 'react';
import { MainLayout } from '../components/layout';
import { Card, Button, Table, Modal, Input } from '../components/common';
import { Plus, Search, Edit, User } from 'lucide-react';
import { guestService } from '../services';
import type { Guest, GuestCreate } from '../types';
import { toast } from 'react-toastify';

const GuestsPage = () => {
  const [guests, setGuests] = useState<Guest[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingGuest, setEditingGuest] = useState<Guest | null>(null);
  
  // Form state
  const [formData, setFormData] = useState<GuestCreate>({
    firstName: '',
    lastName: '',
    phone: '+94',
    email: '',
    idNumber: '',
  });

  // Search guests
  const handleSearch = async () => {
    if (searchQuery.length < 2) {
      toast.warning('Please enter at least 2 characters to search');
      return;
    }

    try {
      setLoading(true);
      const data = await guestService.searchGuests(searchQuery);
      setGuests(data);
    } catch (error: any) {
      toast.error('Failed to search guests');
    } finally {
      setLoading(false);
    }
  };

  // Handle search on Enter key
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  // Create or update guest
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate phone format
    if (!formData.phone.match(/^\+94[0-9]{9}$/)) {
      toast.error('Phone must be in format +94xxxxxxxxx');
      return;
    }

    try {
      if (editingGuest) {
        await guestService.updateGuest(editingGuest.guestID, formData);
        toast.success('Guest updated successfully');
      } else {
        await guestService.createGuest(formData);
        toast.success('Guest created successfully');
      }
      
      setShowModal(false);
      resetForm();
      handleSearch();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Operation failed');
    }
  };

  // Reset form
  const resetForm = () => {
    setFormData({
      firstName: '',
      lastName: '',
      phone: '+94',
      email: '',
      idNumber: '',
    });
    setEditingGuest(null);
  };

  // Open edit modal
  const handleEdit = (guest: Guest) => {
    setEditingGuest(guest);
    setFormData({
      firstName: guest.firstName,
      lastName: guest.lastName,
      phone: guest.phone,
      email: guest.email || '',
      idNumber: guest.idNumber,
    });
    setShowModal(true);
  };

  // Table columns
  const columns = [
    {
      key: 'guestID',
      header: 'Guest ID',
      render: (guest: Guest) => `#${guest.guestID}`,
    },
    {
      key: 'name',
      header: 'Full Name',
      render: (guest: Guest) => (
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
            <User className="text-primary-600" size={16} />
          </div>
          <span className="font-medium">{`${guest.firstName} ${guest.lastName}`}</span>
        </div>
      ),
    },
    {
      key: 'phone',
      header: 'Phone',
    },
    {
      key: 'email',
      header: 'Email',
      render: (guest: Guest) => guest.email || 'N/A',
    },
    {
      key: 'idNumber',
      header: 'ID Number',
    },
    {
      key: 'actions',
      header: 'Actions',
      render: (guest: Guest) => (
        <Button
          size="sm"
          variant="secondary"
          onClick={() => handleEdit(guest)}
          icon={<Edit size={16} />}
        >
          Edit
        </Button>
      ),
    },
  ];

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Guests</h1>
            <p className="text-gray-600 mt-1">Manage guest information</p>
          </div>
          <Button
            variant="primary"
            icon={<Plus size={20} />}
            onClick={() => {
              resetForm();
              setShowModal(true);
            }}
          >
            Add Guest
          </Button>
        </div>

        {/* Search */}
        <Card>
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Search by name, phone, or ID number..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                className="input-field pl-10"
              />
            </div>
            <Button variant="primary" onClick={handleSearch} loading={loading}>
              Search
            </Button>
          </div>
        </Card>

        {/* Results */}
        <Card>
          <Table
            data={guests}
            columns={columns}
            loading={loading}
            emptyMessage="Search for guests to see results"
          />
        </Card>

        {/* Add/Edit Modal */}
        <Modal
          isOpen={showModal}
          onClose={() => {
            setShowModal(false);
            resetForm();
          }}
          title={editingGuest ? 'Edit Guest' : 'Add New Guest'}
        >
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="First Name"
                value={formData.firstName}
                onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                required
              />
              <Input
                label="Last Name"
                value={formData.lastName}
                onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                required
              />
            </div>

            <Input
              label="Phone"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              placeholder="+94771234567"
              helperText="Format: +94xxxxxxxxx"
              required
            />

            <Input
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              placeholder="guest@example.com"
            />

            <Input
              label="ID Number (NIC)"
              value={formData.idNumber}
              onChange={(e) => setFormData({ ...formData, idNumber: e.target.value })}
              placeholder="199512345678 or 199512345678V"
              required
            />

            <div className="flex gap-3 pt-4">
              <Button type="submit" variant="primary" className="flex-1">
                {editingGuest ? 'Update Guest' : 'Create Guest'}
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

export default GuestsPage;