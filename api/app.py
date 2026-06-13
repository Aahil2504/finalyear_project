from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os
import subprocess
import sys
from functools import wraps
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

db = SQLAlchemy(app)
CORS(app)

# ==================== DATABASE MODELS ====================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    roll_number = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    attendance_records = db.relationship('Attendance', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'roll_number': self.roll_number,
            'created_at': self.created_at.isoformat()
        }

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, default=date.today)
    time = db.Column(db.Time, default=datetime.now().time)
    status = db.Column(db.String(20), default='Present')  # Present, Absent, Late
    confidence = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.user.name,
            'email': self.user.email,
            'rollNumber': self.user.roll_number,
            'date': self.date.isoformat(),
            'time': self.time.isoformat(),
            'status': self.status,
            'confidence': self.confidence,
            'timestamp': self.timestamp.isoformat()
        }

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# ==================== API ROUTES ====================

# Dashboard
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    try:
        total_users = User.query.count()
        today = date.today()
        
        # Present today
        present_today = db.session.query(Attendance).filter(
            Attendance.date == today,
            Attendance.status == 'Present'
        ).count()
        
        # Absent calculation
        absent_today = total_users - present_today
        
        # Attendance rate
        attendance_rate = (present_today / total_users * 100) if total_users > 0 else 0
        
        return jsonify({
            'totalUsers': total_users,
            'presentToday': present_today,
            'absentToday': absent_today,
            'attendanceRate': round(attendance_rate, 2)
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Register User
@app.route('/api/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        name = data.get('name', '').strip().replace(' ', '_')
        email = data.get('email', '').strip()
        roll_number = data.get('roll_number', '').strip()
        
        # Validation
        if not name or not email:
            return jsonify({'error': 'Name and email are required'}), 400
        
        if User.query.filter_by(name=name).first():
            return jsonify({'error': 'User already exists'}), 400
        
        # Create user
        user = User(name=name, email=email, roll_number=roll_number)
        db.session.add(user)
        db.session.commit()
        
        # Trigger face registration (non-blocking)
        script_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'register_face.py')
        subprocess.Popen(
            [sys.executable, script_path, name],
            shell=False
        )
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Mark Attendance
@app.route('/api/mark-attendance', methods=['POST'])
def mark_attendance():
    try:
        data = request.get_json() or {}
        name = data.get('name', '').replace('_', ' ').strip()
        confidence = data.get('confidence', 0.0)
        
        # Find user
        user = User.query.filter_by(name=name).first()
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        # Check if already marked today
        today = date.today()
        existing = Attendance.query.filter(
            Attendance.user_id == user.id,
            Attendance.date == today
        ).first()
        
        if existing:
            return jsonify({
                'success': True,
                'message': 'Already marked',
                'name': user.name,
                'timestamp': existing.timestamp.isoformat()
            })
        
        # Create attendance record
        attendance = Attendance(
            user_id=user.id,
            status='Present',
            confidence=confidence
        )
        db.session.add(attendance)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Attendance marked',
            'name': user.name,
            'timestamp': attendance.timestamp.isoformat(),
            'confidence': confidence
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Get All Users
@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Get User by ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict())
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Delete User
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        # Also delete their dataset folder
        dataset_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', user.name)
        if os.path.exists(dataset_path):
            import shutil
            shutil.rmtree(dataset_path)
        
        return jsonify({'success': True, 'message': 'User deleted'})
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Get Attendance Records
@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    try:
        user_id = request.args.get('user_id')
        date_filter = request.args.get('date')
        
        query = Attendance.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if date_filter:
            query = query.filter_by(date=datetime.strptime(date_filter, '%Y-%m-%d').date())
        
        records = query.order_by(Attendance.timestamp.desc()).all()
        return jsonify([record.to_dict() for record in records])
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Get Attendance for User
@app.route('/api/users/<int:user_id>/attendance', methods=['GET'])
def get_user_attendance(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        records = Attendance.query.filter_by(user_id=user_id).order_by(
            Attendance.timestamp.desc()
        ).all()
        
        return jsonify([record.to_dict() for record in records])
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Clear All Attendance (Admin)
@app.route('/api/attendance/clear', methods=['POST'])
def clear_attendance():
    try:
        Attendance.query.delete()
        db.session.commit()
        return jsonify({'success': True, 'message': 'All attendance records cleared'})
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# Health Check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

# ==================== INITIALIZATION ====================
with app.app_context():
    db.create_all()
    print("Database initialized")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
