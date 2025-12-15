# MedFinder Frontend

A stunning, modern web frontend for the MedFinder pharmaceutical intelligence system.

## 🚀 Features

- **Smart Search** - Real-time autocomplete with fuzzy matching
- **Formula Search** - Find medicines by chemical composition
- **Price Comparison** - Discover cheaper generic alternatives (save up to 90%!)
- **Stock Checker** - Real-time availability on dawaai.pk
- **Beautiful UI** - Glassmorphism, animations, responsive design

## 📦 Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool
- **TailwindCSS 4** - Styling
- **Framer Motion** - Animations
- **Lucide React** - Icons
- **React Router DOM** - Navigation
- **Recharts** - Charts (if needed)

## 🎨 Design

- **Colors**: Medical Blue (#2563EB), Success Green (#10B981), Premium Purple (#8B5CF6)
- **Fonts**: Inter, Poppins, JetBrains Mono
- **Effects**: Glassmorphism, smooth hover transitions, skeleton loading

## 🛠️ Setup

### Prerequisites
- Node.js 18+
- Python 3.8+ (for backend API)
- npm or yarn

### Installation

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend API

The frontend requires the Flask backend API to be running:

```bash
# In another terminal, navigate to backend_api
cd backend_api

# Install Python dependencies
pip install -r requirements.txt

# Start the API server
python app.py
```

The frontend proxies API calls to `http://localhost:5000`.

## 📁 Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── SearchBar.jsx        # Autocomplete search
│   │   ├── MedicineCard.jsx     # Medicine display card
│   │   ├── AlternativesList.jsx # Similar medicines view
│   │   ├── AvailabilityCheck.jsx # Stock status
│   │   ├── DetailModal.jsx      # Medicine details popup
│   │   ├── StatsCard.jsx        # Animated stats
│   │   ├── SkeletonCard.jsx     # Loading skeleton
│   │   └── Navbar.jsx           # Navigation
│   ├── pages/
│   │   ├── Home.jsx             # Landing page
│   │   ├── Search.jsx           # Search results
│   │   └── FormulaSearch.jsx    # Formula search
│   ├── api/
│   │   └── medfinder.js         # API client
│   ├── styles/
│   │   └── globals.css          # Design system
│   ├── utils/
│   │   ├── formatPrice.js       # Price utilities
│   │   └── debounce.js          # Utility functions
│   ├── App.jsx                  # Main app
│   └── main.jsx                 # Entry point
├── public/
│   └── favicon.svg
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

## 🔧 Available Scripts

```bash
# Development server
npm run dev

# Production build
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/search/ingredient` | POST | Search by ingredient |
| `/api/search/composition` | POST | Search with dosage filter |
| `/api/autocomplete` | POST | Get suggestions |
| `/api/similar-medicines` | POST | Find alternatives |
| `/api/check-availability` | POST | Check stock |
| `/api/stats` | GET | Database stats |

## 📱 Responsive

- **Mobile**: 320px - 640px (1 column)
- **Tablet**: 641px - 1024px (2 columns)
- **Desktop**: 1025px+ (3 columns)

## 🎯 Key Features

### Search
- Type to get instant suggestions
- Keyboard navigation (Arrow keys, Enter, Escape)
- Fuzzy matching handles typos

### Medicine Cards
- Hover to lift with shadow
- Click for full details
- Check stock instantly
- Find alternatives

### Alternatives
- Sorted by savings
- Animated savings badges
- Annual savings calculation

## 📄 License

MIT License - Use freely for your projects!
