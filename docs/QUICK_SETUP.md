# Quick Setup Guide - Prescription Assistant

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

## Setup Steps

### 1. Environment Variables

Create a `.env` file in the root of medfinder folder:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your HuggingFace token:
```env
HF_TOKEN=hf_your_token_here
```

**Get your token**: https://huggingface.co/settings/tokens

> **Note**: The prescription assistant will work without this token, but AI validation will be disabled.

### 2. Backend Setup

```bash
cd backend_api

# Install Python dependencies
pip install -r requirements.txt

# Run the backend server
python app.py
```

Backend will run on: http://localhost:5000

### 3. Frontend Setup

```bash
cd frontend

# Install Node dependencies (if not done already)
npm install

# Run the development server
npm run dev
```

Frontend will run on: http://localhost:5173

### 4. Access the Feature

Open your browser and go to:
- **Main App**: http://localhost:5173
- **Prescription Assistant**: http://localhost:5173/prescription
- **API Docs**: http://localhost:5000/docs

## Verify Installation

### Test Drug Search:
1. Go to http://localhost:5173/prescription
2. Click "Drug Search" tab
3. Enter "Aspirin"
4. Click "Search Drug Information"
5. You should see detailed drug information

### Test Interaction Check:
1. Click "Interaction Check" tab
2. Enter "Warfarin" in Drug 1
3. Enter "Aspirin" in Drug 2
4. Click "Check Drug Interactions"
5. You should see interaction warnings

## Troubleshooting

### Backend won't start
- Check if port 5000 is available
- Verify Python dependencies are installed
- Check for errors in terminal

### Frontend won't start
- Check if port 5173 is available
- Run `npm install` again
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`

### "AI validation not available"
- This is normal if HF_TOKEN is not set
- Feature still works, just without AI-powered validation
- To enable: Add valid HF_TOKEN to .env

### "Drug not found"
- Check spelling
- Try alternative names (generic vs brand)
- Some drugs may not be in FDA databases

### CORS errors
- Ensure backend is running on port 5000
- Check backend console for errors
- Verify CORS middleware is configured correctly

## Quick Test Commands

### Test Backend API:
```bash
# Health check
curl http://localhost:5000/api/health

# Test drug search
curl -X POST http://localhost:5000/api/prescription/search \
  -H "Content-Type: application/json" \
  -d '{"drug_name": "Aspirin"}'
```

### View API Documentation:
Open http://localhost:5000/docs in your browser

## File Structure

```
medfinder/
├── backend_api/
│   ├── routes/
│   │   └── prescription.py      # Prescription API routes
│   ├── app.py                   # Main FastAPI app
│   └── requirements.txt         # Python dependencies
├── frontend/
│   └── src/
│       ├── pages/
│       │   └── PrescriptionAssistant.jsx  # Prescription UI
│       ├── components/
│       │   └── Navbar.jsx       # Updated with prescription link
│       └── App.jsx              # Added prescription route
├── data/
│   └── drug_index.json          # Drug names for fuzzy matching
├── .env.example                 # Environment variables template
├── PRESCRIPTION_ASSISTANT_README.md  # Detailed documentation
└── IMPLEMENTATION_SUMMARY.md    # Implementation details
```

## Next Steps

1. ✅ Backend running on port 5000
2. ✅ Frontend running on port 5173
3. ✅ Can access prescription feature
4. ✅ Drug search works
5. ✅ Interaction check works

**You're all set!** 🎉

For more details, see:
- `PRESCRIPTION_ASSISTANT_README.md` - Feature documentation
- `IMPLEMENTATION_SUMMARY.md` - Implementation details
- http://localhost:5000/docs - API documentation
