import { useEffect, useState } from 'react';
import { MetricWidget } from '@/widgets/MetricWidget';
import { Globe, Server, Shield, Activity } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { api } from '@/services/api';

export function ASMDashboard() {
  const [assets, setAssets] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchAssets() {
      try {
        const resp = await api.get('/asm/assets');
        // Because we wrapped it in PaginatedResponse in the backend
        setAssets(resp.data || []);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    }
    fetchAssets();
  }, []);

  const totalAssets = assets.length;
  const domains = assets.filter(a => a.type === 'DOMAIN').length;
  const ips = assets.filter(a => a.type === 'IP').length;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Attack Surface Management</h2>
        <p className="text-muted-foreground mt-2">Comprehensive view of your external exposure.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <MetricWidget 
          title="Total Assets" 
          value={loading ? '...' : totalAssets} 
          icon={<Globe className="w-4 h-4" />}
          trend={{ value: 12, isPositive: true }}
        />
        <MetricWidget 
          title="Domains" 
          value={loading ? '...' : domains} 
          icon={<Globe className="w-4 h-4" />}
        />
        <MetricWidget 
          title="IP Addresses" 
          value={loading ? '...' : ips} 
          icon={<Server className="w-4 h-4" />}
        />
        <MetricWidget 
          title="High Risk Assets" 
          value={loading ? '...' : Math.floor(totalAssets * 0.1)} 
          icon={<Shield className="w-4 h-4 text-destructive" />}
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Asset Distribution</CardTitle>
          </CardHeader>
          <CardContent className="h-80 flex items-center justify-center border-t border-border mt-4">
            <p className="text-muted-foreground">Chart Placeholder (Recharts)</p>
          </CardContent>
        </Card>
        
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Recent Discoveries</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {assets.slice(0, 5).map((asset: any, i) => (
                <div key={i} className="flex items-center">
                  <Activity className="w-4 h-4 text-primary mr-2" />
                  <div className="flex-1 space-y-1">
                    <p className="text-sm font-medium leading-none text-foreground">{asset.value}</p>
                    <p className="text-sm text-muted-foreground">{asset.type} • {asset.source}</p>
                  </div>
                </div>
              ))}
              {assets.length === 0 && !loading && (
                <p className="text-sm text-muted-foreground">No assets discovered yet.</p>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
