import { useState } from 'react';

import { exportInvoices } from '../api/client';
import type { TipoOperacion } from '../api/types';
import { Card } from './Card';

const options: { label: string; value?: TipoOperacion }[] = [
  { label: 'Todo (606 y 607)', value: undefined },
  { label: 'Solo compras 606', value: 'COMPRA_606' },
  { label: 'Solo ventas 607', value: 'VENTA_607' },
];

export function ExportPanel() {
  const [selected, setSelected] = useState<TipoOperacion | undefined>(undefined);
  const [status, setStatus] = useState<'idle' | 'downloading' | 'error'>('idle');
  const [error, setError] = useState<string | null>(null);

  const handleExport = async () => {
    setStatus('downloading');
    setError(null);
    try {
      const blob = await exportInvoices(selected);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      const suffix = selected ? selected.toLowerCase() : '606-607';
      a.href = url;
      a.download = `facturas-${suffix}.xlsx`;
      a.click();
      window.URL.revokeObjectURL(url);
      setStatus('idle');
    } catch (err) {
      setStatus('error');
      setError(err instanceof Error ? err.message : 'No se pudo descargar el Excel');
    }
  };

  return (
    <Card
      title="Exportar a Excel"
      description="Genera un archivo .xlsx con las facturas cargadas en el backend."
      action={<span className="badge muted">Listo para DGII 606/607</span>}
    >
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <div>
          <label>Alcance de la exportación</label>
          <select
            value={selected || ''}
            onChange={(e) => {
              const value = e.target.value as TipoOperacion;
              setSelected(value || undefined);
            }}
          >
            {options.map((option) => (
              <option key={option.label} value={option.value || ''}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <button className="button" type="button" onClick={handleExport} disabled={status === 'downloading'}>
          {status === 'downloading' ? 'Generando...' : 'Descargar Excel'}
        </button>
        {status === 'error' && error && <div className="toast error">{error}</div>}
      </div>
    </Card>
  );
}
