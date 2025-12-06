import { useMemo, useState } from 'react';

import { uploadInvoiceWithFile } from '../api/client';
import type { InvoiceCreate, TipoOperacion } from '../api/types';
import { Card } from './Card';

type SubmitStatus = 'idle' | 'saving' | 'success' | 'error';

interface InvoiceUploadCardProps {
  onUploaded: () => Promise<void> | void;
}

const operationOptions: { label: string; value: TipoOperacion }[] = [
  { label: 'Compra 606', value: 'COMPRA_606' },
  { label: 'Venta 607', value: 'VENTA_607' },
];

function todayISO(): string {
  return new Date().toISOString().slice(0, 10);
}

export function InvoiceUploadCard({ onUploaded }: InvoiceUploadCardProps) {
  const baseMetadata = useMemo<InvoiceCreate>(
    () => ({
      tipo_operacion: 'COMPRA_606',
      tipo_documento: 'FACTURA',
      rnc_emisor: '',
      ncf: '',
      fecha_comprobante: todayISO(),
      moneda: 'DOP',
      tasa_cambio: 1,
      comentarios: 'Cargado vía upload web',
    }),
    [],
  );

  const [metadata, setMetadata] = useState<InvoiceCreate>(baseMetadata);
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<SubmitStatus>('idle');
  const [error, setError] = useState<string | null>(null);

  const updateMetadata = (key: keyof InvoiceCreate, value: unknown) => {
    setMetadata((prev) => ({ ...prev, [key]: value }));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) {
      setError('Selecciona un PDF o imagen para continuar.');
      setStatus('error');
      return;
    }

    setStatus('saving');
    setError(null);
    try {
      await uploadInvoiceWithFile(metadata, file);
      await onUploaded();
      setStatus('success');
      setMetadata(baseMetadata);
      setFile(null);
    } catch (err) {
      setStatus('error');
      setError(err instanceof Error ? err.message : 'No se pudo subir la factura');
    }
  };

  return (
    <Card
      title="Subir factura con archivo"
      description="Envía un PDF o imagen para centralizar tus comprobantes 606/607."
      action={<span className="badge muted">Adjunta el archivo y los metadatos mínimos.</span>}
    >
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        <div className="form-row">
          <div>
            <label>Tipo de operación</label>
            <select
              value={metadata.tipo_operacion}
              onChange={(e) => updateMetadata('tipo_operacion', e.target.value as TipoOperacion)}
              required
            >
              {operationOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <p className="helper">Define si es compra (606) o venta (607).</p>
          </div>
          <div>
            <label>NCF</label>
            <input
              value={metadata.ncf}
              onChange={(e) => updateMetadata('ncf', e.target.value)}
              placeholder="E3100000001"
              required
            />
          </div>
          <div>
            <label>RNC/Cédula emisor</label>
            <input
              value={metadata.rnc_emisor}
              onChange={(e) => updateMetadata('rnc_emisor', e.target.value)}
              placeholder="130000000"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div>
            <label>Fecha del comprobante</label>
            <input
              type="date"
              value={metadata.fecha_comprobante}
              onChange={(e) => updateMetadata('fecha_comprobante', e.target.value)}
              required
            />
          </div>
          <div>
            <label>Moneda</label>
            <input
              value={metadata.moneda}
              maxLength={3}
              onChange={(e) => updateMetadata('moneda', e.target.value.toUpperCase())}
              required
            />
          </div>
          <div>
            <label>Tasa de cambio</label>
            <input
              type="number"
              min="0"
              step="0.01"
              value={metadata.tasa_cambio}
              onChange={(e) => updateMetadata('tasa_cambio', parseFloat(e.target.value))}
              required
            />
          </div>
        </div>

        <div>
          <label>Archivo de la factura</label>
          <input
            type="file"
            accept="application/pdf,image/*"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            required
          />
          <p className="helper">PDF, JPG o PNG. Se guardará en la carpeta local de uploads.</p>
        </div>

        <button className="button" type="submit" disabled={status === 'saving'}>
          {status === 'saving' ? 'Subiendo...' : 'Subir factura'}
        </button>
        {status === 'success' && <div className="toast success">Factura subida correctamente.</div>}
        {status === 'error' && error && <div className="toast error">{error}</div>}
      </form>
    </Card>
  );
}
