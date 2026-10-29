import React, { useState, useEffect } from 'react';
import './App.css';

const SAMPLE_CODES = {
  python_billing: `def calc(x, y, z):
    # Messy order calculation with magic numbers and poor naming
    t = 0
    for i in x:
        t = t + i['p'] * i['q']
    if z > 0:
        d = t * z
    else:
        d = 0
    tax = (t - d) * 0.0825
    return t - d + tax`,
  python_nested: `def check_perms(user, action):
    # Complex deeply nested condition ladder
    if user != None:
        if user.get("is_active") == True:
            if user.get("is_superuser") == True:
                return True
            else:
                if action == "read":
                    return True
                elif action == "write":
                    if "editor" in user.get("roles", []):
                        return True
                    elif "admin" in user.get("roles", []):
                        return True
    return False`,
  javascript_async: `function getUserData(userId, callback) {
    // Legacy nested callback with no standard error handling or timeout
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/users/" + userId, true);
    xhr.onload = function() {
        if (xhr.status == 200) {
            var data = JSON.parse(xhr.responseText);
            callback(null, data);
        } else {
            callback("Error " + xhr.status);
        }
    };
    xhr.send();
}`,
  sql_security: `def get_user_account(user_id):
    # CRITICAL: Vulnerable to SQL injection (CWE-89)
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = '{user_id}' AND is_active = 1"
    cursor.execute(query)
    return cursor.fetchone()`
};

