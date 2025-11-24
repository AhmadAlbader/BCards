# 🎨 Company Branding & QR Code Implementation Guide

**Date:** November 23, 2025  
**Status:** Complete Implementation Plan + Code

---

## 📋 Overview

This guide explains how to implement:
1. **Company Branding Control Panel** - Admin can customize colors and logo
2. **QR Code Functionality** - Advanced options for QR customization
3. **Best Practices** - Security, performance, and UX considerations

---

## 🎨 Part 1: Company Branding Control

### Current State
- ✅ Database supports `brand_color` and `logo_url` in companies table
- ✅ Frontend displays branding on public cards
- ✅ Backend API can accept branding data
- ❌ **Missing:** Admin UI to manage branding
- ❌ **Missing:** Settings page in dashboard

### What We're Adding

A new **Branding Settings Page** where admins can:
- View current branding
- Upload/change company logo
- Pick brand colors (with color picker)
- Preview changes live
- See how cards will look with new branding

### Architecture

```
Admin Dashboard
  └── Branding Settings (NEW)
      ├── Logo Upload Section
      │   ├── Upload button (file input)
      │   ├── Preview current logo
      │   └── Delete logo option
      │
      ├── Color Customization
      │   ├── Color picker for brand_color
      │   ├── Preset colors
      │   └── Live preview
      │
      └── Live Preview Card
          └── Shows sample card with current settings
```

### Backend Endpoints

**New Endpoint 1: Get Company Branding**
```
GET /api/company/{company_id}/branding
Authorization: Bearer {token}

Response:
{
  "brand_color": "#3B82F6",
  "logo_url": "https://...",
  "company_name": "ACME Corp"
}
```

**New Endpoint 2: Update Company Branding**
```
PUT /api/company/{company_id}/branding
Authorization: Bearer {token}
Content-Type: application/json

Request:
{
  "brand_color": "#FF6B6B",
  "logo_url": "https://new-logo-url.com/logo.png"
}

Response:
{
  "status": "updated",
  "brand_color": "#FF6B6B",
  "logo_url": "https://new-logo-url.com/logo.png"
}
```

### Frontend Components

**File Structure:**
```
frontend/src/app/company-admin/
├── dashboard/
│   └── page.tsx (existing)
└── branding/ (NEW)
    └── page.tsx (NEW)
```

**Features:**
- Color picker integration (HTML5 input[type="color"])
- Logo upload handler (client-side preview)
- Form validation
- Error handling
- Success notifications
- Live preview of sample card

---

## 🔳 Part 2: QR Code Functionality

### Current State
- ✅ Database has `qr_code` field in cards table
- ✅ Backend generates QR URLs via QR Server API
- ✅ Frontend displays QR code on cards
- ❌ **Missing:** QR customization options
- ❌ **Missing:** Download QR code feature
- ❌ **Missing:** QR configuration in branding

### QR Implementation Strategy

#### **Option A: QR Server API (Current - Simple)**
```
https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=URL
```

**Pros:**
- ✅ No backend dependency
- ✅ Free service
- ✅ Instant generation
- ✅ Customizable size

**Cons:**
- ❌ Limited customization (no color control)
- ❌ Dependent on external service
- ❌ Can't add logo/branding to QR

#### **Option B: qrcode Library (Advanced - Recommended)**
```python
# Backend: Use qrcode library with PIL
import qrcode
from io import BytesIO
import base64

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=2,
)
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

# Convert to base64 or save to file
buffered = BytesIO()
img.save(buffered, format="PNG")
base64_qr = base64.b64encode(buffered.getvalue())
```

**Pros:**
- ✅ Full customization (colors, size, border)
- ✅ Can embed company logo in center
- ✅ Higher error correction options
- ✅ No external dependency

**Cons:**
- ❌ Additional library needed (qrcode, Pillow)
- ❌ Slight performance overhead
- ❌ Backend storage for generated images

#### **Option C: Hybrid Approach (Best)**
```
For Simple QR (no branding):
  → Use QR Server API (fast, no storage)

For Custom QR (with logo/colors):
  → Generate with qrcode library (customizable)
  → Store in S3/cloud storage
  → Return URL or base64 data URI
```

### Recommended: Option C - Hybrid Approach

**Implementation Steps:**

**Step 1: Backend Setup**
```bash
pip install qrcode[pil]
# Already have Pillow from dependencies
```

**Step 2: Add QR Generation Service**
```python
# backend/services.py - Add function

async def generate_custom_qr(
    data: str,
    brand_color: str = "#000000",
    size: int = 300,
    with_logo: Optional[str] = None
) -> bytes:
    """Generate custom QR code with company branding."""
    import qrcode
    from PIL import Image
    from io import BytesIO
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create image with brand color
    img = qr.make_image(fill_color=brand_color, back_color="white")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Add logo if provided
    if with_logo:
        try:
            logo = Image.open(BytesIO(with_logo))
            logo_size = size // 5
            logo = logo.resize((logo_size, logo_size))
            logo_pos = ((size - logo_size) // 2, (size - logo_size) // 2)
            img.paste(logo, logo_pos)
        except:
            pass  # Continue without logo if fails
    
    # Convert to bytes
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()
```

