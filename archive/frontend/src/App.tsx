
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { EnterpriseLayout } from '@/layouts/EnterpriseLayout';
import { ASMDashboard } from '@/pages/asm/index';
import { SOCDashboard } from '@/pages/soc/index';
import { ThemeProvider } from '@/themes/ThemeProvider';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000,
    },
  },
});

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider defaultTheme="dark">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<EnterpriseLayout />}>
              <Route index element={<Navigate to="/asm" replace />} />
              <Route path="asm" element={<ASMDashboard />} />
              <Route path="soc" element={<SOCDashboard />} />
              <Route path="threat" element={<div className="p-6 text-foreground">Threat Intel Dashboard Placeholder</div>} />
              <Route path="cloud" element={<div className="p-6 text-foreground">Cloud Intel Dashboard Placeholder</div>} />
              <Route path="infra" element={<div className="p-6 text-foreground">Infrastructure Dashboard Placeholder</div>} />
              <Route path="executive" element={<div className="p-6 text-foreground">Executive Dashboard Placeholder</div>} />
            </Route>
          </Routes>
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
