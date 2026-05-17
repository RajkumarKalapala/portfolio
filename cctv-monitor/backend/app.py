from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import random, string, os, hashlib

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = 'cctv_monitor_secret_2024'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/cctv.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///something.db'

db = SQLAlchemy(app)

# ─── Models ───────────────────────────────────────────────────────────────────

class Camera(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    camera_id   = db.Column(db.String(20), unique=True, nullable=False)
    name        = db.Column(db.String(100), nullable=False)
    location    = db.Column(db.String(200))
    latitude    = db.Column(db.Float)
    longitude   = db.Column(db.Float)
    zone        = db.Column(db.String(50))
    status      = db.Column(db.String(20), default='Online')   # Online/Offline/Intermittent
    sim_number  = db.Column(db.String(20))
    sim_provider= db.Column(db.String(30))
    signal      = db.Column(db.Integer, default=80)            # 0-100
    data_used   = db.Column(db.Float, default=0.0)             # GB
    data_limit  = db.Column(db.Float, default=10.0)            # GB
    sim_expiry  = db.Column(db.Date)
    last_seen   = db.Column(db.DateTime, default=datetime.utcnow)
    installed_on= db.Column(db.Date)
    ip_address  = db.Column(db.String(20))
    model       = db.Column(db.String(60))
    tickets     = db.relationship('Ticket', backref='camera', lazy=True)

class Ticket(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    ticket_id   = db.Column(db.String(20), unique=True)
    camera_fk   = db.Column(db.Integer, db.ForeignKey('camera.id'), nullable=False)
    issue       = db.Column(db.String(200))
    priority    = db.Column(db.String(10), default='Medium')   # Low/Medium/High/Critical
    status      = db.Column(db.String(20), default='Open')     # Open/In Progress/Resolved/Closed
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_to = db.Column(db.String(60))
    notes       = db.Column(db.Text)

class UptimeLog(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    camera_fk   = db.Column(db.Integer, db.ForeignKey('camera.id'))
    timestamp   = db.Column(db.DateTime, default=datetime.utcnow)
    status      = db.Column(db.String(20))
    signal      = db.Column(db.Integer)
    data_used   = db.Column(db.Float)

class User(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(50), unique=True)
    password    = db.Column(db.String(64))
    role        = db.Column(db.String(20), default='viewer')   # admin/operator/viewer

# ─── Seed Data ────────────────────────────────────────────────────────────────

ZONES   = ['North Zone', 'South Zone', 'East Zone', 'West Zone', 'Central Zone']
MODELS  = ['Hikvision DS-2CD', 'Dahua IPC-HDW', 'CP Plus CP-UNC', 'Axis P3245']
ISPS    = ['Airtel', 'Jio', 'BSNL', 'Vi']
LOCS    = [
    ('Main Market Junction','16.5062','80.6480'),
    ('Railway Station Gate','16.5120','80.6200'),
    ('Bus Stand Circle','16.5010','80.6350'),
    ('City Hospital Entrance','16.4990','80.6550'),
    ('Old Town Square','16.5200','80.6100'),
    ('Collector Office','16.5080','80.6400'),
    ('Municipal Park','16.4960','80.6480'),
    ('IT Park Gate','16.5300','80.6600'),
    ('Airport Road','16.5400','80.6700'),
    ('Port Area Gate','16.5000','80.6900'),
    ('School Crossroads','16.5150','80.6300'),
    ('Police HQ','16.5050','80.6430'),
]

def seed():
    if User.query.count() == 0:
        for u, p, r in [('admin','admin123','admin'),('operator','op123','operator'),('viewer','view123','viewer')]:
            db.session.add(User(username=u, password=hashlib.sha256(p.encode()).hexdigest(), role=r))

    if Camera.query.count() == 0:
        statuses = ['Online']*7 + ['Offline']*2 + ['Intermittent']*3
        for i, (loc, lat, lon) in enumerate(LOCS):
            cam_id  = f'CAM-{1000+i}'
            status  = random.choice(statuses)
            signal  = random.randint(10,95) if status != 'Offline' else random.randint(0,15)
            expiry  = datetime.utcnow().date() + timedelta(days=random.randint(-10, 180))
            used    = round(random.uniform(0.5, 9.5), 2)
            cam = Camera(
                camera_id=cam_id, name=f'Camera {cam_id}',
                location=loc, latitude=float(lat), longitude=float(lon),
                zone=ZONES[i % len(ZONES)], status=status,
                sim_number=f'9{random.randint(100000000,999999999)}',
                sim_provider=random.choice(ISPS),
                signal=signal, data_used=used, data_limit=10.0,
                sim_expiry=expiry, last_seen=datetime.utcnow() - timedelta(minutes=random.randint(0,300)),
                installed_on=datetime.utcnow().date() - timedelta(days=random.randint(30,400)),
                ip_address=f'192.168.{random.randint(1,10)}.{random.randint(2,254)}',
                model=random.choice(MODELS)
            )
            db.session.add(cam)

    db.session.commit()

    if Ticket.query.count() == 0:
        cameras = Camera.query.all()
        issues  = ['Camera offline','SIM data exhausted','Signal weak','Connection intermittent','Physical damage reported','SIM expiry alert']
        for c in random.sample(cameras, min(6, len(cameras))):
            tid = 'TKT-' + ''.join(random.choices(string.digits, k=6))
            t   = Ticket(ticket_id=tid, camera_fk=c.id,
                         issue=random.choice(issues),
                         priority=random.choice(['Low','Medium','High','Critical']),
                         status=random.choice(['Open','In Progress','Resolved']),
                         assigned_to=random.choice(['Team Alpha','Team Beta','Team Gamma']),
                         created_at=datetime.utcnow() - timedelta(days=random.randint(0,30)))
            db.session.add(t)
        db.session.commit()

# ─── Auth ─────────────────────────────────────────────────────────────────────

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        u = request.form.get('username')
        p = hashlib.sha256(request.form.get('password','').encode()).hexdigest()
        user = User.query.filter_by(username=u, password=p).first()
        if user:
            session['user'] = user.username
            session['role'] = user.role
            return redirect(url_for('index'))
        error = 'Invalid credentials'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ─── Pages ────────────────────────────────────────────────────────────────────

@app.route('/')
@login_required
def index():
    return render_template('dashboard.html', user=session['user'], role=session['role'])

@app.route('/cameras')
@login_required
def cameras_page():
    return render_template('cameras.html', user=session['user'], role=session['role'])

@app.route('/tickets')
@login_required
def tickets_page():
    return render_template('tickets.html', user=session['user'], role=session['role'])

@app.route('/map')
@login_required
def map_page():
    return render_template('map.html', user=session['user'], role=session['role'])

@app.route('/reports')
@login_required
def reports_page():
    return render_template('reports.html', user=session['user'], role=session['role'])

# ─── API ──────────────────────────────────────────────────────────────────────

@app.route('/api/summary')
@login_required
def api_summary():
    total   = Camera.query.count()
    online  = Camera.query.filter_by(status='Online').count()
    offline = Camera.query.filter_by(status='Offline').count()
    inter   = Camera.query.filter_by(status='Intermittent').count()
    open_t  = Ticket.query.filter_by(status='Open').count()
    crit_t  = Ticket.query.filter(Ticket.priority=='Critical', Ticket.status!='Resolved').count()
    today   = datetime.utcnow().date()
    exp_soon= Camera.query.filter(Camera.sim_expiry <= today + timedelta(days=30)).count()
    low_data= Camera.query.filter(Camera.data_used >= Camera.data_limit * 0.85).count()
    uptime  = round((online / total * 100) if total else 0, 1)
    return jsonify(dict(total=total, online=online, offline=offline, intermittent=inter,
                        open_tickets=open_t, critical=crit_t, expiring_sims=exp_soon,
                        low_data=low_data, uptime_pct=uptime))

@app.route('/api/cameras')
@login_required
def api_cameras():
    cams = Camera.query.all()
    return jsonify([{
        'id': c.id, 'camera_id': c.camera_id, 'name': c.name,
        'location': c.location, 'lat': c.latitude, 'lon': c.longitude,
        'zone': c.zone, 'status': c.status,
        'sim_number': c.sim_number, 'sim_provider': c.sim_provider,
        'signal': c.signal, 'data_used': c.data_used, 'data_limit': c.data_limit,
        'sim_expiry': str(c.sim_expiry), 'last_seen': c.last_seen.strftime('%Y-%m-%d %H:%M'),
        'ip_address': c.ip_address, 'model': c.model,
        'data_pct': round(c.data_used / c.data_limit * 100, 1)
    } for c in cams])

@app.route('/api/tickets')
@login_required
def api_tickets():
    tks = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return jsonify([{
        'id': t.id, 'ticket_id': t.ticket_id,
        'camera_id': t.camera.camera_id, 'location': t.camera.location,
        'issue': t.issue, 'priority': t.priority, 'status': t.status,
        'assigned_to': t.assigned_to,
        'created_at': t.created_at.strftime('%Y-%m-%d %H:%M'),
        'notes': t.notes
    } for t in tks])

@app.route('/api/tickets/create', methods=['POST'])
@login_required
def create_ticket():
    d = request.json
    cam = Camera.query.filter_by(camera_id=d.get('camera_id')).first()
    if not cam:
        return jsonify({'error': 'Camera not found'}), 404
    tid = 'TKT-' + ''.join(random.choices(string.digits, k=6))
    t = Ticket(ticket_id=tid, camera_fk=cam.id,
               issue=d.get('issue','Unknown issue'),
               priority=d.get('priority','Medium'),
               assigned_to=d.get('assigned_to','Unassigned'),
               notes=d.get('notes',''))
    db.session.add(t)
    db.session.commit()
    return jsonify({'success': True, 'ticket_id': tid})

@app.route('/api/tickets/update', methods=['POST'])
@login_required
def update_ticket():
    d  = request.json
    t  = Ticket.query.filter_by(ticket_id=d.get('ticket_id')).first()
    if not t: return jsonify({'error': 'Not found'}), 404
    t.status     = d.get('status', t.status)
    t.notes      = d.get('notes', t.notes)
    t.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/zone_stats')
@login_required
def zone_stats():
    result = {}
    for z in ZONES:
        cams = Camera.query.filter_by(zone=z).all()
        result[z] = {
            'total':  len(cams),
            'online': sum(1 for c in cams if c.status=='Online'),
            'offline':sum(1 for c in cams if c.status=='Offline'),
            'inter':  sum(1 for c in cams if c.status=='Intermittent'),
        }
    return jsonify(result)

@app.route('/api/simulate_refresh')
@login_required
def simulate_refresh():
    """Simulate live status changes for demo purposes."""
    cams = Camera.query.all()
    for c in cams:
        roll = random.random()
        if c.status == 'Online':
            if roll < 0.05:   c.status = 'Offline'
            elif roll < 0.10: c.status = 'Intermittent'
            else:
                c.signal    = min(100, max(0, c.signal + random.randint(-5,5)))
                c.data_used = min(c.data_limit, c.data_used + round(random.uniform(0,0.05),3))
        elif c.status == 'Offline':
            if roll < 0.15: c.status = 'Online'; c.signal = random.randint(40,80)
        else:
            if roll < 0.20: c.status = 'Online'
            elif roll < 0.25: c.status = 'Offline'
        c.last_seen = datetime.utcnow()
    db.session.commit()
    return jsonify({'refreshed': len(cams), 'time': datetime.utcnow().strftime('%H:%M:%S')})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed()
    app.run(debug=True, port=5000)
