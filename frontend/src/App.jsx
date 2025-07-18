import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputText.trim()) {
      setError('Please enter a news article or claim to verify');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:8000/api/v1/verify/', {
        text: inputText,
        claim_type: 'article',
        language: 'en'
      });

      setResult(response.data);
    } catch (err) {
      console.error('Error:', err);
      setError(
        err.response?.data?.detail || 
        'Failed to verify the article. Please check if the backend is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  const getVerdictColor = (verdict) => {
    switch (verdict?.toUpperCase()) {
      case 'MOST_LIKELY_TRUE': return '#10b981';
      case 'LIKELY_TRUE_NEEDS_SUPPORT': return '#22c55e';
      case 'INCONCLUSIVE_MIXED': return '#f59e0b';
      case 'LIKELY_FALSE': return '#ef4444';
      case 'INSUFFICIENT_DATA': return '#6b7280';
      // Legacy support
      case 'TRUE': return '#10b981';
      case 'FALSE': return '#ef4444';
      case 'MIXED': return '#f59e0b';
      default: return '#6b7280';
    }
  };

  const getVerdictEmoji = (verdict) => {
    switch (verdict?.toUpperCase()) {
      case 'MOST_LIKELY_TRUE': return '🟢';
      case 'LIKELY_TRUE_NEEDS_SUPPORT': return '🟡';
      case 'INCONCLUSIVE_MIXED': return '🟠';
      case 'LIKELY_FALSE': return '🔴';
      case 'INSUFFICIENT_DATA': return '⚫';
      // Legacy support
      case 'TRUE': return '✅';
      case 'FALSE': return '❌';
      case 'MIXED': return '⚠️';
      default: return '❓';
    }
  };

  const getVerdictDisplayText = (verdict) => {
    switch (verdict?.toUpperCase()) {
      case 'MOST_LIKELY_TRUE': return 'Most Likely True';
      case 'LIKELY_TRUE_NEEDS_SUPPORT': return 'Likely True (Needs More Support)';
      case 'INCONCLUSIVE_MIXED': return 'Inconclusive / Mixed Evidence';
      case 'LIKELY_FALSE': return 'Likely False';
      case 'INSUFFICIENT_DATA': return 'Not Enough Data';
      // Legacy support
      case 'TRUE': return 'True';
      case 'FALSE': return 'False';
      case 'MIXED': return 'Mixed';
      default: return 'Unknown';
    }
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🔍 Veritas</h1>
          <p>Advanced Fact-Checking System</p>
        </header>

        <form onSubmit={handleSubmit} className="form">
          <div className="input-group">
            <label htmlFor="article-input">
              Enter News Article or Claim to Verify:
            </label>
            <textarea
              id="article-input"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Paste your news article, headline, or claim here..."
              rows={6}
              disabled={loading}
            />
          </div>

          <button 
            type="submit" 
            disabled={loading || !inputText.trim()}
            className="submit-btn"
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing...
              </>
            ) : (
              'Verify Claim'
            )}
          </button>
        </form>

        {error && (
          <div className="error">
            <strong>Error:</strong> {error}
          </div>
        )}

        {result && (
          <div className="results">
            <h2>📊 Verification Results</h2>
            
            <div className="result-grid">
              <div className="result-card">
                <h3>Truth Score</h3>
                <div className="score">
                  {Math.round((result.truth_score || 0) * 100)}%
                </div>
                <div className="score-bar">
                  <div 
                    className="score-fill"
                    style={{ 
                      width: `${(result.truth_score || 0) * 100}%`,
                      backgroundColor: result.truth_score > 0.7 ? '#10b981' : 
                                     result.truth_score > 0.4 ? '#f59e0b' : '#ef4444'
                    }}
                  ></div>
                </div>
              </div>

              <div className="result-card">
                <h3>Confidence</h3>
                <div className="score">
                  {Math.round((result.confidence || 0) * 100)}%
                </div>
                <div className="score-bar">
                  <div 
                    className="score-fill"
                    style={{ 
                      width: `${(result.confidence || 0) * 100}%`,
                      backgroundColor: '#3b82f6'
                    }}
                  ></div>
                </div>
              </div>

              <div className="result-card verdict-card">
                <h3>Verdict</h3>
                <div
                  className="verdict"
                  style={{ color: getVerdictColor(result.verdict) }}
                >
                  <span className="verdict-emoji">{getVerdictEmoji(result.verdict)}</span>
                  <span className="verdict-text">{getVerdictDisplayText(result.verdict)}</span>
                </div>
              </div>

              <div className="result-card">
                <h3>Processing Time</h3>
                <div className="score">
                  {result.processing_time?.toFixed(2) || 0}s
                </div>
              </div>
            </div>

            {result.matching_articles && result.matching_articles.length > 0 && (
              <div className="sources">
                <h3>📰 Supporting Sources ({result.matching_articles.length})</h3>
                <div className="sources-list">
                  {result.matching_articles.slice(0, 3).map((article, index) => (
                    <div key={index} className="source-item">
                      <h4>{article.title}</h4>
                      <p className="source-url">{article.url}</p>
                      <p className="similarity">
                        Similarity: {Math.round((article.similarity_score || 0) * 100)}%
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {result.contradicting_articles && result.contradicting_articles.length > 0 && (
              <div className="sources contradicting">
                <h3>⚠️ Contradicting Sources ({result.contradicting_articles.length})</h3>
                <div className="sources-list">
                  {result.contradicting_articles.slice(0, 3).map((article, index) => (
                    <div key={index} className="source-item">
                      <h4>{article.title}</h4>
                      <p className="source-url">{article.url}</p>
                      <p className="similarity">
                        Similarity: {Math.round((article.similarity_score || 0) * 100)}%
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
