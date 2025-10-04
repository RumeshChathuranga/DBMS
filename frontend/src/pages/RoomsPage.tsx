import { useState, useEffect } from 'react';
import { MainLayout } from '../components/layout';
import { Card, Badge } from '../components/common';
import { Hotel, Users, DollarSign, Calendar } from 'lucide-react';
import { roomService } from '../services';
import type { Room, RoomType, Branch } from '../types';
import { toast } from 'react-toastify';

const RoomsPage = () => {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [roomTypes, setRoomTypes] = useState<RoomType[]>([]);
  const [selectedBranch, setSelectedBranch] = useState<number>(1);
  const [loading, setLoading] = useState(true);

  const branches: Branch[] = [
    { branchID: 1, branchLocation: 'Colombo', rating: 4.5, phone: '+94112345678', email: 'colombo@skynest.lk' },
    { branchID: 2, branchLocation: 'Kandy', rating: 4.3, phone: '+94812345678', email: 'kandy@skynest.lk' },
    { branchID: 3, branchLocation: 'Galle', rating: 4.7, phone: '+94912345678', email: 'galle@skynest.lk' },
  ];

  useEffect(() => {
    fetchData();
  }, [selectedBranch]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [roomsData, typesData] = await Promise.all([
        roomService.getRoomsByBranch(selectedBranch),
        roomService.getRoomTypes(),
      ]);
      setRooms(roomsData);
      setRoomTypes(typesData);
    } catch (error) {
      toast.error('Failed to fetch rooms');
    } finally {
      setLoading(false);
    }
  };

  // Group rooms by type
  const roomsByType = roomTypes.map((type) => ({
    ...type,
    rooms: rooms.filter((room) => room.typeID === type.typeID),
  }));

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Rooms</h1>
          <p className="text-gray-600 mt-1">View room availability and details</p>
        </div>

        {/* Branch Selector */}
        <Card>
          <div className="flex gap-4">
            <label className="font-medium text-gray-700 self-center">Select Branch:</label>
            <select
              value={selectedBranch}
              onChange={(e) => setSelectedBranch(Number(e.target.value))}
              className="input-field max-w-xs"
            >
              {branches.map((branch) => (
                <option key={branch.branchID} value={branch.branchID}>
                  {branch.branchLocation}
                </option>
              ))}
            </select>
          </div>
        </Card>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="bg-blue-50 border-blue-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-700 font-medium">Total Rooms</p>
                <p className="text-3xl font-bold text-blue-900">{rooms.length}</p>
              </div>
              <div className="p-3 bg-blue-100 rounded-lg">
                <Hotel className="text-blue-600" size={24} />
              </div>
            </div>
          </Card>

          <Card className="bg-green-50 border-green-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-700 font-medium">Available</p>
                <p className="text-3xl font-bold text-green-900">
                  {rooms.filter((r) => r.roomStatus === 'Available').length}
                </p>
              </div>
              <div className="p-3 bg-green-100 rounded-lg">
                <Calendar className="text-green-600" size={24} />
              </div>
            </div>
          </Card>

          <Card className="bg-red-50 border-red-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-red-700 font-medium">Occupied</p>
                <p className="text-3xl font-bold text-red-900">
                  {rooms.filter((r) => r.roomStatus === 'Occupied').length}
                </p>
              </div>
              <div className="p-3 bg-red-100 rounded-lg">
                <Users className="text-red-600" size={24} />
              </div>
            </div>
          </Card>
        </div>

        {/* Rooms by Type */}
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : (
          <div className="space-y-6">
            {roomsByType.map((roomType) => (
              <Card key={roomType.typeID}>
                <div className="mb-4 pb-4 border-b flex justify-between items-center">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{roomType.typeName}</h3>
                    <div className="flex gap-4 mt-2 text-sm text-gray-600">
                      <span className="flex items-center gap-1">
                        <Users size={16} />
                        Capacity: {roomType.capacity}
                      </span>
                      <span className="flex items-center gap-1">
                        <DollarSign size={16} />
                        LKR {roomType.currRate.toLocaleString()} / night
                      </span>
                    </div>
                  </div>
                  <Badge variant={roomType.rooms.length > 0 ? 'success' : 'danger'}>
                    {roomType.rooms.length} rooms
                  </Badge>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                  {roomType.rooms.map((room) => (
                    <div
                      key={room.roomID}
                      className={`p-4 rounded-lg border-2 text-center transition-all ${
                        room.roomStatus === 'Available'
                          ? 'border-green-300 bg-green-50 hover:shadow-md'
                          : 'border-red-300 bg-red-50'
                      }`}
                    >
                      <div className="text-2xl font-bold text-gray-900 mb-1">
                        {room.roomNo}
                      </div>
                      <Badge
                        variant={room.roomStatus === 'Available' ? 'success' : 'danger'}
                      >
                        {room.roomStatus}
                      </Badge>
                    </div>
                  ))}
                </div>

                {roomType.rooms.length === 0 && (
                  <p className="text-center text-gray-500 py-4">
                    No rooms of this type in {branches.find(b => b.branchID === selectedBranch)?.branchLocation}
                  </p>
                )}
              </Card>
            ))}
          </div>
        )}
      </div>
    </MainLayout>
  );
};

export default RoomsPage;