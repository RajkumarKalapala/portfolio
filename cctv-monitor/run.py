#!/usr/bin/env python3
"""
CCTV Unified Monitor Platform — Startup Script
Run: python run.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from app import app, db, seed

if __name__ == '__main__':
    print("\n" + "="*55)
    print("   CCTV UNIFIED MONITORING PLATFORM  —  IT CELL")
    print("="*55)
    with app.app_context():
        db.create_all()
        seed()
        print("   ✓ Database initialized")
        print("   ✓ Demo data seeded")
        print("\n   Open browser: http://127.0.0.1:5000")
        print("   Login:  admin / admin123")
        print("="*55 + "\n")
    app.run(debug=True, port=5000, host='0.0.0.0')