**Step 3: New API Endpoint for Custom QR**
```python
@router.get("/company/{company_id}/qr/generate")
async def generate_card_qr(
    company_id: uuid.UUID,
    employee_slug: str,
    include_logo: bool = False,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate custom QR code with company branding."""
    # Verify ownership
    company = await services.get_company_by_id(db, company_id)
    if not company or company.id != current_user["company_id"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # Get employee
    employee = await services.get_employee_by_slug(db, employee_slug, company_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Generate QR with branding
    qr_bytes = await services.generate_custom_qr(
        data=f"http://localhost:3000/card/{company.slug}/{employee.public_slug}",
        brand_color=company.brand_color or "#000000",
        size=300,
        with_logo=company.logo_url if include_logo else None
    )
    
    # Return as base64 or image file
    import base64
    return {
        "qr_code_base64": base64.b64encode(qr_bytes).decode(),
        "company_branding_applied": True
    }
```

---

## 🛠️ Implementation Steps

### Phase 1: Backend (Days 1-2)

**Step 1.1: Update Database Models**
- ✅ Already done - Company table has brand_color and logo_url

**Step 1.2: Add Branding Endpoints**
```python
# backend/routes.py

@router.get("/company/{company_id}/branding")
async def get_company_branding(
    company_id: uuid.UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get company branding settings."""
    company = await services.get_company_by_id(db, company_id)
    if not company or company.id != current_user["company_id"]:
        raise HTTPException(status_code=403)
    
    return {
        "brand_color": company.brand_color,
        "logo_url": company.logo_url,
        "company_name": company.name,
        "slug": company.slug
    }

@router.put("/company/{company_id}/branding")
async def update_company_branding(
    company_id: uuid.UUID,
    branding_data: dict,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update company branding settings."""
    company = await services.get_company_by_id(db, company_id)
    if not company or company.id != current_user["company_id"]:
        raise HTTPException(status_code=403)
    
    # Validate color format (hex)
    if "brand_color" in branding_data:
        color = branding_data["brand_color"]
        if not isinstance(color, str) or not color.startswith("#"):
            raise HTTPException(status_code=400, detail="Invalid color format")
    
    # Update company
    company = await services.update_company(
        db, 
        company_id,
        branding_data
    )
    
    return {
        "status": "updated",
        "brand_color": company.brand_color,
        "logo_url": company.logo_url
    }
```

**Step 1.3: Add QR Generation Service** (Optional - if using Option C)
```python
# backend/services.py
async def generate_custom_qr(...) → implement as shown above
```

### Phase 2: Frontend (Days 3-4)

**Step 2.1: Create Branding Settings Page**
```typescript
// frontend/src/app/company-admin/branding/page.tsx

'use client';
import { useEffect, useState } from 'react';
import axios from 'axios';

export default function BrandingPage() {
  const [brandColor, setBrandColor] = useState('#3B82F6');
  const [logoUrl, setLogoUrl] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const fetchBranding = async () => {
      const companyId = localStorage.getItem('company_id');
      const token = localStorage.getItem('token');
      
      try {
        const response = await axios.get(
          `${process.env.NEXT_PUBLIC_API_URL}/company/${companyId}/branding`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        setBrandColor(response.data.brand_color || '#3B82F6');
        setLogoUrl(response.data.logo_url || '');
      } finally {
        setLoading(false);
      }
    };
    
    fetchBranding();
  }, []);

  const handleSave = async () => {
    setSaving(true);
    const companyId = localStorage.getItem('company_id');
    const token = localStorage.getItem('token');
    
    try {
      await axios.put(
        `${process.env.NEXT_PUBLIC_API_URL}/company/${companyId}/branding`,
        { brand_color: brandColor, logo_url: logoUrl },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      // Show success message
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold mb-8">Brand Settings</h1>
      
      {/* Color Picker */}
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">Brand Color</h2>
        <input
          type="color"
          value={brandColor}
          onChange={(e) => setBrandColor(e.target.value)}
          className="w-20 h-20 rounded cursor-pointer"
        />
        <p className="text-gray-600 mt-2">{brandColor}</p>
      </div>

      {/* Logo Upload */}
      <div className="bg-white p-6 rounded-lg shadow mb-6">
        <h2 className="text-xl font-semibold mb-4">Company Logo</h2>
        {logoUrl && <img src={logoUrl} alt="Logo" className="h-16 mb-4" />}
        <input
          type="text"
          placeholder="Logo URL"
          value={logoUrl}
          onChange={(e) => setLogoUrl(e.target.value)}
          className="w-full border rounded px-3 py-2"
        />
      </div>

      {/* Save Button */}
      <button
        onClick={handleSave}
        disabled={saving}
        className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
      >
        {saving ? 'Saving...' : 'Save Changes'}
      </button>

      {/* Live Preview */}
      <div className="mt-8 bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Preview</h2>
        <div
          className="w-full max-w-md rounded-lg p-8 text-white"
          style={{ backgroundColor: brandColor }}
        >
          <h3 className="text-2xl font-bold">Sample Card</h3>
          <p className="text-lg opacity-90">Employee Name</p>
          {logoUrl && (
            <img src={logoUrl} alt="Logo" className="h-12 mt-4" />
          )}
        </div>
      </div>
    </div>
  );
}
```