export default function App() {
  const [code, setCode] = useState(SAMPLE_CODES.python_billing);
  const [goal, setGoal] = useState('readability');
  const [language, setLanguage] = useState('python');
  const [context, setContext] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState('code'); // 'code' | 'explanations' | 'diff'
  const [copyStatus, setCopyStatus] = useState('Copy Code');
  const [health, setHealth] = useState({
    status: 'checking',
    gemini_configured: false,
    gemini_model: 'gemini-2.5-flash',
    nebius_configured: false,
    nebius_model: 'nebius/nvidia/Nemotron-3_5-Lightning',
    groq_configured: false,
    groq_model: 'llama-3.1-8b-instant',
    active_provider: 'demo',
    demo_mode: true
  });

  useEffect(() => {
    fetchHealth();
  }, []);

  const fetchHealth = async () => {
    try {
      const res = await fetch('/health');
      if (res.ok) {
        const data = await res.json();
        setHealth(data);
      }
    } catch (e) {
      console.warn('Backend currently offline or proxy connecting...');
    }
  };

  const handleRefactor = async () => {
    if (!code || code.trim().length < 5) {
      setError('Validation Error: Source code must contain at least 5 characters to refactor.');
      setResult(null);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await fetch('/api/refactor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          code,
          goal,
          language,
          context: context.trim() ? context.trim() : null
        })
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        throw new Error(data.detail || data.error || `HTTP Error ${res.status}`);
      }

      setResult(data);
      setActiveTab('code');
    } catch (err) {
      setError(err.message || 'An unexpected error occurred during refactoring.');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (!result?.refactored_code) return;
    navigator.clipboard.writeText(result.refactored_code);
    setCopyStatus('Copied to Clipboard! ✓');
    setTimeout(() => setCopyStatus('Copy Code'), 2200);
  };

  const handleDownload = () => {
    if (!result?.refactored_code) return;
    const blob = new Blob([result.refactored_code], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const ext = result.language === 'python' ? 'py' : (result.language === 'javascript' ? 'js' : (result.language === 'typescript' ? 'ts' : 'txt'));
    a.download = `refactored_${result.goal}_${Date.now()}.${ext}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const loadSample = (key) => {
    setCode(SAMPLE_CODES[key]);
    setError(null);
    if (key === 'sql_security') {
      setGoal('security');
      setLanguage('python');
    } else if (key === 'javascript_async') {
      setGoal('modernize');
      setLanguage('javascript');
    } else if (key === 'python_nested') {
      setGoal('complexity');
      setLanguage('python');
    } else {
      setGoal('readability');
      setLanguage('python');
    }
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="header-left">
          <div className="logo-icon">⚡</div>
          <div className="logo-text">
            <h1>Refactor<span>.ai</span></h1>
            <p className="tagline">Autonomous Multi-Model Code Refactoring • Google Gemini &amp; NVIDIA Nemotron</p>
          </div>
        </div>

        <div className="header-right">
          <div className="provider-badge">
            <span className={`provider-dot ${health.gemini_configured ? 'dot-blue' : (health.nebius_configured ? 'dot-green' : (health.groq_configured ? 'dot-amber' : 'dot-demo'))}`}></span>
            <span>
              {health.gemini_configured
                ? 'Google Gemini Flash (Active Live AI)'
                : (health.nebius_configured
                    ? 'NVIDIA Nemotron (Nebius Live AI)'
                    : (health.groq_configured
                        ? 'Groq Fallback (Live AI)'
                        : 'Deterministic Demo Mode'))}
            </span>
          </div>
        </div>
      </header>

      {/* Provider Status Banner */}
      <div className={`demo-banner ${result?.demo_mode || health.demo_mode ? 'banner-demo' : 'banner-live'}`}>
        <span>
          {result?.demo_mode || health.demo_mode ? (
            <>
              ℹ️ <strong>Deterministic Demo Mode:</strong> Self-contained baseline fixtures active. Set <code>GEMINI_API_KEY</code> or <code>NEBIUS_API_KEY</code> in <code>.env</code> for live cloud inference.
            </>
          ) : (
            <>
              ⚡ <strong>Live AI Mode Active:</strong> Output generated by <strong>{result?.provider?.toUpperCase() || health.active_provider.toUpperCase()}</strong> using model <code>{result?.model || health.gemini_model}</code>.
            </>
          )}
        </span>
        <span style={{ fontSize: '0.75rem', opacity: 0.9 }}>
          Compliance: <strong>NVIDIA Nemotron via Nebius Supported</strong>
        </span>
      </div>

      {/* Main Workspace */}
      <main className="main-content">
        {/* Left Column: Input Code */}
        <section className="panel">
          <div className="panel-header">
            <span className="panel-title">
              <span>📝</span> Source Code
            </span>
            <div className="panel-actions">
              <button className="btn-secondary" onClick={() => loadSample('python_billing')}>Billing (Readability)</button>
              <button className="btn-secondary" onClick={() => loadSample('python_nested')}>Nested (Complexity)</button>
              <button className="btn-secondary" onClick={() => loadSample('javascript_async')}>JS XHR (Modernize)</button>
              <button className="btn-secondary" onClick={() => loadSample('sql_security')}>SQL (Security)</button>
            </div>
          </div>

          <div className="controls-bar">
            <div className="control-row">
              <div className="control-group">
                <span className="control-label">Objective:</span>
                <div className="goal-pills">
                  {[
                    { id: 'readability', label: '📖 Readability' },
                    { id: 'complexity', label: '🔀 Reduce Complexity' },
                    { id: 'performance', label: '⚡ Performance' },
                    { id: 'potential_bugs', label: '🐛 Bug Detection' },
                    { id: 'maintainability', label: '🛠️ Maintainability' },
                    { id: 'add_comments', label: '💬 Add Comments' },
                    { id: 'explain_code', label: '🔍 Explain Code' },
                    { id: 'add_types', label: '🏷️ Add Types' },
                    { id: 'security', label: '🛡️ Security' },
                    { id: 'modernize', label: '✨ Modernize' },
                  ].map((g) => (
                    <button
                      key={g.id}
                      className={`goal-pill ${goal === g.id ? 'active' : ''}`}
                      onClick={() => setGoal(g.id)}
                    >
                      {g.label}
                    </button>
                  ))}
                </div>
              </div>

              <div className="control-group">
                <span className="control-label">Language:</span>
                <select
                  className="select-input"
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                >
                  <option value="auto">Auto-Detect</option>
                  <option value="python">Python</option>
                  <option value="javascript">JavaScript</option>
                  <option value="typescript">TypeScript</option>
                  <option value="java">Java</option>
                  <option value="go">Go</option>
                  <option value="rust">Rust</option>
                  <option value="cpp">C++</option>
                  <option value="sql">SQL</option>
                </select>
              </div>
            </div>
          </div>

          <div className="editor-container">
            <textarea
              className="code-textarea"
              value={code}
              onChange={(e) => {
                setCode(e.target.value);
                if (error) setError(null);
              }}
              placeholder="// Paste source code to refactor..."
              spellCheck="false"
            />
          </div>

          <div className="panel-footer">
            <span className="char-count">{code.length} characters</span>
            <button
              className="btn-primary"
              onClick={handleRefactor}
              disabled={loading}
            >
              {loading ? (
                <>
                  <div className="spinner"></div>
                  Analyzing with AI...
                </>
              ) : (
                <>
                  <span>⚡</span> Refactor Code
                </>
              )}
            </button>
          </div>
        </section>

        {/* Right Column: Refactored Result */}
        <section className="panel">
          <div className="panel-header">
            <span className="panel-title">
              <span>✨</span> Refactored Code &amp; Analysis
            </span>
            {result && (
              <div className="panel-actions">
                <button className="btn-secondary" onClick={handleCopy}>
                  {copyStatus}
                </button>
                <button className="btn-secondary" onClick={handleDownload}>
                  Download
                </button>
              </div>
            )}
          </div>

          {result && (
            <div className="tabs-bar">
              <button
                className={`tab-btn ${activeTab === 'code' ? 'active' : ''}`}
                onClick={() => setActiveTab('code')}
              >
                Refactored Code
              </button>
              <button
                className={`tab-btn ${activeTab === 'explanations' ? 'active' : ''}`}
                onClick={() => setActiveTab('explanations')}
              >
                Insights &amp; Explanations ({result.explanations?.length || 0})
              </button>
              <button
                className={`tab-btn ${activeTab === 'diff' ? 'active' : ''}`}
                onClick={() => setActiveTab('diff')}
              >
                Side-by-Side Comparison
              </button>
            </div>
          )}

          <div className="editor-container" style={{ display: 'flex', flexDirection: 'column' }}>
            {error && (
              <div style={{ padding: '1rem', background: '#451a1a', borderBottom: '1px solid #7f1d1d', color: '#fca5a5', fontSize: '0.85rem' }}>
                ⚠️ <strong>Error:</strong> {error}
              </div>
            )}

            {!result && !loading && (
              <div className="empty-state">
                <div className="empty-icon">🧠</div>
                <h3 style={{ fontSize: '1.05rem', color: '#cbd5e1' }}>Autonomous Refactoring Engine Ready</h3>
                <p style={{ maxWidth: '440px', fontSize: '0.85rem' }}>
                  Select an objective (Readability, Complexity, Performance, Bugs, Security), paste your source code, and click <strong>Refactor Code</strong>.
                </p>
              </div>
            )}

            {loading && (
              <div className="empty-state">
                <div className="spinner" style={{ width: '36px', height: '36px', borderWidth: '3px' }}></div>
                <p style={{ fontSize: '0.9rem', color: '#93c5fd' }}>Synthesizing AST, executing refactoring passes &amp; verifying safety boundaries...</p>
              </div>
            )}

            {result && !loading && activeTab === 'code' && (
              <>
                <pre className="code-display">
                  <code>{result.refactored_code}</code>
                </pre>
                <div style={{ padding: '0.65rem 1rem', background: '#1c1917', borderTop: '1px solid #292524', color: '#fbbf24', fontSize: '0.75rem' }}>
                  ⚠️ {result.warning}
                </div>
              </>
            )}

            {result && !loading && activeTab === 'explanations' && (
              <div className="explanation-container">
                <div className="section-box" style={{ borderColor: '#3b82f6' }}>
                  <h4><span>📋</span> Executive Summary</h4>
                  <p style={{ fontSize: '0.85rem', color: '#e2e8f0', lineHeight: 1.6 }}>{result.explanation}</p>
                </div>

                <div className="section-box">
                  <h4><span>💡</span> What Changed &amp; Why</h4>
                  <ul className="bullet-list">
                    {result.explanations?.map((exp, idx) => (
                      <li key={idx}>{exp}</li>
                    ))}
                  </ul>
                </div>

                <div className="section-box">
                  <h4><span>🚀</span> Key Improvements</h4>
                  <ul className="bullet-list">
                    {result.improvements?.map((imp, idx) => (
                      <li key={idx}>{imp}</li>
                    ))}
                  </ul>
                </div>

                <div className="section-box" style={{ borderColor: '#f59e0b' }}>
                  <h4><span>⚠️</span> Risks, Tradeoffs &amp; Assumptions</h4>
                  <ul className="bullet-list">
                    {(result.risks || result.risks_and_tradeoffs)?.map((risk, idx) => (
                      <li key={idx}>{risk}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {result && !loading && activeTab === 'diff' && (
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', height: '100%', minHeight: '400px', borderTop: '1px solid var(--border-color)' }}>
                <div style={{ borderRight: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column' }}>
                  <div style={{ background: '#181e2e', padding: '0.4rem 0.75rem', fontSize: '0.75rem', color: '#94a3b8', borderBottom: '1px solid var(--border-color)' }}>
                    Original Code ({result.original_code?.split('\n').length || 0} lines)
                  </div>
                  <pre style={{ flex: 1, padding: '0.75rem', fontSize: '0.8rem', color: '#94a3b8', overflow: 'auto', background: '#0a0d14' }}>
                    <code>{result.original_code}</code>
                  </pre>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column' }}>
                  <div style={{ background: '#142921', padding: '0.4rem 0.75rem', fontSize: '0.75rem', color: '#34d399', borderBottom: '1px solid var(--border-color)' }}>
                    Refactored Code ({result.refactored_code?.split('\n').length || 0} lines)
                  </div>
                  <pre style={{ flex: 1, padding: '0.75rem', fontSize: '0.8rem', color: '#38bdf8', overflow: 'auto', background: '#0b111e' }}>
                    <code>{result.refactored_code}</code>
                  </pre>
                </div>
              </div>
            )}
          </div>

          <div className="panel-footer">
            {result ? (
              <div className="meta-chip">
                <span>Mode: <strong>{result.demo_mode ? 'Deterministic Demo' : 'Live Cloud AI'}</strong></span>
                <span>•</span>
                <span>Provider: <strong>{result.provider}</strong></span>
                <span>•</span>
                <span>Model: <strong>{result.model}</strong></span>
                <span>•</span>
                <span>Latency: <strong>{result.processing_ms}ms</strong></span>
              </div>
            ) : (
              <span className="char-count">Awaiting user input...</span>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
