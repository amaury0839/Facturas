import { useCallback, useEffect, useState } from 'react';
import { createInvoice, fetchInvoices } from './api/client';
import type { InvoiceCreate, InvoiceRead } from './api/types';
import { Card } from './components/Card';
import { Header } from './components/Header';
import { HealthStatus } from './components/HealthStatus';
import { InvoiceForm } from './components/InvoiceForm';
import { InvoiceList } from './components/InvoiceList';

function App() {
  const [invoices, setInvoices] = useState<InvoiceRead[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadInvoices = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchInvoices();
      setInvoices(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No se pudo obtener el listado');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadInvoices();
  }, [loadInvoices]);

  const handleCreate = async (payload: InvoiceCreate) => {
    await createInvoice(payload);
    await loadInvoices();
  };

  return (
    <div className="container">
      <Header />
      <div className="grid">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <InvoiceForm onSubmit={handleCreate} />
          <InvoiceList invoices={invoices} loading={loading} error={error} onRefresh={loadInvoices} />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <HealthStatus />
          <Card title="Configuración rápida" description="Define la URL base del API con VITE_API_BASE_URL.">
            <p style={{ margin: '6px 0', color: '#475569' }}>
              Por defecto apunta a <strong>http://localhost:8000</strong>. Ajusta la variable de entorno de Vite si despliegas el
              backend en otra ubicación.
            </p>
            <p style={{ margin: '6px 0', color: '#475569' }}>
              Utiliza este panel para validar flujos básicos: cargar facturas, revisar estados de validación y confirmar que el
              API responde.
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default App;
