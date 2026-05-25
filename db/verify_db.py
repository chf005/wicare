import db_manager

patients = db_manager.get_all_patients()
rooms = db_manager.get_room_occupancy()

print('Patients count:', len(patients))
for p in patients[:5]:
    print(p)

print('\nRooms count:', len(rooms))
for r in rooms[:5]:
    print(r)
