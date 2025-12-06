import { useMemo, useState } from 'react';
import type { InvoiceCreate, TipoDocumento, TipoIdentificacion, TipoOperacion } from '../api/types';
import { Card } from './Card';

type SubmitStatus = 'idle' | 'saving' | 'success' | 'error';

interface InvoiceFormProps {
  onSubmit: (payload: InvoiceCreate) => Promise<void>;
}

const tipoOperacionOptions: { label: string; value: TipoOperacion }[] = [
  { label: 'Compra 606', value: 'COMPRA_606' },
  { label: 'Venta 607', value: 'VENTA_607' },
];

const tipoDocumentoOptions: { label: string; value: TipoDocumento }[] = [
  { label: 'Factura', value: 'FACTURA' },
  { label: 'Nota de crédito', value: 'NOTA_CREDITO' },
  { label: 'Nota de débito', value: 'NOTA_DEBITO' },
  { label: 'Otro', value: 'OTRO' },
];

const tipoIdentificacionOptions: { label: string; value: TipoIdentificacion }[] = [
  { label: 'RNC', value: 'RNC' },
  { label: 'Cédula', value: 'CEDULA' },
  { label: 'Pasaporte', value: 'PASAPORTE' },
  { label: 'ID Tributaria', value: 'ID_TRIBUTARIA' },
];

function todayISO(): string {
  return new Date().toISOString().slice(0, 10);
}

