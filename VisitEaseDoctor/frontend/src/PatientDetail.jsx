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
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pdfs, setPdfs] = useState([]);

  // ChatGPT-like interface state
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi! How can I help you with this patient?' }
  ]);
  const [input, setInput] = useState('');
  const chatEndRef = useRef(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch(`http://localhost:8080/get-structured-data?user_id=${patient.id}`, {
          credentials: 'include'
        });
        if (!response.ok) {
          throw new Error('Failed to fetch user data');
        }
        const data = await response.json();
        setUserData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    const fetchPdfs = async () => {
      try {
        const fileTypes = ['labData', 'insuranceCard', 'doctorLetter'];
        const pdfPromises = fileTypes.map(async (type) => {
          const response = await fetch(`http://localhost:8080/get-pdf-by-type-for-user?user_id=${patient.id}&file_type=${type}`, {
            credentials: 'include'
          });
          if (response.ok) {
            const data = await response.json();
            return {
              name: `${type.charAt(0).toUpperCase() + type.slice(1)}.pdf`,
              url: data.url
            };
          }
          return null;
        });

        const pdfResults = await Promise.all(pdfPromises);
        setPdfs(pdfResults.filter(Boolean));
      } catch (err) {
        console.error('Error fetching PDFs:', err);
      }
    };

    fetchUserData();
    fetchPdfs();
  }, [patient.id]);

  // Scroll to top on mount
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  // Auto-scroll to the latest chat message
  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  async function handleSend(e) {
    e.preventDefault();
    if (!input.trim()) return;

    // Add the new user message to the chat
    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');

    try {
      const res = await fetch('http://localhost:8080/api/doctor-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: patient.id,
          messages: newMessages
        })
      });
      const data = await res.json();
      if (data.response) {
        setMessages(msgs => [...msgs, { role: 'assistant', content: data.response }]);
      } else if (data.error) {
        setMessages(msgs => [...msgs, { role: 'assistant', content: 'Error: ' + data.error }]);
      }
    } catch (err) {
      setMessages(msgs => [...msgs, { role: 'assistant', content: 'Error: ' + err.message }]);
    }
  }

  function Pill({ children }) {
    return <span className="patient-detail-pill">{children}</span>;
  }

  // Helper to render a limited number of pills (no '+N more' pill, max 5 words per pill)
  function renderLimitedPills(arr, max = 3) {
    if (!Array.isArray(arr)) return null;
    const shown = arr.slice(0, max);
    return (
      <>
        {shown.map((x, i) => {
          // Truncate to 5 words max
          const words = typeof x === 'string' ? x.split(' ') : [];
          const shortText = words.length > 5 ? words.slice(0, 5).join(' ') + ' ...' : x;
          return <Pill key={i}>{shortText}</Pill>;
        })}
      </>
    );
  }

  // Helper to render message content with **bold**
  function renderMessageWithBold(text) {
    if (typeof text !== 'string') return text;
    const parts = text.split(/(\*\*[^*]+\*\*)/g);
    return parts.map((part, i) => {
      if (/^\*\*[^*]+\*\*$/.test(part)) {
        return <strong key={i}>{part.slice(2, -2)}</strong>;
      }
      return <span key={i}>{part}</span>;
    });
  }

  if (loading) {
    return <div className="patient-detail-bg">Loading...</div>;
  }

  if (error) {
    return <div className="patient-detail-bg">Error: {error}</div>;
  }

  // Extract data from userData
  const doctorLetter = userData?.doctorLetter || {};
  const labData = userData?.labData || [];
  const medicationPlan = userData?.medicationPlan || {};
  const insuranceCard = userData?.insuranceCard || {};

  // Prepare data for display
  const displayData = {
    name: insuranceCard.name || patient?.name || 'Unknown Patient',
    time: new Date().toLocaleString(),
    pain: {
      location: doctorLetter.clinicalFindings || [],
      duration: doctorLetter.anamnesis || [],
      trigger: doctorLetter.assessment || [],
    },
    other: doctorLetter.plan || [],
    reportUrl: '#',
  };

  // PDF types to display
  const pdfTypes = [
    { type: 'labData', label: 'Lab Results' },
    { type: 'insuranceCard', label: 'Insurance Card' },
    { type: 'doctorLetter', label: 'Doctor Letter' },
  ];

  // Helper to get PDF by type
  const getPdfByType = (type) => pdfs.find(pdf => pdf.name.toLowerCase().includes(type.toLowerCase()));

  return (
    <div className="patient-detail-bg">
      {/* Back button */}
      <button onClick={onBack} style={{ position: 'absolute', top: 32, left: 32, background: 'none', border: 'none', color: '#2b4c4c', fontSize: '1.2rem', fontWeight: 600, cursor: 'pointer', zIndex: 20 }}>&larr; Back</button>
      {/* Download Report button */}
      <a
        href={displayData.reportUrl}
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
        <div className="patient-detail-name">{displayData.name}</div>
        <div className="patient-detail-time">{displayData.time}</div>
        <div className="patient-detail-grid">
          {/* Left: Pill containers */}
          <div className="patient-detail-left">
            <div className="patient-detail-card">
              <div className="patient-detail-card-title patient-detail-card-title-lg">Clinical Findings</div>
              <div style={{ fontWeight: 600, marginBottom: 4 }}>Location</div>
              <div className="patient-detail-pill-list">{renderLimitedPills(displayData.pain.location, 3)}</div>
              <div style={{ fontWeight: 600, marginBottom: 4 }}>Anamnesis</div>
              <div className="patient-detail-pill-list">{renderLimitedPills(displayData.pain.duration, 3)}</div>
              <div style={{ fontWeight: 600, marginBottom: 4 }}>Assessment</div>
              <div className="patient-detail-pill-list">{renderLimitedPills(displayData.pain.trigger, 3)}</div>
            </div>
            <div className="patient-detail-card">
              <div className="patient-detail-card-title">Treatment Plan</div>
              <div className="patient-detail-pill-list">{renderLimitedPills(displayData.other, 3)}</div>
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
                  {renderMessageWithBold(msg.content)}
                </div>
              ))}
              <div ref={chatEndRef} />
            </div>
            <form
              className="patient-detail-chat-input-row"
              onSubmit={handleSend}
            >
              <input
                className="patient-detail-chat-input"
                type="text"
                placeholder="Type your message..."
                value={input}
                onChange={e => setInput(e.target.value)}
              />
              <button
                className="patient-detail-chat-send-btn"
                type="submit"
              >
                Send
              </button>
            </form>
          </div>
          {/* Bottom: Fixed grid of key info cards */}
          <div className="patient-detail-bottom-row">
            {/* Insurance Information Card */}
            <div className="patient-detail-card" style={{ minWidth: 220, flex: 1, margin: 0 }}>
              <div className="patient-detail-card-title">Insurance Information</div>
              <div><b>Provider:</b> {insuranceCard.insuranceProvider || 'N/A'}</div>
              <div><b>Number:</b> {insuranceCard.insuranceNumber || 'N/A'}</div>
            </div>
            {/* Medication Plan Card */}
            <div className="patient-detail-card" style={{ minWidth: 220, flex: 1, margin: 0 }}>
              <div className="patient-detail-card-title">Medication Plan</div>
              {Array.isArray(medicationPlan.medication) && medicationPlan.medication.length > 0 ? (
                <div>
                  <b>Name:</b> {medicationPlan.medication[0].medicationName || 'N/A'}<br />
                  <b>Dosage:</b> {medicationPlan.medication[0].dosage || 'N/A'}
                </div>
              ) : (
                <div>N/A</div>
              )}
            </div>
            {/* Lab Results Card */}
            <div className="patient-detail-card" style={{ minWidth: 220, flex: 1, margin: 0 }}>
              <div className="patient-detail-card-title">Lab Results</div>
              {Array.isArray(labData) && labData.length > 0 ? (
                <div>
                  <b>Test:</b> {labData[0].testName || 'N/A'}<br />
                  <b>Value:</b> {labData[0].value || 'N/A'} {labData[0].unit || ''}
                </div>
              ) : (
                <div>N/A</div>
              )}
            </div>
          </div>
        </div>
        {/* PDF container */}
        <div className="patient-detail-pdf-container">
          {pdfTypes.map(({ type, label }) => {
            const pdf = getPdfByType(type);
            return (
              <div
                key={type}
                className="patient-detail-pdf-entry"
                style={{ display: 'flex', alignItems: 'center', cursor: pdf ? 'pointer' : 'default', padding: '1.1rem 2rem', borderBottom: '1px solid #e0e0e0' }}
                onClick={() => pdf && window.open(pdf.url, '_blank')}
              >
                <PdfIcon />
                <span style={{ fontWeight: 500, fontSize: '1.08em', color: pdf ? '#21756c' : '#888', flex: 1 }}>{label}</span>
                {pdf ? (
                  <a
                    href={pdf.url}
                    download={label.replace(/ /g, '_') + '.pdf'}
                    className="patient-detail-pdf-download"
                    style={{ marginLeft: 'auto' }}
                    onClick={e => e.stopPropagation()}
                    title={`Download ${label}`}
                  >
                    <DownloadIcon />
                  </a>
                ) : (
                  <span style={{ color: '#888', fontStyle: 'italic', marginLeft: 'auto' }}>No PDF</span>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default PatientDetail; 