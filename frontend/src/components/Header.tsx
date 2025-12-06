export function Header() {
  return (
    <header
      style={{
        padding: '18px 0 10px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: 12,
      }}
    >
      <div>
        <p style={{ margin: 0, color: '#6366f1', fontWeight: 700, letterSpacing: 0.5 }}>
          Facturación DGII 606/607
        </p>
        <h1 style={{ margin: '6px 0 0', fontSize: 28, color: '#0f172a' }}>
          Panel de Facturas
        </h1>
        <p style={{ margin: '6px 0 0', color: '#475569' }}>
          Carga y validación rápida de comprobantes fiscales.
        </p>
      </div>
      <div
        style={{
          background: '#eef2ff',
          color: '#4338ca',
          fontWeight: 700,
          padding: '10px 14px',
          borderRadius: 12,
          fontSize: 13,
        }}
      >
        React + Vite
      </div>
    </header>
  );
}
