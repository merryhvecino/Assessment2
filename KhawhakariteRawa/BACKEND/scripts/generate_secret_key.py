#!/usr/bin/env python3
"""
Generate a secure JWT secret key for Kaiwhakarite Rawa
"""

import secrets
import string


def generate_secret_key(length=64):
    """Generate a cryptographically secure secret key."""
    # Use URL-safe characters
    return secrets.token_urlsafe(length)


def generate_strong_password(length=32):
    """Generate a strong alphanumeric secret key."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def main():
    print("🔐 JWT Secret Key Generator for Kaiwhakarite Rawa")
    print("=" * 50)
    
    # Generate different types of keys
    url_safe_key = generate_secret_key(64)
    strong_key = generate_strong_password(64)
    simple_key = secrets.token_hex(32)  # 64 character hex string
    
    print(f"\n📋 OPTION 1 - URL Safe Key (RECOMMENDED):")
    print(f"SECRET_KEY={url_safe_key}")
    
    print(f"\n📋 OPTION 2 - Strong Mixed Characters:")
    print(f"SECRET_KEY={strong_key}")
    
    print(f"\n📋 OPTION 3 - Hex String:")
    print(f"SECRET_KEY={simple_key}")
    
    print(f"\n🛡️  SECURITY NOTES:")
    print(f"   - Keep this key SECRET and SECURE")
    print(f"   - Never commit it to version control")
    print(f"   - Use environment variables in production")
    print(f"   - Change it if compromised")
    print(f"   - Each environment should have a different key")
    
    # Create .env file template
    env_template = f"""# Kaiwhakarite Rawa - Environment Variables
# SECURITY: Keep this file secret! Add to .gitignore

# JWT Security (CHANGE THIS!)
SECRET_KEY={url_safe_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24

# Database
DATABASE_URL=sqlite:///../database/kaiwhakarite.db

# File Upload Settings
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760

# Email Configuration (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=
EMAIL_PASSWORD=
EMAIL_FROM=Kaiwhakarite Rawa <noreply@kaiwhakarite.co.nz>

# System Settings
ADMIN_EMAIL=admin@kaiwhakarite.co.nz
DEBUG=false

# Application Info
APP_NAME=Kaiwhakarite Rawa
APP_VERSION=1.0.0
"""
    
    # Save to .env.example
    with open('.env.example', 'w') as f:
        f.write(env_template)
    
    print(f"\n📁 Created .env.example file with secure key!")
    print(f"   - Copy .env.example to .env")
    print(f"   - Add .env to your .gitignore")
    print(f"   - Update your secret key in .env")

if __name__ == "__main__":
    main() 