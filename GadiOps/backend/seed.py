from datetime import date, timedelta
from app.core.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.driver import Driver

# Initialize tables
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# 1. Seed Roles
if not db.query(User).first():
    db.add_all([
        User(email="manager@gadiops.com", password_hash=hash_password("admin123"), role="Fleet Manager"),
        User(email="driver@gadiops.com", password_hash=hash_password("driver123"), role="Driver"),
        User(email="analyst@gadiops.com", password_hash=hash_password("analyst123"), role="Financial Analyst")
    ])

# 2. Seed Vehicles
if not db.query(Vehicle).first():
    db.add_all([
        Vehicle(registration_number="MH-12-AB-1234", model="Tata Ace Gold", vehicle_type="Mini Truck", max_load_capacity=750.0, odometer=12000.0, acquisition_cost=550000.0, status="Available"),
        Vehicle(registration_number="DL-01-XY-5678", model="Mahindra Bolero Pik-Up", vehicle_type="Pickup", max_load_capacity=1500.0, odometer=45000.0, acquisition_cost=850000.0, status="Available"),
        Vehicle(registration_number="KA-03-MM-9012", model="Ashok Leyland Dost", vehicle_type="LCV", max_load_capacity=1250.0, odometer=28000.0, acquisition_cost=700000.0, status="In Shop")
    ])

# 3. Seed Drivers
if not db.query(Driver).first():
    db.add_all([
        Driver(name="Alex Kumar", license_number="DL-IND-001", license_category="Commercial", license_expiry_date=date.today() + timedelta(days=365), contact_number="9876543210", safety_score=95.0, status="Available"),
        Driver(name="Rajesh Singh", license_number="DL-IND-002", license_category="Heavy", license_expiry_date=date.today() - timedelta(days=10), contact_number="9876543211", safety_score=88.0, status="Available") # Expired license!
    ])

db.commit()
db.close()
print("🎉 GadiOps local mock data seeded successfully!")