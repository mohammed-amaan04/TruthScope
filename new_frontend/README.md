# Truth Scope - React Frontend

A modern React + TypeScript frontend for the Veritas fact-checking system, featuring a newspaper-themed design.

## 🎨 Features

- **Newspaper Theme**: Black and white design with classic newspaper typography
- **News Dashboard**: Slideshow of top stories across Politics, Economics, Celebrity, and Sports
- **Fact-Checking Interface**: Clean input form for claims and articles
- **Results Display**: Comprehensive verification results with truth scores and sources
- **Responsive Design**: Works on desktop and mobile devices
- **Modern Stack**: React 19, TypeScript, Tailwind CSS, and Vite

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn
- Veritas backend running on `http://localhost:8000`

### Installation

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```
   Or use the batch file:
   ```bash
   start_frontend.bat
   ```

3. **Open Browser**:
   Navigate to `http://localhost:3001`

## 📁 Project Structure

```
new_frontend/
├── src/
│   ├── components/
│   │   ├── NewsDashboard.tsx    # News slideshow component
│   │   └── FactCheckInput.tsx   # Fact-checking input form
│   ├── pages/
│   │   ├── HomePage.tsx         # Main landing page
│   │   └── ResultsPage.tsx      # Verification results page
│   ├── App.tsx                  # Main app component
│   ├── main.tsx                 # React entry point
│   └── index.css                # Global styles & newspaper theme
├── public/                      # Static assets
├── package.json                 # Dependencies and scripts
└── vite.config.ts              # Vite configuration
```

## 🎨 Design System

### Typography
- **Headlines**: Playfair Display (serif, bold)
- **Body Text**: Crimson Text (serif, readable)
- **Newspaper Elements**: Classic black borders, dividers

### Color Palette
- **Primary**: `#1a1a1a` (Newspaper Black)
- **Secondary**: `#4a4a4a` (Newspaper Gray)
- **Background**: `#fafafa` (Off-white)
- **Accent**: `#8b0000` (Dark Red)

## 🔌 API Integration

The frontend connects to your Veritas backend:
- **Endpoint**: `POST http://localhost:8000/api/v1/verify/`
- **Request**: `{ text, claim_type, language }`
- **Response**: Truth score, confidence, verdict, sources

## 📱 Pages

### Home Page (`/`)
- News dashboard with category slideshow
- Fact-checking input form
- AI system information

### Results Page (`/results`)
- Truth and confidence scores
- Verdict with color coding
- Supporting and contradicting sources
- Processing information

## 🛠️ Development

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Customization
- Modify `src/index.css` for theme changes
- Update `tailwind.config.js` for design tokens
- Edit components in `src/components/` for functionality
