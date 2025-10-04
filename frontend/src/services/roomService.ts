import api from './api';
import type { Room, RoomType } from '../types';

class RoomService {
  async getRoomTypes(): Promise<RoomType[]> {
    console.log('Fetching room types');
    const result = await api.get<RoomType[]>('/rooms/types');
    console.log('Room types:', result);
    return result;
  }

  async getRoomsByBranch(branchId: number): Promise<Room[]> {
    console.log('Fetching rooms for branch:', branchId);
    const result = await api.get<Room[]>(`/rooms/branch/${branchId}`);
    console.log('Rooms fetched:', result);
    return result;
  }

  async getRoomById(id: number): Promise<Room> {
    return await api.get<Room>(`/rooms/${id}`);
  }
}

export default new RoomService();