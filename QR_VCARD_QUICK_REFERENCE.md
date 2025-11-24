# Quick Reference: QR Code System

## Endpoints Overview

### 1. Get Digital Card
```
GET /api/card/{company_slug}/{employee_slug}
Returns: Card data with QR and vCard URLs
Status: 200 OK
```

### 2. Download vCard File
```
GET /api/card/{company_slug}/{employee_slug}/vcard
Returns: .vcf file (RFC 3.0 compliant)
Status: 200 OK
Content-Type: text/vcard; charset=utf-8
Header: Content-Disposition: attachment; filename="Name.vcf"
```

### 3. Get QR Code Image
```
GET /api/card/{company_slug}/{employee_slug}/qr-vcard
Returns: PNG image (400x400px)
Status: 200 OK
Content-Type: image/png
Data: Valid PNG binary
```

## Test Commands

```bash
# Get card data
curl http://localhost:8000/api/card/test-admin-s-company-8f8d7331/alice-johnson-b45d8511

# Download vCard
curl -O http://localhost:8000/api/card/test-admin-s-company-8f8d7331/alice-johnson-b45d8511/vcard

# View vCard content
curl http://localhost:8000/api/card/test-admin-s-company-8f8d7331/alice-johnson-b45d8511/vcard | head -20

# Download QR image
curl -O http://localhost:8000/api/card/test-admin-s-company-8f8d7331/alice-johnson-b45d8511/qr-vcard

# Check QR image validity
file qr-vcard  # Should show: PNG image data...
```

## vCard Format

Standard RFC 3.0 fields included:

```
BEGIN:VCARD
VERSION:3.0
FN:Full Name (formatted name)
N:LastName;FirstName;;; (structured name)
TITLE:Job Title
ORG:Company Name
EMAIL;TYPE=INTERNET:email@example.com
TEL;TYPE=VOICE:+1234567890
TEL;TYPE=CELL:cell phone number
PHOTO;VALUE=URI:http://example.com/photo.jpg
NOTE:Bio/Description
URL;TYPE=linkedin:http://linkedin.com/...
END:VCARD
```

## How Phone Scanning Works

1. **Camera App Detects QR**: Phone camera scans QR code
2. **Extracts URL**: Gets vCard endpoint URL from QR data
3. **Downloads vCard**: Phone downloads .vcf file
4. **Recognizes Format**: OS recognizes vCard MIME type
5. **Shows Prompt**: "Add to Contacts?" dialog appears
6. **User Confirms**: Taps "Add"
7. **Contact Saved**: All fields imported to contacts

## Production Setup

### Environment Variables Needed

```bash
# .env or docker environment
API_BASE_URL=https://api.yourdomain.com
FRONTEND_BASE_URL=https://yourdomain.com
```

### Code Change Required

In `backend/services.py`, update:

```python
# FROM:
vcard_url = f"http://localhost:8000/api/card/{company_slug}/{employee_slug}/vcard"

# TO:
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
vcard_url = f"{API_BASE_URL}/api/card/{company_slug}/{employee_slug}/vcard"
```

## Troubleshooting

### QR Code Not Appearing
```bash
# Test endpoint
curl http://localhost:8000/api/card/[slug]/[slug]/qr-vcard
# Should return PNG data (binary), not HTML error
```

### vCard Not Importing
```bash
# Check vCard format
curl http://localhost:8000/api/card/[slug]/[slug]/vcard
# Should start with "BEGIN:VCARD" and end with "END:VCARD"

# Verify it's valid
curl http://localhost:8000/api/card/[slug]/[slug]/vcard | file -
# Should show: ASCII text
```

### Contact Fields Missing on Phone
- Check vCard includes all desired fields
- Some phones may not support certain fields (NOTE, PHOTO, URL)
- Test with multiple devices if possible

## Performance Notes

- vCard generation: ~10-20ms (on-demand, no DB)
- QR code endpoint: ~50-100ms (includes external API call)
- Both cached by browser (if using HTTP cache headers)
- Scales linearly with number of employees

## Analytics

Track user interactions via:
```bash
GET /api/analytics/company/{company_id}
```

Actions recorded:
- `download_vcard` - User downloaded vCard
- `scan_qr` - User accessed QR endpoint

## Customization Options

### Change QR Size
In `backend/routes.py`, modify:
```python
# Current: size=400x400
qr_image_url = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={url}"

# Options: 100x100, 200x200, 300x300, 400x400, 500x500, etc.
```

### Add QR Error Correction
```python
# Add &ecc=parameter (L, M, Q, H)
qr_image_url = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&ecc=H&data={url}"
```

### Change QR Format
```python
# Support formats: png (default), jpg, gif, svg
qr_image_url = f"https://api.qrserver.com/v1/create-qr-code/?format=svg&data={url}"
```

## Support & Documentation

- vCard RFC 3.0: https://tools.ietf.org/html/rfc2426
- QR Server API: https://api.qrserver.com/
- Mobile vCard Import: Check phone OS documentation
