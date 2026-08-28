import * as React from 'react';
import { useQuery } from '@tanstack/react-query';
import { workflowService } from '@/services/workflow.service';
import { useWorkflowMonitor } from '@/hooks/useWorkflowMonitor';
import { Terminal, Info, CheckCircle2, AlertTriangle, XCircle, Copy, Trash2, Search } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { cn } from '@/utils';
import { toast } from 'sonner';

export function WorkflowExecutionLogs() {
  const { activeExecution } = useWorkflowMonitor();
  const [filter, setFilter] = React.useState<string>('all');
  const [searchTerm, setSearchTerm] = React.useState('');

  const { data: logs = [], isLoading } = useQuery({
    queryKey: ['workflow', 'logs', activeExecution?.id],
    queryFn: () => workflowService.getExecutionLogs(activeExecution!.id).then(r => r.data),
    enabled: !!activeExecution?.id,
  });

  const filteredLogs = logs.filter(log => {
    if (filter !== 'all' && log.severity !== filter) return false;
    if (searchTerm && !log.message.toLowerCase().includes(searchTerm.toLowerCase()) && !log.nodeName.toLowerCase().includes(searchTerm.toLowerCase())) return false;
    return true;
  });

  const copyLogs = () => {
    const text = filteredLogs.map(l => `[${new Date(l.startedAt).toLocaleTimeString()}] [${l.severity.toUpperCase()}] [${l.nodeName}] ${l.message}`).join('\n');
    navigator.clipboard.writeText(text);
    toast.success('Logs copied to clipboard');
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'info': return <Info className="h-4 w-4 text-info" />;
      case 'success': return <CheckCircle2 className="h-4 w-4 text-success" />;
      case 'warning': return <AlertTriangle className="h-4 w-4 text-warning" />;
      case 'error': return <XCircle className="h-4 w-4 text-destructive" />;
      default: return <Terminal className="h-4 w-4 text-muted-foreground" />;
    }
  };

  if (!activeExecution) return null;

  return (
    <div className="section-card flex flex-col h-[500px]">
      {/* Log Header & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border pb-4 mb-4">
        <div className="flex items-center gap-2">
          <Terminal className="h-5 w-5 text-primary" />
          <h3 className="text-heading-4">Execution Logs</h3>
        </div>
        
        <div className="flex flex-wrap items-center gap-2">
          <div className="relative">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input 
              type="text"
              placeholder="Search logs..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="h-8 w-40 pl-8 pr-3 text-sm rounded-md border border-border bg-input focus:outline-none focus:ring-2 focus:ring-primary/20"
            />
          </div>
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="h-8 px-2 text-sm rounded-md border border-border bg-input focus:outline-none focus:ring-2 focus:ring-primary/20"
          >
            <option value="all">All Levels</option>
            <option value="info">Info</option>
            <option value="success">Success</option>
            <option value="warning">Warning</option>
            <option value="error">Error</option>
          </select>
          <Button variant="outline" size="sm" onClick={copyLogs} title="Copy Logs">
            <Copy className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="sm" title="Clear Logs">
            <Trash2 className="h-4 w-4 text-destructive" />
          </Button>
        </div>
      </div>

      {/* Log Viewer */}
      <div className="flex-1 overflow-y-auto bg-foreground rounded-xl p-4 custom-scrollbar font-mono text-sm">
        {isLoading ? (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            Loading logs...
          </div>
        ) : filteredLogs.length === 0 ? (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            No logs found matching criteria
          </div>
        ) : (
          <div className="space-y-2">
            {filteredLogs.map((log) => (
              <div key={log.id} className="flex items-start gap-3 py-1 group hover:bg-white/5 rounded px-2 -mx-2 transition-colors">
                <span className="text-muted-foreground w-20 flex-shrink-0">
                  {new Date(log.startedAt).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute:'2-digit', second:'2-digit' })}
                </span>
                <div className="mt-0.5 flex-shrink-0">
                  {getSeverityIcon(log.severity)}
                </div>
                <div className="flex-1 break-words">
                  <span className={cn(
                    "font-semibold mr-2",
                    log.severity === 'info' && "text-info",
                    log.severity === 'success' && "text-success",
                    log.severity === 'warning' && "text-warning",
                    log.severity === 'error' && "text-destructive"
                  )}>
                    [{log.nodeName}]
                  </span>
                  <span className="text-background/90">{log.message}</span>
                  {log.duration && (
                    <span className="text-muted-foreground ml-2">({log.duration}s)</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
