import api from './api';
import type { LoginRequest, LoginResponse, User } from '../types';

class AuthService {
  private readonly TOKEN_KEY = 'token';
  private readonly USER_KEY = 'user';

  async login(username: string, password: string): Promise<LoginResponse> {
    const data: LoginRequest = { username, password };
    const response = await api.post<LoginResponse>('/auth/login', data);
    
    if (response.access_token) {
      this.setToken(response.access_token);
      this.setUser(response.user);
    }
    
    return response;
  }

  logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  setToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
  }

  getUser(): User | null {
    const userStr = localStorage.getItem(this.USER_KEY);
    if (!userStr) return null;
    
    try {
      return JSON.parse(userStr) as User;
    } catch {
      return null;
    }
  }

  setUser(user: User): void {
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  async verifyToken(): Promise<boolean> {
    try {
      const response = await api.post<{ success: boolean }>('/auth/verify-token');
      return response.success;
    } catch {
      return false;
    }
  }

  async getCurrentUser(): Promise<User | null> {
    try {
      return await api.get<User>('/auth/me');
    } catch {
      return null;
    }
  }
}

export default new AuthService();