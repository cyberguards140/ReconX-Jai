
import { MetricWidget } from '@/widgets/MetricWidget';
import { ShieldAlert, AlertTriangle, CheckCircle, Clock } from 'lucide-react';

export function SOCDashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">SOC Operations Center</h2>
        <p className="text-muted-foreground mt-2">Real-time incident response and analyst workloads.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <MetricWidget 
          title="Open Incidents" 
          value={24} 
          icon={<ShieldAlert className="w-4 h-4 text-destructive" />}
          trend={{ value: 5, isPositive: false }}
        />
        <MetricWidget 
          title="Critical Alerts" 
          value={7} 
          icon={<AlertTriangle className="w-4 h-4 text-orange-500" />}
        />
        <MetricWidget 
          title="Resolved Today" 
          value={42} 
          icon={<CheckCircle className="w-4 h-4 text-green-500" />}
        />
        <MetricWidget 
          title="MTTR" 
          value="2h 15m" 
          icon={<Clock className="w-4 h-4 text-primary" />}
        />
      </div>
    </div>
  );
}