**Step 2.2: Add Navigation to Branding Settings**
- Add link in dashboard sidebar or header menu
- Path: `/company-admin/branding`

### Phase 3: Integration (Day 5)

**Step 3.1: Update Public Card to Use Branding**
- Already implemented ✅

**Step 3.2: Add QR Code Download**
```typescript
// In public card page
<a
  href={`${process.env.NEXT_PUBLIC_API_URL}/company/${card.company_id}/qr/generate?employee_slug=${employee_slug}`}
  className="bg-white px-4 py-2 rounded font-semibold hover:bg-gray-100"
>
  📥 Download QR
</a>
```

---

## 🎯 Security Considerations

### Authentication & Authorization
✅ Only company admins can change branding
```python
if company.id != current_user["company_id"]:
    raise HTTPException(status_code=403)
```

### Logo Upload Security
⚠️ Current approach uses URL strings (safe)
⚠️ If implementing file upload:
- Validate file type (only images)
- Set max size limit (e.g., 5MB)
- Store in S3/cloud storage
- Use CDN for serving

### Color Validation
✅ Validate hex color format
```python
import re
hex_pattern = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')
if not hex_pattern.match(brand_color):
    raise HTTPException(status_code=400, detail="Invalid color")
```

---

## 📊 QR Code Implementation Comparison

| Feature | QR Server API | qrcode Library | Hybrid |
|---------|---------------|----------------|--------|
| Color Customization | ❌ | ✅ | ✅ |
| Logo Embedding | ❌ | ✅ | ✅ |
| Size Options | ✅ | ✅ | ✅ |
| Performance | ⚡ Fast | Medium | Fast |
| External Dependency | ✅ Yes | ❌ No | Minimal |
| Storage Required | ❌ No | ✅ Yes | Optional |
| **Recommended** | Simple | Advanced | **BEST** |

---

## 🚀 Deployment Checklist

- [ ] Add branding endpoints to backend
- [ ] Add QR generation service (if Option C)
- [ ] Create branding settings page frontend
- [ ] Test color picker functionality
- [ ] Test logo upload/display
- [ ] Test live preview
- [ ] Test public card with branding
- [ ] Test QR code generation
- [ ] Add navigation menu item
- [ ] Test authentication/authorization
- [ ] Add error handling
- [ ] Performance test with large logos
- [ ] Mobile responsive testing

---

## 🔄 Data Flow

### Setting Branding
```
Admin clicks "Brand Settings"
         ↓
Frontend: GET /api/company/{id}/branding
         ↓
Load current brand_color and logo_url
         ↓
Admin picks new color and logo
         ↓
Frontend: PUT /api/company/{id}/branding
         ↓
Backend validates and updates database
         ↓
Response confirms update
         ↓
Admin preview updates live
```

### Viewing Branded Cards
```
User views public card
         ↓
Frontend: GET /api/card/{company_slug}/{employee_slug}
         ↓
Backend returns card with company.brand_color and company.logo_url
         ↓
Frontend renders card with dynamic branding
         ↓
Card displays with company colors and logo
```

### Generating Custom QR
```
Admin clicks "Download QR"
         ↓
Frontend: GET /api/company/{id}/qr/generate?employee_slug=...
         ↓
Backend generates QR with brand_color
         ↓
Returns base64 or image URL
         ↓
Browser downloads QR code PNG
```

---

## 💡 Future Enhancements

1. **Card Templates**
   - Multiple card layout options
   - Different color schemes
   - Custom fonts

2. **Advanced QR Options**
   - Logo embedding in QR center
   - Custom error correction level
   - Size presets (mobile, print, etc.)

3. **Branding Assets**
   - Upload multiple logos (favicon, dark mode, etc.)
   - Font customization
   - Background patterns

4. **Multi-brand Support**
   - Different branding per department
   - Seasonal branding
   - Brand versioning/history

5. **Bulk Operations**
   - Export all employee cards with branding
   - Batch update employee cards
   - Branding preview for all employees

---

## 📞 Support & Troubleshooting

### Issue: Color not updating on cards
**Solution:** Clear browser cache, refresh page, verify token is valid

### Issue: Logo not displaying
**Solution:** Verify URL is publicly accessible, check CORS settings

### Issue: QR code not generating
**Solution:** Check if qrcode library installed, verify data URL is correct

### Issue: Slow branding page load
**Solution:** Implement caching, use CDN for logos, optimize image sizes

---

**Implementation Status:** Ready to code  
**Estimated Time:** 2-3 days  
**Complexity:** Medium  
**Dependencies:** qrcode[pil] (optional)

