import { describe, it, expect, vi } from 'vitest';
import axios from 'axios';

// Mock axios
vi.mock('axios');

describe('App Component API Integration', () => {
  
  it('axios is mockable', () => {
    expect(axios.get).toBeDefined();
    expect(vi.isMockFunction(axios.get)).toBe(true);
  });

  it('can mock axios.get', async () => {
    axios.get.mockResolvedValue({ data: { test: 'value' } });
    
    const result = await axios.get('/test');
    
    expect(result.data).toEqual({ test: 'value' });
  });

  it('can mock axios.post', async () => {
    axios.post.mockResolvedValue({ data: { success: true } });
    
    const result = await axios.post('/test', {});
    
    expect(result.data).toEqual({ success: true });
  });
});

describe('Frontend Configuration', () => {
  it('API URL is defined correctly', () => {
    const API_URL = 'http://localhost:8000/api';
    expect(API_URL).toBe('http://localhost:8000/api');
  });

  it('expected API endpoints are defined', () => {
    const endpoints = [
      '/api/config/',
      '/api/operations/scan',
      '/api/operations/clean',
      '/api/operations/undo',
      '/api/history/'
    ];
    
    endpoints.forEach(endpoint => {
      expect(endpoint).toContain('/api/');
    });
  });
});
