import { useEffect, useState } from 'react';
import { fetchHealth } from '../api/client';
import type { HealthResponse } from '../api/types';
import { Card } from './Card';

export function HealthStatus() {
  const [status, setStatus] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHealth()
      .then(setStatus)
      .catch((err: Error) => setError(err.message));
  }, []);

  return (
    <Card title="Estado del backend" description="Ping a /health para confirmar disponibilidad.">
      {status && (
        <div className="badge success">
          <span className="status-dot" style={{ backgroundColor: '#22c55e' }} /> Online · {status.status}
        </div>
      )}
      {error && (
        <div className="badge warning" style={{ marginTop: 6 }}>
          <span className="status-dot" style={{ backgroundColor: '#f59e0b' }} /> {error}
        </div>
      )}
      {!status && !error && <p style={{ margin: 0, color: '#475569' }}>Consultando servicio...</p>}
    </Card>
  );
}
