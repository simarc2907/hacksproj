from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, JWTManager
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="frontend", static_url_path="")
CORS(app)  # Enable CORS for frontend requests

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///buildaid.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    aadhar_path = db.Column(db.String(200))
    pan_path = db.Column(db.String(200))

    def __init__(self, full_name, email, phone, role, password):
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.role = role
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

with app.app_context():
    db.create_all()

# 🚀 Serve Frontend Files
@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('frontend', path)

# ✅ Home Test Route
@app.route('/api/status')
def home():
    return jsonify({"message": "BuildAid API is running"}), 200

# ✅ User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(
        full_name=data['full_name'],
        email=data['email'],
        phone=data['phone'],
        role=data['role'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# ✅ User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity={'email': user.email, 'role': user.role})
        return jsonify({"message": "Login successful", "token": access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# ✅ Upload Aadhar & PAN Card
@app.route('/upload_documents', methods=['POST'])
def upload_documents():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    aadhar_file = request.files.get('aadhar')
    pan_file = request.files.get('pan')

    if aadhar_file:
        aadhar_path = os.path.join(app.config['UPLOAD_FOLDER'], f"aadhar_{user.id}.jpg")
        aadhar_file.save(aadhar_path)
        user.aadhar_path = aadhar_path

    if pan_file:
        pan_path = os.path.join(app.config['UPLOAD_FOLDER'], f"pan_{user.id}.jpg")
        pan_file.save(pan_path)
        user.pan_path = pan_path

    db.session.commit()
    return jsonify({"message": "Documents uploaded successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