export function InvoiceForm({ onSubmit }: InvoiceFormProps) {
  const initialForm = useMemo<InvoiceCreate>(
    () => ({
      tipo_operacion: 'VENTA_607',
      tipo_documento: 'FACTURA',
      rnc_emisor: '',
      nombre_emisor: '',
      rnc_receptor: '',
      nombre_receptor: '',
      tipo_identificacion_receptor: 'RNC',
      ncf: '',
      ncf_modificado: '',
      fecha_comprobante: todayISO(),
      fecha_pago_retencion: '',
      moneda: 'DOP',
      tasa_cambio: 1,
      comentarios: '',
      totals: {
        monto_facturado: 0,
        itbis_facturado: 0,
      },
      pagos: {
        monto_efectivo: 0,
        monto_tarjeta: 0,
        monto_venta_credito: 0,
      },
    }),
    [],
  );

  const [form, setForm] = useState<InvoiceCreate>(initialForm);
  const [status, setStatus] = useState<SubmitStatus>('idle');
  const [error, setError] = useState<string | null>(null);

  const updateField = (key: keyof InvoiceCreate, value: unknown) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const updateTotals = (key: keyof NonNullable<InvoiceCreate['totals']>, value: number) => {
    setForm((prev) => ({
      ...prev,
      totals: {
        ...prev.totals,
        [key]: Number.isNaN(value) ? 0 : value,
      },
    }));
  };

  const updatePagos = (key: keyof NonNullable<InvoiceCreate['pagos']>, value: number) => {
    setForm((prev) => ({
      ...prev,
      pagos: {
        ...prev.pagos,
        [key]: Number.isNaN(value) ? 0 : value,
      },
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setStatus('saving');
    setError(null);
    try {
      await onSubmit(form);
      setStatus('success');
      setForm(initialForm);
    } catch (err) {
      setStatus('error');
      setError(err instanceof Error ? err.message : 'No se pudo guardar la factura');
    }
  };

  return (
    <Card
      title="Registrar factura"
      description="Envía la factura al backend con los campos mínimos."
      action={
        <span style={{ color: '#475569', fontWeight: 600, fontSize: 13 }}>
          Origen: Web · {form.moneda}
        </span>
      }
    >
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
        <div className="form-row">
          <div>
            <label>Tipo de operación</label>
            <select
              value={form.tipo_operacion}
              onChange={(e) => updateField('tipo_operacion', e.target.value as TipoOperacion)}
              required
            >
              {tipoOperacionOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>Tipo de documento</label>
            <select
              value={form.tipo_documento}
              onChange={(e) => updateField('tipo_documento', e.target.value as TipoDocumento)}
              required
            >
              {tipoDocumentoOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>Moneda</label>
            <input
              value={form.moneda}
              maxLength={3}
              onChange={(e) => updateField('moneda', e.target.value.toUpperCase())}
              required
            />
            <p className="helper">ISO 4217, ej: DOP o USD.</p>
          </div>
          <div>
            <label>Tasa de cambio</label>
            <input
              type="number"
              min="0"
              step="0.01"
              value={form.tasa_cambio}
              onChange={(e) => updateField('tasa_cambio', parseFloat(e.target.value))}
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div>
            <label>RNC/Cédula emisor</label>
            <input
              value={form.rnc_emisor}
              onChange={(e) => updateField('rnc_emisor', e.target.value)}
              required
            />
          </div>
          <div>
            <label>Nombre emisor</label>
            <input value={form.nombre_emisor} onChange={(e) => updateField('nombre_emisor', e.target.value)} />
          </div>
          <div>
            <label>RNC/Cédula receptor</label>
            <input value={form.rnc_receptor} onChange={(e) => updateField('rnc_receptor', e.target.value)} />
          </div>
          <div>
            <label>Nombre receptor</label>
            <input value={form.nombre_receptor} onChange={(e) => updateField('nombre_receptor', e.target.value)} />
          </div>
          <div>
            <label>Tipo identificación receptor</label>
            <select
              value={form.tipo_identificacion_receptor}
              onChange={(e) => updateField('tipo_identificacion_receptor', e.target.value as TipoIdentificacion)}
            >
              {tipoIdentificacionOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-row">
          <div>
            <label>NCF</label>
            <input value={form.ncf} onChange={(e) => updateField('ncf', e.target.value)} required />
          </div>
          <div>
            <label>NCF modificado (opcional)</label>
            <input value={form.ncf_modificado} onChange={(e) => updateField('ncf_modificado', e.target.value)} />
          </div>
          <div>
            <label>Fecha comprobante</label>
            <input
              type="date"
              value={form.fecha_comprobante}
              onChange={(e) => updateField('fecha_comprobante', e.target.value)}
              required
            />
          </div>
          <div>
            <label>Fecha pago/retención</label>
            <input
              type="date"
              value={form.fecha_pago_retencion}
              onChange={(e) => updateField('fecha_pago_retencion', e.target.value)}
            />
          </div>
        </div>

        <div className="form-row">
          <div>
            <label>Monto facturado</label>
            <input
              type="number"
              min="0"
              step="0.01"
              value={form.totals?.monto_facturado ?? 0}
              onChange={(e) => updateTotals('monto_facturado', parseFloat(e.target.value))}
            />
          </div>
          <div>
            <label>ITBIS facturado</label>
            <input
              type="number"
              min="0"
              step="0.01"
              value={form.totals?.itbis_facturado ?? 0}
              onChange={(e) => updateTotals('itbis_facturado', parseFloat(e.target.value))}
            />
          </div>
          <div>
            <label>Pago en efectivo</label>
            <input
              type="number"
              min="0"
              step="0.01"
              value={form.pagos?.monto_efectivo ?? 0}
              onChange={(e) => updatePagos('monto_efectivo', parseFloat(e.target.value))}
            />
          </div>
          <div>
            <label>Pago con tarjeta</label>
            <input
              type="number"
              min="0"
              step="0.01"
              value={form.pagos?.monto_tarjeta ?? 0}
              onChange={(e) => updatePagos('monto_tarjeta', parseFloat(e.target.value))}
            />
          </div>
          <div>
            <label>Venta a crédito</label>
            <input
              type="number"
              min="0"
              step="0.01"
              value={form.pagos?.monto_venta_credito ?? 0}
              onChange={(e) => updatePagos('monto_venta_credito', parseFloat(e.target.value))}
            />
          </div>
        </div>

        <div>
          <label>Comentarios</label>
          <textarea
            rows={3}
            value={form.comentarios}
            placeholder="Notas internas, estatus de OCR, etc."
            onChange={(e) => updateField('comentarios', e.target.value)}
          />
        </div>

        <button className="button" type="submit" disabled={status === 'saving'}>
          {status === 'saving' ? 'Guardando...' : 'Guardar factura'}
        </button>

        {status === 'success' && <div className="toast success">Factura enviada correctamente.</div>}
        {status === 'error' && error && <div className="toast error">{error}</div>}
      </form>
    </Card>
  );
}
