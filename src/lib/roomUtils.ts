import type { RoomStatus } from '../components/RoomGrid';

export interface RawRoom {
  mac_address: string;
  device_name?: string | null;
  room_number?: string | null;
  current_rssi?: number | null;
  movement_score?: number | null;
  occupancy_status?: string | null;
  last_seen?: string | null;
}

export function mapRawRoomToRoomStatus(device: RawRoom): RoomStatus {
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
}
