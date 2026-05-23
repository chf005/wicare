import { useEffect, useState } from 'react';
import { Patient } from '../types';
import { fetchPatients } from '../lib/api';
import { mockPatients } from '../lib/mockData';

const PATIENTS_STORAGE_KEY = 'csi_patients';

function loadSavedPatients(): Patient[] {
  const saved = localStorage.getItem(PATIENTS_STORAGE_KEY);
  if (saved) {
    try {
      return JSON.parse(saved);
    } catch {
      // ignore invalid JSON and fallback to mock data
    }
  }
  return mockPatients;
}

export function usePatients() {
  const [patients, setPatients] = useState<Patient[]>(loadSavedPatients);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPatients()
      .then((data) => {
        setPatients(data);
        setError(null);
      })
      .catch((err) => {
        console.error('usePatients fetch error', err);
        setError('無法讀取受護者資料，使用本機備援資料。');
      })
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    localStorage.setItem(PATIENTS_STORAGE_KEY, JSON.stringify(patients));
  }, [patients]);

  return { patients, setPatients, loading, error };
}
