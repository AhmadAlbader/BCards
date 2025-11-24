# 📱 Phone Scanning Setup Guide

## The Problem & Solution

### What Was Wrong
- QR codes contained `http://localhost:8000/...`
- When phone scanned QR, it tried to access localhost on the **phone**
- Phone can't access localhost (it only exists on your computer)
- Result: QR codes didn't work on phones ❌

### What Was Fixed
- Changed all URLs to use `192.168.1.123` (your computer's local network IP)
- Phone on same WiFi can now access your computer
- QR codes now work! ✅

---

## Prerequisites for Phone Testing

1. **Same WiFi Network**: Phone and computer must be on the same WiFi
2. **Backend Running**: `docker-compose up -d backend` (port 8000)
3. **Frontend Running**: `docker-compose up -d frontend` (port 3000)
4. **Local Network Access**: Phone must be able to reach 192.168.1.123

### Test Network Access First

On your **phone browser**, visit:
```
http://192.168.1.123:3000
```

If you see the website, network is working! If not, debug:
- Check WiFi connection
- Check firewall settings on your computer
- Verify Docker containers are running

---

## Testing Procedure

### On Your Computer

1. Open browser to card page:
   ```
   http://192.168.1.123:3000/card/test-admin-s-company-8f8d7331/alice-johnson-1e569e00
   ```

2. Click **"📱 Show QR"** button

3. QR code displays on screen

### On Your Phone

1. Open **Camera app** (iOS) or **Google Lens** (Android)

2. Point at QR code on computer screen

3. Tap notification when it appears

4. Select **"Add to Contacts"**

5. Contact saves with fields:
   - Name ✅
   - Title ✅
   - Company ✅
   - Email ✅
   - Phone ✅
   - Photo (if available) ✅

---

## Quick Reference URLs

Your machine IP: **192.168.1.123**

### View Card on Phone Browser
```
http://192.168.1.123:3000/card/test-admin-s-company-8f8d7331/alice-johnson-1e569e00
```

### Manual vCard Download (Alternative)
```
http://192.168.1.123:8000/api/card/test-admin-s-company-8f8d7331/alice-johnson-1e569e00/vcard
```

### Get QR Code Image
```
http://192.168.1.123:8000/api/card/test-admin-s-company-8f8d7331/alice-johnson-1e569e00/qr-vcard
```

---

## Troubleshooting

### QR Code Doesn't Appear in Browser
- Refresh page
- Check backend is running: `docker ps | grep backend`
- Check logs: `docker logs digital-cards-backend`

### Phone Can't Scan QR
- Make sure phone is on **same WiFi** as computer
- Camera app should recognize QR automatically
- If not, try Google Lens (Android) or built-in scanner

### Phone Can't Access Website After Scanning
- Test first: Go to `http://192.168.1.123:3000` on phone
- If that fails, network issue, not QR issue
- Check firewall on your computer
- Restart Docker: `docker-compose restart`

### Contact Doesn't Save to Phone
- vCard must be valid format
- Test manually: Visit vCard URL on phone
- Should trigger "Save Contact" dialog
- If it downloads as file instead, import manually

### Wrong IP Address
- Find your IP: `ifconfig | grep "inet " | grep -v 127.0.0.1`
- If different from 192.168.1.123, update:
  - `backend/services.py` (line ~212)
  - `backend/routes.py` (line ~532)
  - Restart backend: `docker-compose restart backend`
  - Reseed data: `python3 seed_test_data.py`

---

## Files Changed for Local Network Fix

### backend/services.py
```python
# BEFORE:
qr_url = f"http://localhost:8000/api/card/.../qr-vcard"

# AFTER:
qr_url = f"http://192.168.1.123:8000/api/card/.../qr-vcard"
```

### backend/routes.py
```python
# BEFORE:
vcard_url = f"http://localhost:8000/api/card/.../vcard"

# AFTER:
vcard_url = f"http://192.168.1.123:8000/api/card/.../vcard"
```

---

## Next Steps (Production)

When moving to production:
1. Use actual domain name instead of IP
2. Use HTTPS instead of HTTP
3. Update environment variables in `.env` file
4. Configure API_URL and FRONTEND_URL

Example production setup:
```
API_URL=https://api.yourdomain.com
FRONTEND_URL=https://yourdomain.com
```

---

## Testing Complete!

Your QR code system should now:
✅ Generate QR codes that work on phones
✅ Point to your computer's local IP
✅ Allow instant contact saving
✅ Support iOS, Android, Windows, macOS

Go scan that QR code! 📱✨
