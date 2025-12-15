# MedFinder Startup Scripts

## Available Batch Files

### 1. `start_medfinder.bat` (Recommended)
**Full-featured startup script with checks and user guidance**

Features:
- ✅ Checks for .env file
- ✅ Creates .env from .env.example if missing
- ✅ Starts backend server on port 5000
- ✅ Starts frontend server on port 5173
- ✅ Opens MedFinder in your default browser
- ✅ Shows helpful status messages
- ✅ Runs servers in separate windows

**Usage:**
```batch
Double-click start_medfinder.bat
```

OR from command line:
```batch
start_medfinder.bat
```

### 2. `quick_start.bat`
**Simple, fast startup without extra checks**

Features:
- 🚀 Quick startup
- 🚀 Minimal output
- 🚀 Opens browser automatically

**Usage:**
```batch
Double-click quick_start.bat
```

### 3. `stop_medfinder.bat`
**Stops all MedFinder servers**

Features:
- 🛑 Stops all Node.js processes (Frontend)
- 🛑 Stops all Python processes (Backend)
- 🛑 Clean shutdown

**Usage:**
```batch
Double-click stop_medfinder.bat
```

## Quick Start Guide

### First Time Setup

1. **Install Dependencies**
   
   Backend:
   ```batch
   cd backend_api
   pip install -r requirements.txt
   ```
   
   Frontend:
   ```batch
   cd frontend
   npm install
   ```

2. **Configure Environment**
   
   Create `.env` file in root folder:
   ```env
   HF_TOKEN=your_huggingface_token_here
   ```
   
   Get token from: https://huggingface.co/settings/tokens

3. **Run the Application**
   ```batch
   start_medfinder.bat
   ```

### Daily Use

**To Start:**
- Double-click `start_medfinder.bat` or `quick_start.bat`

**To Stop:**
- Double-click `stop_medfinder.bat`
- OR close the server windows manually

## What Happens When You Run

### `start_medfinder.bat`:

1. Checks if `.env` file exists
2. Creates it from `.env.example` if missing
3. Opens a new window for Backend (port 5000)
4. Waits 3 seconds for backend to initialize
5. Opens a new window for Frontend (port 5173)
6. Opens http://localhost:5173 in your browser
7. Shows success message with all URLs

### `quick_start.bat`:

1. Starts Backend in new window
2. Waits 2 seconds
3. Starts Frontend in new window
4. Waits 3 seconds
5. Opens browser

### `stop_medfinder.bat`:

1. Kills all Node.js processes (Frontend)
2. Kills all Python processes (Backend)
3. Shows confirmation
4. Done!

## URLs After Startup

| Service | URL |
|---------|-----|
| **Frontend (Main App)** | http://localhost:5173 |
| **Backend API** | http://localhost:5000 |
| **API Documentation** | http://localhost:5000/docs |
| **Prescription Assistant** | http://localhost:5173/prescription |

## Troubleshooting

### Port Already in Use

**Error:** "Address already in use" or similar

**Solution:**
1. Run `stop_medfinder.bat`
2. Wait a few seconds
3. Try starting again

OR manually:
```batch
# Kill Node.js
taskkill /F /IM node.exe

# Kill Python
taskkill /F /IM python.exe
```

### Backend Won't Start

**Possible Causes:**
- Python not installed
- Dependencies not installed
- Port 5000 already in use

**Solutions:**
1. Install Python 3.8+
2. Run: `cd backend_api && pip install -r requirements.txt`
3. Check port: `netstat -ano | findstr :5000`

### Frontend Won't Start

**Possible Causes:**
- Node.js not installed
- Dependencies not installed
- Port 5173 already in use

**Solutions:**
1. Install Node.js 16+
2. Run: `cd frontend && npm install`
3. Check port: `netstat -ano | findstr :5173`

### Browser Doesn't Open

**Solution:**
Manually open: http://localhost:5173

### .env File Issues

**Error:** "HF_TOKEN not found" or AI validation unavailable

**Solution:**
1. Create `.env` file
2. Add: `HF_TOKEN=your_token_here`
3. Get token from: https://huggingface.co/settings/tokens

**Note:** App works without HF_TOKEN, but AI validation will be limited

## Manual Startup (Alternative)

If batch files don't work, start manually:

### Terminal 1 - Backend:
```batch
cd backend_api
python app.py
```

### Terminal 2 - Frontend:
```batch
cd frontend
npm run dev
```

### Browser:
Open http://localhost:5173

## Advanced Options

### Run in Background (No Windows)

Create `start_hidden.bat`:
```batch
@echo off
start /B pythonw backend_api\app.py
timeout /t 3 /nobreak > nul
start /B npm run dev --prefix frontend
```

### Custom Ports

Edit the batch files or set environment variables:
```batch
set PORT=8000
set VITE_PORT=3000
```

## Notes

- **Windows Only**: These are Windows batch files (.bat)
- **Admin Rights**: Not required for normal operation
- **Firewall**: May need to allow Python/Node.js through firewall
- **Antivirus**: Some antivirus may flag the scripts, add exception if needed

## Getting Help

1. Check console output in server windows for errors
2. Review logs in backend/frontend
3. Visit http://localhost:5000/docs for API documentation
4. See `QUICK_SETUP.md` for detailed setup instructions
5. See `PRESCRIPTION_ASSISTANT_README.md` for feature documentation

## Summary

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `start_medfinder.bat` | Full startup with checks | **Daily use** |
| `quick_start.bat` | Fast startup | Quick testing |
| `stop_medfinder.bat` | Stop all servers | End of work |

**Recommended Workflow:**
1. First time: `start_medfinder.bat` (checks .env)
2. Daily use: `quick_start.bat` (faster)
3. End of day: `stop_medfinder.bat` (clean shutdown)

Enjoy using MedFinder! 🎉
