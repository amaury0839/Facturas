import { useCallback, useEffect, useMemo, useState } from 'react';
import { createInvoice, fetchInvoices } from './api/client';
import type { InvoiceCreate, InvoiceRead } from './api/types';
import { Card } from './components/Card';
import { ExportPanel } from './components/ExportPanel';
import { Header } from './components/Header';
import { HealthStatus } from './components/HealthStatus';
import { InvoiceForm } from './components/InvoiceForm';
import { InvoiceList } from './components/InvoiceList';
import { InvoiceUploadCard } from './components/InvoiceUploadCard';

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

  const summary = useMemo(
    () => ({
      total: invoices.length,
      compras606: invoices.filter((invoice) => invoice.tipo_operacion === 'COMPRA_606').length,
      ventas607: invoices.filter((invoice) => invoice.tipo_operacion === 'VENTA_607').length,
      montoFacturado: invoices.reduce(
        (acc, invoice) => acc + (invoice.totals?.monto_facturado ?? 0),
        0,
      ),
      montoItbis: invoices.reduce(
        (acc, invoice) => acc + (invoice.totals?.itbis_facturado ?? 0),
        0,
      ),
    }),
    [invoices],
  );

  return (
    <div className="container">
      <Header />
      <Card
        title="Centro de control"
        description="Visualiza en un solo lugar el estado del backend y las facturas que ya se han registrado."
        action={
          <div style={{ display: 'flex', gap: 10 }}>
            <span className="badge success">
              <span className="status-dot" style={{ backgroundColor: '#22c55e' }} /> Listo para cargar
            </span>
            <span className="badge muted">SPA React + Vite</span>
          </div>
        }
      >
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: 14,
            marginTop: 12,
          }}
        >
          <div
            style={{
              padding: '14px 16px',
              background: '#eef2ff',
              borderRadius: 14,
              border: '1px solid #e2e8f0',
            }}
          >
            <p style={{ margin: '0 0 6px 0', color: '#475569', fontWeight: 600 }}>Facturas totales</p>
            <p style={{ margin: 0, fontSize: 28, fontWeight: 800, color: '#312e81' }}>{summary.total}</p>
            <p style={{ margin: '6px 0 0', color: '#475569' }}>Incluye compras 606 y ventas 607.</p>
          </div>
          <div
            style={{
              padding: '14px 16px',
              background: '#ecfeff',
              borderRadius: 14,
              border: '1px solid #e2e8f0',
            }}
          >
            <p style={{ margin: '0 0 6px 0', color: '#0f172a', fontWeight: 700 }}>Resumen por tipo</p>
            <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
              <span className="badge success">
                <span className="status-dot" style={{ backgroundColor: '#22c55e' }} /> Compras 606: {summary.compras606}
              </span>
              <span className="badge warning">
                <span className="status-dot" style={{ backgroundColor: '#f59e0b' }} /> Ventas 607: {summary.ventas607}
              </span>
            </div>
            <p style={{ margin: '8px 0 0', color: '#475569', fontSize: 13 }}>
              Usa el formulario de la izquierda para seguir agregando comprobantes.
            </p>
          </div>
          <div
            style={{
              padding: '14px 16px',
              background: '#f8fafc',
              borderRadius: 14,
              border: '1px solid #e2e8f0',
            }}
          >
            <p style={{ margin: '0 0 8px', color: '#0f172a', fontWeight: 700 }}>Totales rápidos</p>
            <ul style={{ margin: 0, paddingLeft: 18, color: '#475569', lineHeight: 1.6 }}>
              <li>
                Monto facturado:{' '}
                {summary.montoFacturado.toLocaleString('es-DO', {
                  style: 'currency',
                  currency: 'DOP',
                })}
              </li>
              <li>
                ITBIS cargado:{' '}
                {summary.montoItbis.toLocaleString('es-DO', {
                  style: 'currency',
                  currency: 'DOP',
                })}
              </li>
              <li>Revisa los adjuntos y exporta a Excel en el panel lateral.</li>
            </ul>
          </div>
        </div>
      </Card>
      <div className="grid">
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <InvoiceUploadCard onUploaded={loadInvoices} />
          <InvoiceForm onSubmit={handleCreate} />
          <InvoiceList invoices={invoices} loading={loading} error={error} onRefresh={loadInvoices} />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <HealthStatus />
          <ExportPanel />
          <Card title="Configuración rápida" description="Sigue estos pasos antes de probar en producción.">
            <ol style={{ margin: '8px 0 0', paddingLeft: 18, color: '#475569', lineHeight: 1.7 }}>
              <li>
                Copia <code>backend/.env.example</code> a <code>.env</code> y agrega tus secretos de Telegram o notificaciones.
              </li>
              <li>
                Define <code>VITE_API_BASE_URL</code> en el entorno de Vite para apuntar al backend (por defecto
                <strong> http://localhost:8000</strong> ).
              </li>
              <li>Levanta el backend con uvicorn y ejecuta `npm run dev` en el frontend.</li>
            </ol>
            <p style={{ margin: '10px 0 0', color: '#0f172a', fontWeight: 700 }}>Listo para facturar.</p>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default App;
