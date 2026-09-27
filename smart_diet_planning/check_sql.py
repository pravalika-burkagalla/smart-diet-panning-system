with open(r'd:\smart_diet_planning\database.sql', 'r', encoding='utf-8') as f:
    sql = f.read()
print(f'SQL file size: {len(sql)} bytes')
print(f'First 300 chars:\n{sql[:300]}')
print(f'INSERT statements: {sql.count("INSERT")}')
