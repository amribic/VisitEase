import React from 'react';
import './PatientList.css';

function Pill({ children }) {
  return (
    <span style={{
      display: 'inline-block',
      background: '#f6f6f6',
      borderRadius: '999px',
      padding: '0.4em 1.2em',
      margin: '0.2em 0.5em 0.2em 0',
      fontSize: '1.05em',
      color: '#222',
      fontWeight: 500,
      border: '1px solid #e0e0e0',
    }}>{children}</span>
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
    treatment: ['Painkillers'],
    sickNote: ['Yes'],
    additional: ['Nausea'],
  };

  return (
    <div style={{ minHeight: '100vh', background: '#fff', width: '100vw', position: 'relative' }}>
      {/* Back button */}
      <button onClick={onBack} style={{ position: 'absolute', top: 32, left: 32, background: 'none', border: 'none', color: '#2b4c4c', fontSize: '1.2rem', fontWeight: 600, cursor: 'pointer', zIndex: 20 }}>&larr; Back</button>
      {/* Copy button */}
      <button style={{ position: 'absolute', top: 40, right: 56, background: 'none', border: 'none', color: '#21756c', fontWeight: 600, fontSize: '1.08rem', display: 'flex', alignItems: 'center', gap: 6, cursor: 'pointer' }}>
        <svg width="20" height="20" fill="none" stroke="#21756c" strokeWidth="2" viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><rect x="3" y="3" width="13" height="13" rx="2"/></svg>
        Copy
      </button>
      <div style={{ maxWidth: 1800, margin: '0 auto', padding: '3.5rem 3rem 2rem 3rem' }}>
        <div style={{ marginBottom: 8, color: '#21756c', fontWeight: 700, fontSize: '1.2rem' }}>Medical History</div>
        <div style={{ fontWeight: 800, fontSize: '2rem', marginBottom: 4 }}>{data.name}</div>
        <div style={{ color: '#888', fontSize: '1.08rem', marginBottom: 24 }}>{data.time}</div>
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: 20 }}>
          {/* Pain & Other */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
            <div style={{ border: '1px solid #e0e0e0', borderRadius: 12, padding: '1.5rem', background: '#fff' }}>
              <div style={{ fontWeight: 700, fontSize: '1.25rem', marginBottom: 16 }}>Pain</div>
              <div style={{ fontWeight: 600, marginBottom: 4 }}>Location</div>
              <div style={{ marginBottom: 12 }}>{data.pain.location.map((x, i) => <Pill key={i}>{x}</Pill>)}</div>
              <div style={{ fontWeight: 600, marginBottom: 4 }}>Duration</div>
              <div style={{ marginBottom: 12 }}>{data.pain.duration.map((x, i) => <Pill key={i}>{x}</Pill>)}</div>
              <div style={{ fontWeight: 600, marginBottom: 4 }}>Suspected Trigger</div>
              <div>{data.pain.trigger.map((x, i) => <Pill key={i}>{x}</Pill>)}</div>
            </div>
            <div style={{ border: '1px solid #e0e0e0', borderRadius: 12, padding: '1.5rem', background: '#fff' }}>
              <div style={{ fontWeight: 700, fontSize: '1.15rem', marginBottom: 10 }}>Other</div>
              {data.other.map((x, i) => <Pill key={i}>{x}</Pill>)}
            </div>
          </div>
          {/* Treatment & Sick Note */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
            <div style={{ border: '1px solid #e0e0e0', borderRadius: 12, padding: '1.5rem', background: '#fff', marginBottom: 20 }}>
              <div style={{ fontWeight: 700, fontSize: '1.15rem', marginBottom: 10 }}>Previous Treatment</div>
              {data.treatment.map((x, i) => <Pill key={i}>{x}</Pill>)}
            </div>
            <div style={{ border: '1px solid #e0e0e0', borderRadius: 12, padding: '1.5rem', background: '#fff' }}>
              <div style={{ fontWeight: 700, fontSize: '1.15rem', marginBottom: 10 }}>Sick Note Requested</div>
              {data.sickNote.map((x, i) => <Pill key={i}>{x}</Pill>)}
            </div>
          </div>
          {/* Additional Complaints */}
          <div style={{ border: '1px solid #e0e0e0', borderRadius: 12, padding: '1.5rem', background: '#fff', display: 'flex', flexDirection: 'column', gap: 10 }}>
            <div style={{ fontWeight: 700, fontSize: '1.15rem', marginBottom: 10 }}>Additional Complaints</div>
            {data.additional.map((x, i) => <Pill key={i}>{x}</Pill>)}
          </div>
        </div>
      </div>
    </div>
  );
}

export default PatientDetail; 