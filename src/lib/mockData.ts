
export type Role = 'HQ' | 'OPERATOR' | 'MERCHANT';

export interface User {
  id: string;
  name: string;
  role: Role;
  assignedStores: string[]; // Store IDs
}

export interface Store {
  id: string;
  name: string;
  region: string;
}

export const mockStores: Store[] = [
  { id: '1', name: '王府井总店', region: '北京' },
  { id: '2', name: '三里屯店', region: '北京' },
  { id: '3', name: '徐家汇店', region: '上海' },
  { id: '4', name: '南京东路店', region: '上海' },
  { id: '5', name: '天河城店', region: '广州' },
];

export const mockUsers: Record<string, User> = {
  'hq_user': {
    id: 'u1',
    name: '张总部',
    role: 'HQ',
    assignedStores: mockStores.map(s => s.id),
  },
  'op_user': {
    id: 'u2',
    name: '李运营',
    role: 'OPERATOR',
    assignedStores: ['1', '2'], // Only Beijing stores
  },
  'merchant_user': {
    id: 'u3',
    name: '王店长',
    role: 'MERCHANT',
    assignedStores: ['3'], // Only Xujiahui
  },
};

// Default current user for simulation
export const currentUser = mockUsers['hq_user'];
