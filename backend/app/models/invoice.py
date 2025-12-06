from datetime import date, datetime
from enum import Enum
from typing import Optional

from sqlmodel import Column, DateTime, Enum as SqlEnum, Field, Relationship, SQLModel


class TipoOperacion(str, Enum):
    COMPRA_606 = "COMPRA_606"
    VENTA_607 = "VENTA_607"


class TipoDocumento(str, Enum):
    FACTURA = "FACTURA"
    NOTA_CREDITO = "NOTA_CREDITO"
    NOTA_DEBITO = "NOTA_DEBITO"
    OTRO = "OTRO"


class TipoIdentificacion(str, Enum):
    RNC = "RNC"
    CEDULA = "CEDULA"
    PASAPORTE = "PASAPORTE"
    ID_TRIBUTARIA = "ID_TRIBUTARIA"


class OrigenFactura(str, Enum):
    WEB = "WEB"
    TELEGRAM = "TELEGRAM"
    API = "API"


class OcrStatus(str, Enum):
    PENDIENTE = "PENDIENTE"
    PROCESADO = "PROCESADO"
    ERROR = "ERROR"


class ValidationStatus(str, Enum):
    PENDIENTE = "PENDIENTE"
    OBSERVADO = "OBSERVADO"
    VALIDADO = "VALIDADO"


class ConfigCompany(SQLModel, table=True):
    __tablename__ = "config_company"

    id: Optional[int] = Field(default=None, primary_key=True)
    rnc: str
    razon_social: str
    maneja_606: bool = True
    maneja_607: bool = True
    telegram_bot_token: Optional[str] = None
    telegram_webhook_url: Optional[str] = None


class Invoice(SQLModel, table=True):
    __tablename__ = "invoices"

    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: Optional[int] = Field(default=None, foreign_key="config_company.id")
    tipo_operacion: TipoOperacion = Field(sa_column=Column(SqlEnum(TipoOperacion)))
    tipo_documento: TipoDocumento = Field(sa_column=Column(SqlEnum(TipoDocumento)))
    rnc_emisor: str
    nombre_emisor: Optional[str] = None
    rnc_receptor: Optional[str] = None
    nombre_receptor: Optional[str] = None
    tipo_identificacion_receptor: Optional[TipoIdentificacion] = Field(
        default=None, sa_column=Column(SqlEnum(TipoIdentificacion))
    )
    ncf: str
    ncf_modificado: Optional[str] = None
    fecha_comprobante: date
    fecha_pago_retencion: Optional[date] = None
    moneda: str = Field(default="DOP", max_length=3)
    tasa_cambio: float = 1.0
    origen: OrigenFactura = Field(sa_column=Column(SqlEnum(OrigenFactura)))
    ocr_status: OcrStatus = Field(default=OcrStatus.PENDIENTE, sa_column=Column(SqlEnum(OcrStatus)))
    validation_status: ValidationStatus = Field(
        default=ValidationStatus.PENDIENTE, sa_column=Column(SqlEnum(ValidationStatus))
    )
    comentarios: Optional[str] = None
    file_url: Optional[str] = None
    file_mime: Optional[str] = None
    file_size: Optional[int] = None
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )

    totals: Optional["InvoiceTotals"] = Relationship(back_populates="invoice")
    payments: Optional["PaymentBreakdown"] = Relationship(back_populates="invoice")


class InvoiceTotals(SQLModel, table=True):
    __tablename__ = "invoice_totals"

    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoices.id", index=True)
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

    invoice: Invoice = Relationship(back_populates="totals")


class PaymentBreakdown(SQLModel, table=True):
    __tablename__ = "payment_breakdown"

    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="invoices.id", index=True)
    monto_efectivo: Optional[float] = 0
    monto_cheque_transferencia_deposito: Optional[float] = 0
    monto_tarjeta: Optional[float] = 0
    monto_venta_credito: Optional[float] = 0
    monto_bonos_certificados_regalo: Optional[float] = 0
    monto_permuta: Optional[float] = 0
    monto_otras_formas_venta: Optional[float] = 0

    invoice: Invoice = Relationship(back_populates="payments")
