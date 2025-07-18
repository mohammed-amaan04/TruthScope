# Veritas Frontend

A simple, clean React interface for the Veritas fact-checking system.

## 🌟 Features

- **Simple Input**: Paste news articles or claims for verification
- **Real-time Results**: See truth scores and confidence levels
- **Visual Feedback**: Color-coded results with progress bars
- **Source Display**: View supporting and contradicting sources
- **Responsive Design**: Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites
- **Node.js 16+** (Download from [nodejs.org](https://nodejs.org/))
- **Veritas Backend** running on `http://localhost:8000`

### Installation & Setup

1. **Install Node.js** (if not already installed)
   - Download from https://nodejs.org/
   - Install the LTS version

2. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Start the Development Server**
   ```bash
   npm run dev
   ```
   
   **Or use the batch file (Windows):**
   ```bash
   start_frontend.bat
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 🎯 How to Use

1. **Start the Backend**: Make sure your Veritas API is running on port 8000
2. **Open the Frontend**: Navigate to http://localhost:3000
3. **Enter Content**: Paste a news article, headline, or claim in the text area
4. **Click "Verify Claim"**: The system will analyze the content
5. **View Results**: See the truth score, confidence, verdict, and sources

## 📊 Understanding the Results

### Truth Score
- **Green (70-100%)**: Likely true, well-supported by evidence
- **Yellow (40-69%)**: Mixed evidence, requires careful consideration
- **Red (0-39%)**: Likely false, contradicted by evidence

### Confidence Score
- **High (80-100%)**: System is very confident in the assessment
- **Medium (50-79%)**: Moderate confidence, some uncertainty
- **Low (0-49%)**: Low confidence, limited evidence available

### Verdict
- **✅ TRUE**: Well-supported by credible sources
- **❌ FALSE**: Contradicted by evidence
- **⚠️ MIXED**: Conflicting evidence found
- **❓ INSUFFICIENT_DATA**: Not enough reliable sources

## 🛠️ Technical Details

### Built With
- **React 18**: Modern React with hooks
- **Vite**: Fast development server and build tool
- **Axios**: HTTP client for API requests
- **CSS3**: Custom styling with gradients and animations

### Project Structure
```
frontend/
├── src/
│   ├── App.jsx          # Main application component
│   ├── App.css          # Styling
│   └── main.jsx         # React entry point
├── index.html           # HTML template
├── package.json         # Dependencies and scripts
├── vite.config.js       # Vite configuration
└── start_frontend.bat   # Windows startup script
```

### API Integration
The frontend communicates with the Veritas backend API:
- **Endpoint**: `POST http://localhost:8000/api/v1/verify/`
- **Request Format**: JSON with text, claim_type, and language
- **Response**: Truth score, confidence, verdict, and source articles

## 🔧 Development

### Available Scripts
- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run preview`: Preview production build

### Customization
- **Colors**: Modify CSS variables in `App.css`
- **API URL**: Change the axios base URL in `App.jsx`
- **Styling**: Update the CSS classes for different appearance

## 🚨 Troubleshooting

### Common Issues

**1. "Cannot connect to backend"**
- Ensure the Veritas API is running on http://localhost:8000
- Check if the backend is accessible by visiting http://localhost:8000/docs

**2. "Node.js not found"**
- Install Node.js from https://nodejs.org/
- Restart your terminal/command prompt after installation

**3. "npm install fails"**
- Try deleting `node_modules` and `package-lock.json`
- Run `npm install` again
- Check your internet connection

**4. "Port 3000 already in use"**
- Stop other applications using port 3000
- Or modify the port in `vite.config.js`

### CORS Issues
If you encounter CORS errors:
1. The backend should already have CORS enabled
2. Make sure you're accessing the frontend via http://localhost:3000
3. Check that the backend is running on http://localhost:8000

## 📱 Mobile Support

The interface is responsive and works on:
- **Desktop**: Full feature set
- **Tablet**: Optimized layout
- **Mobile**: Touch-friendly interface

## 🎨 UI Features

- **Gradient Background**: Modern purple gradient design
- **Loading States**: Spinner animation during verification
- **Progress Bars**: Visual representation of scores
- **Color Coding**: Intuitive color scheme for results
- **Smooth Animations**: Hover effects and transitions

---

**🔍 Veritas Frontend - Simple, Clean, Effective** ✨
