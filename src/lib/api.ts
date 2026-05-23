import { Patient } from '../types';

interface RawPatient {
  patient_id: number;
  name: string;
  gender?: string | null;
  birth_date?: string | null;
  age?: number | null;
  room_number?: string | null;
  medical_history?: string | string[] | null;
  medications?: string[] | null;
  notes?: string | null;
}

interface RawRoom {
  mac_address: string;
  device_name?: string | null;
  room_number?: string | null;
  current_rssi?: number | null;
  movement_score?: number | null;
  occupancy_status?: string | null;
  last_seen?: string | null;
}

const API_BASE = '/api';

function parseTextArray(value: string | string[] | null | undefined): string[] {
  if (!value) return [];
  if (Array.isArray(value)) return value.filter(Boolean);
  return value
    .toString()
    .split(/[,;\n]/)
    .map(item => item.trim())
    .filter(Boolean);
}

export async function fetchPatients(): Promise<Patient[]> {
  const res = await fetch(`${API_BASE}/patients`);
  if (!res.ok) {
    throw new Error(`API fetchPatients failed: ${res.status}`);
  }
  const raw: RawPatient[] = await res.json();
  return raw.map(p => ({
    id: String(p.patient_id),
    name: p.name || '未知',
    gender: (p.gender === '女' ? '女' : '男'),
    birthDate: p.birth_date || '',
    age: p.age ?? 0,
    roomNumber: p.room_number || '',
    contactName: '',
    contactPhone: '',
    medications: parseTextArray(p.medications ?? []),
    medicalHistory: parseTextArray(p.medical_history),
    notes: p.notes || '',
  }));
}

export async function fetchRooms(): Promise<RawRoom[]> {
  const res = await fetch(`${API_BASE}/rooms`);
  if (!res.ok) {
    throw new Error(`API fetchRooms failed: ${res.status}`);
  }
  return res.json();
}
