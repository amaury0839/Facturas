import type { HealthResponse, InvoiceCreate, InvoiceRead, TipoOperacion } from './types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const detail = (body as { detail?: string }).detail || response.statusText;
    throw new Error(detail || 'Error de red');
  }
  return response.json();
}

export async function fetchInvoices(): Promise<InvoiceRead[]> {
  const res = await fetch(`${API_BASE_URL}/invoices`);
  return handleResponse<InvoiceRead[]>(res);
}

export async function createInvoice(payload: InvoiceCreate): Promise<InvoiceRead> {
  const res = await fetch(`${API_BASE_URL}/invoices`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  return handleResponse<InvoiceRead>(res);
}

export async function uploadInvoiceWithFile(
  payload: InvoiceCreate,
  file: File,
): Promise<InvoiceRead> {
  const formData = new FormData();
  formData.append('metadata', JSON.stringify(payload));
  formData.append('file', file);

  const res = await fetch(`${API_BASE_URL}/invoices/upload`, {
    method: 'POST',
    body: formData,
  });
  return handleResponse<InvoiceRead>(res);
}

export async function exportInvoices(tipo_operacion?: TipoOperacion): Promise<Blob> {
  const url = new URL(`${API_BASE_URL}/invoices/export`);
  if (tipo_operacion) {
    url.searchParams.set('tipo_operacion', tipo_operacion);
  }
  const res = await fetch(url.toString());
  if (!res.ok) {
    throw new Error('No se pudo generar el Excel');
  }
  return res.blob();
}

export async function fetchHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE_URL}/health`);
  return handleResponse<HealthResponse>(res);
}
