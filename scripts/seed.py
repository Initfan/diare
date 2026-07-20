import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.extensions import db
from app.models.role import Role
from app.models.user import User


def seed():
    app = create_app('development')
    with app.app_context():
        db.create_all()

        # Seed roles
        roles_data = [
            ('Administrator', 'Pengelola sistem dan model'),
            ('Petugas administrasi', 'Pengelola data administratif pasien'),
            ('Perawat', 'Petugas pemeriksaan klinis'),
            ('Dokter', 'Validasi hasil skrining'),
        ]
        role_objs = {}
        for name, desc in roles_data:
            role = Role.query.filter_by(name=name).first()
            if not role:
                role = Role(name=name, description=desc)
                db.session.add(role)
                db.session.flush()
                print(f"Role '{name}' dibuat.")
            role_objs[name] = role

        db.session.commit()

        # Seed users
        users_data = [
            ('Administrator', 'admin', 'admin@klinik.id', 'Admin1234!', 'Administrator'),
            ('Dr. Budi Santoso', 'dokter1', 'dokter1@klinik.id', 'Dokter1234!', 'Dokter'),
            ('Suster Wati', 'perawat1', 'perawat1@klinik.id', 'Perawat1234!', 'Perawat'),
            ('Administrasi Rina', 'admin_rina', 'rina@klinik.id', 'Rina1234!', 'Petugas administrasi'),
        ]
        for full_name, username, email, password, role_name in users_data:
            user = User.query.filter_by(username=username).first()
            if not user:
                role = role_objs.get(role_name)
                user = User(
                    full_name=full_name,
                    username=username,
                    email=email,
                    role_id=role.id,
                    is_active=True
                )
                user.set_password(password)
                db.session.add(user)
                print(f"User '{username}' ({role_name}) dibuat.")

        db.session.commit()
        print("\nSeed selesai. Akun default:")
        print("  admin / Admin1234! (Administrator)")
        print("  dokter1 / Dokter1234! (Dokter)")
        print("  perawat1 / Perawat1234! (Perawat)")
        print("  admin_rina / Rina1234! (Petugas administrasi)")


if __name__ == '__main__':
    seed()
