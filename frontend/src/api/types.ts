export type TipoOperacion = 'COMPRA_606' | 'VENTA_607';
export type TipoDocumento = 'FACTURA' | 'NOTA_CREDITO' | 'NOTA_DEBITO' | 'OTRO';
export type TipoIdentificacion = 'RNC' | 'CEDULA' | 'PASAPORTE' | 'ID_TRIBUTARIA';
export type OrigenFactura = 'WEB' | 'TELEGRAM' | 'API';
export type ValidationStatus = 'PENDIENTE' | 'OBSERVADO' | 'VALIDADO';
export type OcrStatus = 'PENDIENTE' | 'PROCESADO' | 'ERROR';

export interface InvoiceTotalsCreate {
  tipo_bien_servicio_comprado?: number | null;
  monto_facturado_servicios?: number | null;
  monto_facturado_bienes?: number | null;
  monto_facturado?: number | null;
  itbis_facturado?: number | null;
  itbis_retenido?: number | null;
  impuesto_selectivo?: number | null;
  monto_propina_legal?: number | null;
  tipo_ingreso?: number | null;
  retencion_renta_por_terceros?: number | null;
  monto_percibido_itbis?: number | null;
}

export interface PaymentBreakdownCreate {
  monto_efectivo?: number;
  monto_cheque_transferencia_deposito?: number;
  monto_tarjeta?: number;
  monto_venta_credito?: number;
  monto_bonos_certificados_regalo?: number;
  monto_permuta?: number;
  monto_otras_formas_venta?: number;
}

export interface InvoiceCreate {
  tipo_operacion: TipoOperacion;
  tipo_documento: TipoDocumento;
  rnc_emisor: string;
  nombre_emisor?: string;
  rnc_receptor?: string;
  nombre_receptor?: string;
  tipo_identificacion_receptor?: TipoIdentificacion;
  ncf: string;
  ncf_modificado?: string;
  fecha_comprobante: string;
  fecha_pago_retencion?: string;
  moneda: string;
  tasa_cambio: number;
  origen?: OrigenFactura;
  comentarios?: string;
  file_url?: string;
  file_mime?: string;
  file_size?: number;
  totals?: InvoiceTotalsCreate | null;
  pagos?: PaymentBreakdownCreate | null;
}

export interface InvoiceTotalsRead extends InvoiceTotalsCreate {}

export interface PaymentBreakdownRead extends PaymentBreakdownCreate {}

export interface InvoiceRead {
  id: number;
  tipo_operacion: TipoOperacion;
  tipo_documento: TipoDocumento;
  rnc_emisor: string;
  nombre_emisor?: string;
  rnc_receptor?: string;
  nombre_receptor?: string;
  tipo_identificacion_receptor?: TipoIdentificacion;
  ncf: string;
  ncf_modificado?: string;
  fecha_comprobante: string;
  fecha_pago_retencion?: string;
  moneda: string;
  tasa_cambio: number;
  origen: OrigenFactura;
  ocr_status: OcrStatus;
  validation_status: ValidationStatus;
  comentarios?: string;
  file_url?: string;
  file_mime?: string;
  file_size?: number;
  created_at: string;
  updated_at: string;
  totals?: InvoiceTotalsRead | null;
  payments?: PaymentBreakdownRead | null;
}

export interface InvoiceUploadPayload extends InvoiceCreate {
  file: File;
}

export interface HealthResponse {
  status: string;
  message?: string;
  invoice_count?: number;
}
