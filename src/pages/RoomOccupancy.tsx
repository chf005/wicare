import React, { useEffect, useState } from 'react';
import { RoomGrid, RoomStatus } from '../components/RoomGrid';
import { fetchRooms } from '../lib/api';
import { mapRawRoomToRoomStatus } from '../lib/roomUtils';

export function RoomOccupancy() {
  const [rooms, setRooms] = useState<RoomStatus[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchRooms()
      .then((rawRooms) => {
        const mappedRooms: RoomStatus[] = rawRooms.map((device) => {
          const roomNumber = device.room_number?.trim();
          const name = roomNumber ? `${roomNumber} 號房` : device.device_name || device.mac_address;
          const movementScore = Number(device.movement_score ?? 0);
          const occupancy = (device.occupancy_status || '').toLowerCase();
          let status: RoomStatus['status'] = 'empty';

          if (occupancy === 'motion' || movementScore > 20) {
            status = 'motion';
          } else if (occupancy === 'idle' || movementScore > 2) {
            status = 'idle';
          }

          const floorMatch = roomNumber?.match(/(\d+)/);
          const floor = floorMatch ? `${floorMatch[0].charAt(0)}F` : 'N/A';
          const lastActivity = device.last_seen ? device.last_seen : '剛剛';

          return {
            id: device.mac_address,
            name,
            floor,
            status,
            lastActivity,
            movementScore,
            sensorName: device.device_name || device.mac_address,
            sensorSignal: Number(device.current_rssi ?? 0),
            resident: '',
          };
        });
        setRooms(mappedRooms);
        setError(null);
      })
      .catch((err) => {
        console.error('fetchRooms error', err);
        setError('無法取得房間佔用資料，請確認後端是否啟動。');
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="h-full flex flex-col space-y-5">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-slate-800">房間佔用總覽</h1>
          <p className="text-sm text-slate-500 mt-1">即時顯示各感測區域的佔用狀態與活動強度</p>
        </div>
        <div className="flex items-center gap-2 bg-white px-3 py-2 rounded-lg border border-slate-100 text-sm">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
          <span className="text-slate-600 font-medium">即時更新中</span>
        </div>
      </div>

      {loading && (
        <div className="rounded-xl border border-slate-200 bg-white p-5 text-slate-500">正在載入房間資料...</div>
      )}
      {error && (
        <div className="rounded-xl border border-rose-200 bg-rose-50 p-5 text-rose-700">{error}</div>
      )}

      <div className="flex-1 min-h-0">
        <RoomGrid rooms={rooms} />
      </div>
    </div>
  );
}
