import db_manager

rows = db_manager.get_all_patients()
print('Found', len(rows), 'patients')
for r in rows[:10]:
    print(r)
