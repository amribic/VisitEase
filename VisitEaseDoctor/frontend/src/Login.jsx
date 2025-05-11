import { useState } from 'react';
import './Login.css';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // For now, just call onLogin with the username
    onLogin(username);
  };

  return (
    <div className="login-bg">
      <div className="login-card">
        <div className="login-header">
          <h2 className="login-title">Login</h2>
        </div>
        <form onSubmit={handleSubmit} className="login-form">
          <div className="login-field">
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="login-input"
              autoComplete="off"
            />
          </div>
          <div className="login-field">
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="login-input"
              autoComplete="off"
            />
          </div>
          <button type="submit" className="login-btn">Login</button>
        </form>
      </div>
    </div>
  );
}

export default Login; 