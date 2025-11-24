# 🌐 Network Configuration Guide

## Problem You're Facing

You're getting connection errors because the app has hardcoded IPs in its configuration. When you switch networks or connect from a different IP, the old IP is no longer valid.

## Solution: Auto-Detection with Setup Script

The app now supports **automatic IP detection** and **dynamic configuration** for any network.

### Quick Start (Recommended)

```bash
cd /Users/mac/New\ AI\ Projects/Digital\ Business\ Cards

# Run the setup script - it will auto-detect your IP
./setup-env.sh

# Then start your services
docker-compose down && docker-compose up -d
```

The script will:
1. ✅ Auto-detect your machine's IP address
2. ✅ Create/update `.env.local` with the correct IP
3. ✅ Create/update `.env.development` with the correct IP
4. ✅ Configure backend CORS to accept requests from your IP

## How Auto-Detection Works

### Frontend (Next.js)

The frontend now has **intelligent URL detection**:

```typescript
// Auto-detects based on current URL
function getApiUrl(): string {
  const host = window.location.hostname;  // Gets current hostname
  const port = 8000;
  const protocol = window.location.protocol;
  return `${protocol}//${host}:${port}/api`;  // Constructs API URL
}
```

**This means:**
- If you visit `http://192.168.1.123:3000` → API becomes `http://192.168.1.123:8000/api`
- If you visit `http://10.0.0.5:3000` → API becomes `http://10.0.0.5:8000/api`
- **No rebuild needed!** Just visit from a different IP

### Backend (FastAPI)

The backend CORS is configured to accept multiple origins:

```python
CORS_ORIGINS = os.getenv(
  "CORS_ORIGINS",
  "http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000,http://192.168.1.123:3000,..."
)
```

**This allows:**
- localhost connections (development)
- 127.0.0.1 connections (local machine)
- Any IP in the `CORS_ORIGINS` env var

## Detailed Setup Instructions

### Step 1: Get Your Machine IP

**macOS:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Linux:**
```bash
hostname -I
```

**Windows:**
```cmd
ipconfig
```

Look for the IP starting with `192.168.x.x` or `10.x.x.x`

### Step 2: Run Setup Script

```bash
./setup-env.sh
# Enter your IP when prompted (or press Enter to auto-detect)
```

### Step 3: Verify Environment Files

Check that `.env.local` and `.env.development` have been created with your IP:

```bash
cat .env.local | grep MACHINE_IP
# Should show your actual IP, not the placeholder
```

### Step 4: Restart Services

**With Docker:**
```bash
docker-compose down
docker-compose up -d
```

**Locally (macOS/Linux):**
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
npm run dev
```

### Step 5: Test the Connection

Open your browser and visit:
```
http://YOUR-MACHINE-IP:3000
```

For example: `http://192.168.1.123:3000`

## Switching Networks

When you change to a different network (WiFi → USB tethering, different office WiFi, etc.):

### Option A: Automatic (Recommended)
1. Run `./setup-env.sh` again
2. Enter your new IP
3. Restart services

### Option B: Manual Override
If you want to manually override the API URL (for debugging):

```typescript
// In browser console
localStorage.setItem('api_url_override', 'http://NEW_IP:8000/api');
window.location.reload();
```

Clear the override:
```typescript
// In browser console
localStorage.removeItem('api_url_override');
window.location.reload();
```

## Troubleshooting

### "Cannot connect to backend"

1. **Check your IP is correct:**
   ```bash
   # Verify backend is running on your IP
   curl http://YOUR_IP:8000/api/health
   ```

2. **Verify Docker network (if using Docker):**
   ```bash
   docker exec digital-cards-backend printenv | grep -E "API_HOST|CORS_ORIGINS"
   ```

3. **Check browser console for API URL:**
   ```javascript
   // Open browser DevTools > Console
   console.log('API URL:', getApiUrl());
   ```

4. **Clear browser cache:**
   - Open DevTools (F12)
   - Application → Storage → Clear Site Data
   - Reload page

### "CORS error"

1. **Verify CORS_ORIGINS includes your IP:**
   ```bash
   echo $CORS_ORIGINS
   ```

2. **Update backend CORS if needed:**
   Edit `.env.local` and add your IP to `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://YOUR_IP:3000
   ```

3. **Restart backend:**
   ```bash
   docker-compose restart digital-cards-backend
   # or
   # Stop the local backend and restart
   ```

### "Page loads but API calls fail"

1. **Check frontend is using correct API URL:**
   ```javascript
   // In browser console
   fetch('/api/proxy?path=/health')
     .then(r => r.json())
     .then(d => console.log('API OK:', d))
     .catch(e => console.error('API Error:', e));
   ```

2. **Verify backend health:**
   ```bash
   curl http://YOUR_IP:8000/api/health
   ```

3. **Check Docker logs:**
   ```bash
   docker logs digital-cards-backend -f
   docker logs digital-cards-frontend -f
   ```

## Environment Variables Reference

| Variable | Purpose | Example |
|----------|---------|---------|
| `NEXT_PUBLIC_API_URL` | Frontend to backend API URL | `http://192.168.1.123:8000/api` |
| `NEXT_PUBLIC_APP_URL` | Frontend app URL | `http://192.168.1.123:3000` |
| `API_HOST` | Backend host | `192.168.1.123` |
| `API_PORT` | Backend port | `8000` |
| `CORS_ORIGINS` | Allowed frontend origins | `http://192.168.1.123:3000` |
| `ALLOWED_HOSTS` | Allowed hostnames | `192.168.1.123,localhost` |

## How to Test Different Scenarios

### Test 1: Same Machine, Same Network
```bash
# Terminal 1
./setup-env.sh
# Use your machine IP

# Terminal 2
docker-compose up -d

# Browser
http://YOUR_MACHINE_IP:3000  ✅ Should work
```

### Test 2: Different Machine on Same Network
```bash
# On another computer on the same WiFi
http://YOUR_MACHINE_IP:3000  ✅ Should work
```

### Test 3: Switch WiFi Networks
```bash
# Switch to different WiFi
./setup-env.sh
# Enter new IP
docker-compose down && docker-compose up -d

# Browser
http://NEW_IP:3000  ✅ Should work
```

## Performance Notes

- **Frontend auto-detection** happens in the browser (client-side)
  - No rebuild needed
  - Works instantly
  - Your IP is detected from `window.location.hostname`

- **Backend CORS** is configured at startup
  - If you add a new IP, restart the backend
  - Use `./setup-env.sh` to update and restart automatically

## Best Practices

1. **Always run `./setup-env.sh` when changing networks**
   - It ensures both frontend and backend configs are in sync

2. **Keep `.env.local` in `.gitignore`**
   - It contains your personal machine IP
   - Already configured in the repository

3. **Use environment variables, not hardcoded IPs**
   - All URLs now use `$NEXT_PUBLIC_API_URL` and related env vars
   - Makes the app portable across environments

4. **Test with `curl` before debugging in browser**
   - Confirms backend is reachable
   - Rules out frontend-specific issues

## Questions?

If something isn't working:

1. Run `./setup-env.sh` again
2. Check the browser console for the actual API URL being used
3. Verify backend is running: `curl http://YOUR_IP:8000/api/health`
4. Check Docker logs: `docker logs digital-cards-backend`
