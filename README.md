# Face Recognition Attendance System

A complete web-based attendance management system using face recognition technology with Python backend and React frontend.

## Features

✅ **User Registration** - Register users with face capture (20 face samples per user)
✅ **Real-time Attendance** - Mark attendance using face recognition with blink detection
✅ **Dashboard** - View statistics and attendance trends
✅ **Attendance Reports** - Filter and export attendance data as CSV
✅ **Admin Panel** - Manage users and clear attendance records
✅ **Modern UI** - Responsive React frontend with Tailwind CSS styling
✅ **REST API** - Complete API for all operations
✅ **Database Integration** - SQLite with SQLAlchemy ORM
✅ **Docker Support** - Full containerization with Docker Compose

## Technology Stack

### Backend
- **Python 3.9+**
- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **OpenCV** - Image processing
- **MTCNN** - Face detection
- **MediaPipe** - Face landmarks & blink detection
- **TensorFlow/Keras** - Deep learning

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Chart.js** - Analytics and charts
- **Axios** - HTTP client
- **CSS3** - Modern styling

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy

## Project Structure

```
finalyear_project/
├── api/
│   ├── app.py                 # Main Flask application
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/             # React pages
│   │   ├── App.jsx            # Main app component
│   │   └── index.css          # Global styles
│   ├── package.json
│   └── vite.config.js
├── src/
│   ├── register_face.py       # Face registration script
│   ├── face_recognition.py    # Face recognition script
│   └── face_attendance_blink.py # Attendance with blink detection
├── dataset/                   # User face datasets
├── attendance/                # Attendance records
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

## Installation

### Method 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/Aahil2504/finalyear_project.git
cd finalyear_project

# Build and start services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# API: http://localhost:5000
```

### Method 2: Local Development

#### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd api
pip install -r requirements.txt

# Run Flask server
python app.py
# Server runs on http://localhost:5000
```

#### Frontend Setup

```bash
# In another terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
# Server runs on http://localhost:3000
```

## API Endpoints

### Dashboard
- `GET /api/dashboard` - Get dashboard statistics

### Users
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get user by ID
- `POST /api/register` - Register new user
- `DELETE /api/users/<id>` - Delete user

### Attendance
- `GET /api/attendance` - Get all attendance records
- `GET /api/users/<id>/attendance` - Get user's attendance
- `POST /api/mark-attendance` - Mark attendance
- `POST /api/attendance/clear` - Clear all records (Admin)

### Health
- `GET /api/health` - Health check

## Usage

### Register New User

1. Navigate to **Register** page
2. Enter user details (Name, Email, Roll Number)
3. Click "Start Camera"
4. Look at camera - system will capture 20 face samples
5. Click "Register User" to save

### Mark Attendance

1. Navigate to **Attendance** page
2. Click "Start Camera"
3. Align your face in camera view
4. **Blink** to mark attendance
5. System will confirm attendance

### View Reports

1. Navigate to **Reports** page
2. Filter by Name or Date (optional)
3. Click "Export CSV" to download attendance data

### Admin Functions

1. Navigate to **Admin** page (if admin)
2. View all registered users
3. Delete users as needed
4. Clear all attendance records

## Configuration

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```
FLASK_ENV=development
DATABASE_URL=sqlite:///attendance.db
VITE_API_URL=http://localhost:5000
MIN_CONFIDENCE=75
```

## Database

The application uses SQLite database with two main tables:

### Users Table
```
id (Integer, Primary Key)
name (String, Unique)
email (String, Unique)
roll_number (String)
created_at (DateTime)
```

### Attendance Table
```
id (Integer, Primary Key)
user_id (Integer, Foreign Key)
date (Date)
time (Time)
status (String)
confidence (Float)
timestamp (DateTime)
```

## Troubleshooting

### Camera Not Working
- Ensure camera permissions are granted
- Check if another application is using the camera
- Try USB webcam if built-in camera fails

### Face Not Recognized
- Ensure face is well-lit
- Face should be straight on (not at angle)
- Register with 20 clear face samples
- Adjust MIN_CONFIDENCE value in .env

### CORS Errors
- Check if backend is running on port 5000
- Verify API_URL in frontend configuration
- Ensure Flask-CORS is installed

### Database Errors
- Delete `attendance.db` and restart
- Check database file permissions
- Verify SQLAlchemy installation

## Performance Tips

1. **Lighting** - Ensure good lighting during registration and attendance
2. **Face Size** - Keep face size 200x200 pixels for best results
3. **Database** - Regular backups of attendance records
4. **GPU** - Use GPU for faster face processing (requires CUDA)

## Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Email notifications
- [ ] Biometric authentication
- [ ] Real-time attendance sync
- [ ] Advanced analytics and reports
- [ ] Multi-user support with roles
- [ ] Attendance scheduling
- [ ] Integration with calendar systems

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Author

**Aakhil** - Final Year Project

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues and documentation
- Review code comments for implementation details

## Acknowledgments

- MTCNN for face detection
- MediaPipe for facial landmarks
- OpenCV for image processing
- Flask for web framework
- React for UI library
