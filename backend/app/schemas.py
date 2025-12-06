from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from .models.invoice import (
    OrigenFactura,
    TipoDocumento,
    TipoIdentificacion,
    TipoOperacion,
)


class InvoiceTotalsCreate(BaseModel):
    tipo_bien_servicio_comprado: Optional[int] = None
    monto_facturado_servicios: Optional[float] = None
    monto_facturado_bienes: Optional[float] = None
    monto_facturado: Optional[float] = None
    itbis_facturado: Optional[float] = None
    itbis_retenido: Optional[float] = None
    impuesto_selectivo: Optional[float] = None
    monto_propina_legal: Optional[float] = None
    tipo_ingreso: Optional[int] = None
    retencion_renta_por_terceros: Optional[float] = None
    monto_percibido_itbis: Optional[float] = None


class PaymentBreakdownCreate(BaseModel):
    monto_efectivo: Optional[float] = 0
    monto_cheque_transferencia_deposito: Optional[float] = 0
    monto_tarjeta: Optional[float] = 0
    monto_venta_credito: Optional[float] = 0
    monto_bonos_certificados_regalo: Optional[float] = 0
    monto_permuta: Optional[float] = 0
    monto_otras_formas_venta: Optional[float] = 0


class InvoiceCreate(BaseModel):
    tipo_operacion: TipoOperacion = Field(description="COMPRA_606 o VENTA_607")
    tipo_documento: TipoDocumento
    rnc_emisor: str
    nombre_emisor: Optional[str] = None
    rnc_receptor: Optional[str] = None
    nombre_receptor: Optional[str] = None
    tipo_identificacion_receptor: Optional[TipoIdentificacion] = None
    ncf: str
    ncf_modificado: Optional[str] = None
    fecha_comprobante: date
    fecha_pago_retencion: Optional[date] = None
    moneda: str = "DOP"
    tasa_cambio: float = 1.0
    origen: OrigenFactura = OrigenFactura.WEB
    comentarios: Optional[str] = None
    totals: Optional[InvoiceTotalsCreate] = None
    pagos: Optional[PaymentBreakdownCreate] = None


class InvoiceTotalsRead(BaseModel):
    tipo_bien_servicio_comprado: Optional[int] = None
    monto_facturado_servicios: Optional[float] = None
    monto_facturado_bienes: Optional[float] = None
    monto_facturado: Optional[float] = None
    itbis_facturado: Optional[float] = None
    itbis_retenido: Optional[float] = None
    impuesto_selectivo: Optional[float] = None
    monto_propina_legal: Optional[float] = None
    tipo_ingreso: Optional[int] = None
    retencion_renta_por_terceros: Optional[float] = None
    monto_percibido_itbis: Optional[float] = None

    class Config:
        orm_mode = True


class PaymentBreakdownRead(BaseModel):
    monto_efectivo: Optional[float] = 0
    monto_cheque_transferencia_deposito: Optional[float] = 0
    monto_tarjeta: Optional[float] = 0
    monto_venta_credito: Optional[float] = 0
    monto_bonos_certificados_regalo: Optional[float] = 0
    monto_permuta: Optional[float] = 0
    monto_otras_formas_venta: Optional[float] = 0

    class Config:
        orm_mode = True


class InvoiceRead(BaseModel):
    id: int
    tipo_operacion: TipoOperacion
    tipo_documento: TipoDocumento
    rnc_emisor: str
    nombre_emisor: Optional[str] = None
    rnc_receptor: Optional[str] = None
    nombre_receptor: Optional[str] = None
    tipo_identificacion_receptor: Optional[TipoIdentificacion] = None
    ncf: str
    ncf_modificado: Optional[str] = None
    fecha_comprobante: date
    fecha_pago_retencion: Optional[date] = None
    moneda: str
    tasa_cambio: float
    origen: OrigenFactura
    comentarios: Optional[str] = None
    totals: Optional[InvoiceTotalsRead] = None
    pagos: Optional[PaymentBreakdownRead] = Field(default=None, alias="payments")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
