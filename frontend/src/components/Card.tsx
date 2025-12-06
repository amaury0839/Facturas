import type { PropsWithChildren, ReactNode } from 'react';

interface CardProps extends PropsWithChildren {
  title?: string;
  description?: string;
  action?: ReactNode;
}

export function Card({ title, description, action, children }: CardProps) {
  return (
    <section
      style={{
        backgroundColor: '#fff',
        borderRadius: 16,
        padding: 18,
        boxShadow: '0 20px 60px rgba(15, 23, 42, 0.08)',
        border: '1px solid #e2e8f0',
      }}
    >
      {(title || description || action) && (
        <header
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: 12,
            gap: 10,
          }}
        >
          <div>
            {title && (
              <h2
                style={{
                  margin: '0 0 4px 0',
                  fontSize: 18,
                  color: '#0f172a',
                  fontWeight: 700,
                }}
              >
                {title}
              </h2>
            )}
            {description && (
              <p style={{ margin: 0, color: '#475569', fontSize: 14 }}>{description}</p>
            )}
          </div>
          {action && <div>{action}</div>}
        </header>
      )}
      {children}
    </section>
  );
}
