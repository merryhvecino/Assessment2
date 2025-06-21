# 🔐 JWT Security Guide - Kaiwhakarite Rawa

## What is a JWT Secret Key?

The **JWT (JSON Web Token) Secret Key** is the most critical security component of your authentication system. It's used to:

### 🎯 **Primary Functions:**
1. **Digital Signing**: Creates unforgeable signatures on JWT tokens
2. **Token Verification**: Validates tokens haven't been tampered with
3. **Security Guarantee**: Ensures only your server can create valid tokens
4. **Session Protection**: Prevents unauthorized access and token forgery

### 🔄 **How JWT Authentication Works:**
```
1. User Login Request
   ↓
2. Server validates credentials
   ↓
3. Server creates JWT token signed with SECRET_KEY
   ↓
4. Token sent to client (stored in localStorage/cookies)
   ↓
5. Client includes token in API requests (Authorization header)
   ↓
6. Server verifies token using SECRET_KEY
   ↓
7. If valid → Grant Access | If invalid → Reject Request
```

## 🛡️ **CRITICAL: Why You MUST Hide the Secret Key**

### ⚠️ **Security Risks if Exposed:**
- **Complete System Compromise**: Anyone with the key can create valid tokens
- **Impersonation Attacks**: Attackers can become any user, including admins
- **Data Breach**: Full access to all protected endpoints and data
- **Long-term Damage**: Tokens stay valid until expiration (24 hours default)

### 🎯 **Attack Scenarios:**
```bash
# If someone gets your SECRET_KEY, they can:
import jwt
fake_token = jwt.encode({
    "user_id": 1,
    "role": "admin",
    "exp": future_time
}, your_secret_key, algorithm="HS256")

# Now they have admin access to your entire system!
```

## 🔒 **How to Properly Secure Your JWT Secret Key**

### **Step 1: Generate a Strong Secret Key**
We created a generator for you! Use one of these methods:

```bash
# Option 1: Use our generator (RECOMMENDED)
python scripts/generate_secret_key.py

# Option 2: Generate manually in Python
import secrets
secure_key = secrets.token_urlsafe(64)  # 64-character URL-safe key
print(f"SECRET_KEY={secure_key}")

# Option 3: Use OpenSSL
openssl rand -base64 64
```

### **Step 2: Create Environment Variables**
Create a `.env` file (already added to .gitignore):

```bash
# .env file (NEVER commit this!)
SECRET_KEY=gsdCjAv7tA4R96_x-saQoWibpaeTonvOEk7aC-lVE3gunUnH0GA9VUkpzDvpv-qZhv4II5JxAB9RnBupxEUHZQ
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=24
DEBUG=false
```

### **Step 3: Update Your Configuration**
Your `server/config.py` already uses environment variables correctly:

```python
# This is SECURE - it checks environment first
SECRET_KEY: str = config(
    'SECRET_KEY', 
    default='your_secret_key_here_make_it_very_long_and_secure'
)
```

## 📋 **Security Implementation Checklist**

### ✅ **Immediate Actions (DO NOW):**
- [ ] **Generate new secret key** using `python scripts/generate_secret_key.py`
- [ ] **Create `.env` file** with your secure key
- [ ] **Verify `.gitignore`** includes `.env` files
- [ ] **Remove hardcoded secrets** from any config files
- [ ] **Test environment variables** are working

### 🛡️ **Production Security (BEFORE DEPLOYMENT):**
- [ ] **Different keys per environment** (dev, staging, production)
- [ ] **Rotate keys regularly** (every 90 days recommended)
- [ ] **Use key management service** (AWS KMS, Azure Key Vault, etc.)
- [ ] **Monitor for key exposure** in logs or error messages
- [ ] **Set up key rotation process**

### 🔍 **Advanced Security Measures:**
- [ ] **Add rate limiting** to prevent brute force attacks
- [ ] **Implement token blacklisting** for logout/revocation
- [ ] **Use short expiration times** (1-4 hours) with refresh tokens
- [ ] **Add IP address validation** for sensitive operations
- [ ] **Log all authentication events** for security monitoring

## 🚨 **Emergency Response: If Your Key is Compromised**

### **Immediate Actions:**
1. **Generate new secret key** immediately
2. **Update production environment** with new key
3. **Force logout all users** (invalidates all existing tokens)
4. **Monitor system logs** for suspicious activity
5. **Change any other potentially exposed secrets**
6. **Review access logs** for unauthorized access

### **Recovery Steps:**
```bash
# 1. Generate new key
python scripts/generate_secret_key.py

# 2. Update .env file
SECRET_KEY=NEW_SECURE_KEY_HERE

# 3. Restart servers to apply changes
./start_servers.bat

# 4. All users will need to log in again (expected behavior)
```

## 📊 **Your Current Security Status**

### ✅ **Good Security Practices Already Implemented:**
- **Environment variables**: Your config.py uses python-decouple correctly
- **Fallback defaults**: Safe defaults for development
- **Proper algorithm**: HS256 is secure for symmetric keys
- **Token expiration**: 24-hour limit prevents indefinite access

### ⚠️ **Needs Improvement:**
- **Weak default key**: Change from development placeholder
- **No environment file**: Create `.env` with secure values
- **No key rotation**: Implement periodic key updates

## 🎯 **Quick Security Setup (5 Minutes)**

```bash
# 1. Generate secure key
python scripts/generate_secret_key.py

# 2. Copy the URL-safe key (Option 1)
# Example: gsdCjAv7tA4R96_x-saQoWibpaeTonvOEk7aC-lVE3gunUnH0GA9VUkpzDvpv-qZhv4II5JxAB9RnBupxEUHZQ

# 3. Create .env file
echo "SECRET_KEY=YOUR_GENERATED_KEY_HERE" > .env

# 4. Restart servers
./start_servers.bat

# 5. Test login - you should be able to authenticate normally
```

## 🏆 **Best Practices Summary**

### **Development Environment:**
- Use `.env` files for secrets
- Never commit secrets to git
- Use strong, unique keys even for development

### **Production Environment:**
- Use cloud key management services
- Rotate keys regularly (90 days)
- Monitor for security breaches
- Use different keys per environment
- Implement comprehensive logging

### **Team Collaboration:**
- Share `.env.example` (without actual secrets)
- Document key rotation procedures
- Use secure channels for key distribution
- Regular security training for all developers

---

## 🔗 **Additional Resources**

- [JWT.io Debugger](https://jwt.io/) - Decode and verify JWTs
- [OWASP JWT Security](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [Python-decouple Documentation](https://pypi.org/project/python-decouple/)

---

**Remember**: Your JWT secret key is like the master key to your entire system. Treat it with the same security as you would treat your bank password! 🔐 