import React, { useState, useRef, useEffect } from 'react';
import './PatientDetail.css';

function PdfIcon() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#d32f2f" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: 12 }}>
      <rect x="4" y="2" width="16" height="20" rx="2" fill="#fff3f3" stroke="#d32f2f"/>
      <path d="M8 6h8M8 10h8M8 14h4" stroke="#d32f2f"/>
    </svg>
  );
}

function DownloadIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#21756c" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 5v12m0 0l-4-4m4 4l4-4" />
      <rect x="4" y="19" width="16" height="2" rx="1" fill="#21756c" />
    </svg>
  );
}

function PatientDetail({ patient, onBack }) {
  // Sample data for demonstration (replace with real patient data as needed)
  const data = {
    name: patient?.name || 'Mr. Krüger, Nils',
    time: 'Today, 11:26 AM',
    pain: {
      location: ['Forehead, temples and/or neck'],
      duration: ['Several times a week', 'For a few weeks'],
      trigger: ['Stress or psychological strain', 'Sleep problems'],
    },
    other: ['Patient already knows these pains'],
    pdfs: [
      { name: 'Lab Results.pdf', url: '#' },
      { name: 'Prescription.pdf', url: '#' },
      { name: 'Discharge Summary.pdf', url: '#' },
    ],
    reportUrl: '#',
  };

  function Pill({ children }) {
    return <span className="patient-detail-pill">{children}</span>;
  }

  // ChatGPT-like interface state
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! How can I help you with this patient?' }
  ]);
  const [input, setInput] = useState('');
  const chatEndRef = useRef(null);

  // Scroll to top on mount
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  function handleSend(e) {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages(msgs => [
      ...msgs,
      { role: 'user', content: input }
    ]);
    // Simulate assistant reply
    setTimeout(() => {
      setMessages(msgs => [
        ...msgs,
        { role: 'assistant', content: 'This is a sample response from the assistant.' }
      ]);
    }, 800);
    setInput('');
  }

  return (
    <div className="patient-detail-bg">
      {/* Back button */}
      <button onClick={onBack} style={{ position: 'absolute', top: 32, left: 32, background: 'none', border: 'none', color: '#2b4c4c', fontSize: '1.2rem', fontWeight: 600, cursor: 'pointer', zIndex: 20 }}>&larr; Back</button>
      {/* Download Report button */}
      <a
        href={data.reportUrl}
        download="Patient_Report.pdf"
        style={{
          position: 'absolute',
          top: 36,
          right: 56,
          background: '#fff',
          border: '1.5px solid #e0e0e0',
          color: '#21756c',
          fontWeight: 600,
          fontSize: '1.08rem',
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          cursor: 'pointer',
          borderRadius: 8,
          padding: '0.5rem 1.2rem',
          boxShadow: '0 2px 8px rgba(44,62,80,0.04)',
          textDecoration: 'none',
          transition: 'background 0.15s, border-color 0.15s',
        }}
        title="Download Report"
      >
        <DownloadIcon />
        Download Report
      </a>
      <div className="patient-detail-main">
        <div className="patient-detail-section-title">Medical History</div>
        <div className="patient-detail-name">{data.name}</div>
        <div className="patient-detail-time">{data.time}</div>
        <div className="patient-detail-grid">
          {/* Left: Pill containers */}
          <div className="patient-detail-left">
            <div className="patient-detail-card">
              <div className="patient-detail-card-title patient-detail-card-title-lg">Pain</div>
              <div style={{ fontWeight: 600, marginBottom: 4 }}>Location</div>
              <div style={{ marginBottom: 12 }}>{data.pain.location.map((x, i) => <Pill key={i}>{x}</Pill>)}</div>
              <div style={{ fontWeight: 600, marginBottom: 4 }}>Duration</div>
              <div style={{ marginBottom: 12 }}>{data.pain.duration.map((x, i) => <Pill key={i}>{x}</Pill>)}</div>
              <div style={{ fontWeight: 600, marginBottom: 4 }}>Suspected Trigger</div>
              <div>{data.pain.trigger.map((x, i) => <Pill key={i}>{x}</Pill>)}</div>
            </div>
            <div className="patient-detail-card">
              <div className="patient-detail-card-title">Other</div>
              {data.other.map((x, i) => <Pill key={i}>{x}</Pill>)}
            </div>
          </div>
          {/* Right: Chat */}
          <div className="patient-detail-chat-container">
            <div className="patient-detail-chat-messages">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`patient-detail-chat-message ${msg.role}`}
                >
                  {msg.content}
                </div>
              ))}
              <div ref={chatEndRef} />
            </div>
            <form className="patient-detail-chat-input-row" onSubmit={handleSend}>
              <input
                className="patient-detail-chat-input"
                type="text"
                placeholder="Type your message..."
                value={input}
                onChange={e => setInput(e.target.value)}
              />
              <button className="patient-detail-chat-send-btn" type="submit">Send</button>
            </form>
          </div>
          {/* Bottom: Full-width row of cards */}
          <div className="patient-detail-bottom-row">
            <div className="patient-detail-card" style={{ minWidth: 220, flex: 1, margin: 0 }}>
              <div className="patient-detail-card-title">Previous Treatment</div>
              <Pill>Painkillers</Pill>
            </div>
            <div className="patient-detail-card" style={{ minWidth: 220, flex: 1, margin: 0 }}>
              <div className="patient-detail-card-title">Sick Note Requested</div>
              <Pill>Yes</Pill>
            </div>
            <div className="patient-detail-card" style={{ minWidth: 220, flex: 1, margin: 0 }}>
              <div className="patient-detail-card-title">Additional Complaints</div>
              <Pill>Nausea</Pill>
            </div>
          </div>
        </div>
        {/* PDF container */}
        <div className="patient-detail-pdf-container">
          {data.pdfs.map((pdf, i) => (
            <div
              key={pdf.name}
              className="patient-detail-pdf-entry"
              onClick={() => window.open(pdf.url, '_blank')}
            >
              <PdfIcon />
              {pdf.name}
              <a
                href={pdf.url}
                download={pdf.name}
                className="patient-detail-pdf-download"
                onClick={e => e.stopPropagation()}
                title={`Download ${pdf.name}`}
              >
                <DownloadIcon />
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default PatientDetail; 