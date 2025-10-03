import api from './api';
import type { Room, RoomType } from '../types';

class RoomService {
  async getRoomTypes(): Promise<RoomType[]> {
    return await api.get<RoomType[]>('/rooms/types');
  }

  async getRoomsByBranch(branchId: number): Promise<Room[]> {
    return await api.get<Room[]>(`/rooms/branch/${branchId}`);
  }

  async getRoomById(id: number): Promise<Room> {
    return await api.get<Room>(`/rooms/${id}`);
  }
}

export default new RoomService();