#!/usr/bin/env python3

from backend.app import app, db, seed

# Runs on Vercel import
with app.app_context():
    db.create_all()
    seed()

print("\n" + "="*55)
print("   CCTV UNIFIED MONITORING PLATFORM  —  IT CELL")
print("="*55)
print("   ✓ Database initialized")
print("   ✓ Demo data seeded")
print("="*55 + "\n")

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
