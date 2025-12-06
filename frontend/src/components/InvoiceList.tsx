import type { InvoiceRead } from '../api/types';
import { Card } from './Card';

interface InvoiceListProps {
  invoices: InvoiceRead[];
  loading: boolean;
  error?: string | null;
  onRefresh: () => void;
}

const validationColors: Record<string, string> = {
  VALIDADO: '#16a34a',
  OBSERVADO: '#ea580c',
  PENDIENTE: '#6b7280',
};

const ocrColors: Record<string, string> = {
  PROCESADO: '#16a34a',
  PENDIENTE: '#6b7280',
  ERROR: '#dc2626',
};

function StatusBadge({ label, color }: { label: string; color: string }) {
  return (
    <span
      className="badge"
      style={{
        backgroundColor: '#f8fafc',
        color: color || '#334155',
        border: `1px solid ${color || '#e2e8f0'}`,
      }}
    >
      <span className="status-dot" style={{ backgroundColor: color || '#94a3b8' }} />
      {label}
    </span>
  );
}

export function InvoiceList({ invoices, loading, error, onRefresh }: InvoiceListProps) {
  return (
    <Card
      title="Facturas recientes"
      description="Consulta y valida las facturas registradas en el backend."
      action={
        <button className="button" type="button" onClick={onRefresh} disabled={loading}>
          {loading ? 'Actualizando...' : 'Refrescar'}
        </button>
      }
    >
      {error && <div className="toast error">{error}</div>}
      {loading && <p style={{ margin: '6px 0', color: '#475569' }}>Cargando facturas...</p>}
      {!loading && invoices.length === 0 && (
        <p style={{ margin: '6px 0', color: '#475569' }}>No hay facturas registradas todavía.</p>
      )}
      {invoices.length > 0 && (
        <div style={{ overflowX: 'auto' }}>
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Tipo</th>
                <th>NCF</th>
                <th>RNC Emisor</th>
                <th>Fecha</th>
                <th>OCR</th>
                <th>Validación</th>
              </tr>
            </thead>
            <tbody>
              {invoices.map((invoice) => (
                <tr key={invoice.id}>
                  <td>{invoice.id}</td>
                  <td>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                      <span style={{ fontWeight: 700 }}>{invoice.tipo_operacion}</span>
                      <span style={{ color: '#475569', fontSize: 13 }}>{invoice.tipo_documento}</span>
                    </div>
                  </td>
                  <td>
                    <div style={{ fontWeight: 700 }}>{invoice.ncf}</div>
                    {invoice.ncf_modificado && (
                      <div style={{ color: '#475569', fontSize: 13 }}>Modifica: {invoice.ncf_modificado}</div>
                    )}
                  </td>
                  <td>
                    <div style={{ fontWeight: 700 }}>{invoice.rnc_emisor}</div>
                    {invoice.nombre_emisor && (
                      <div style={{ color: '#475569', fontSize: 13 }}>{invoice.nombre_emisor}</div>
                    )}
                  </td>
                  <td>{invoice.fecha_comprobante}</td>
                  <td>
                    <StatusBadge
                      label={invoice.ocr_status}
                      color={ocrColors[invoice.ocr_status] || '#334155'}
                    />
                  </td>
                  <td>
                    <StatusBadge
                      label={invoice.validation_status}
                      color={validationColors[invoice.validation_status] || '#334155'}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </Card>
  );
}
