import * as React from 'react';
import { ContentWrapper } from '@/components/common/PageHeader';
import { PageHeader, SectionHeader } from '@/components/common/PageHeader';
import { SectionCard } from '@/components/common/MetricCard';
import { EmptyState } from '@/components/common/EmptyState';
import { ClientService } from '@/services/client.service';
import { History, Users, Layers, Award, AlertTriangle, ArrowRight } from 'lucide-react';
import type { Client } from '@/types';

export function HistoricalClientsPage() {
  const [clients, setClients] = React.useState<Client[]>([]);
  const [selectedClientId, setSelectedClientId] = React.useState<string>('');
  const [matches, setMatches] = React.useState<any[]>([]);
  const [loadingClients, setLoadingClients] = React.useState(false);
  const [loadingHistory, setLoadingHistory] = React.useState(false);

  // Load clients list for dropdown
  React.useEffect(() => {
    setLoadingClients(true);
    ClientService.getClients({ page: 1, pageSize: 100 })
      .then((res) => {
        setClients(res.data || []);
        if (res.data?.length > 0) {
          // Auto-select first client
          setSelectedClientId(res.data[0].id);
        }
      })
      .catch((err) => console.error("Failed to load clients:", err))
      .finally(() => setLoadingClients(false));
  }, []);

  // Load similarity matches when client selection changes
  React.useEffect(() => {
    if (!selectedClientId) {
      setMatches([]);
      return;
    }
    setLoadingHistory(true);
    ClientService.getHistory(selectedClientId)
      .then((res) => {
        setMatches(res.data || []);
      })
      .catch((err) => {
        console.error("Failed to load history matches:", err);
        setMatches([]);
      })
      .finally(() => setLoadingHistory(false));
  }, [selectedClientId]);

  return (
    <ContentWrapper>
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <PageHeader
          title="Historical Similarity Match"
          description="View past client outcomes and lessons learned matching current client profiles."
        />
        
        {/* Client Select Dropdown */}
        <div className="flex items-center gap-2 bg-card border px-3 py-1.5 rounded-xl shadow-sm self-start sm:self-auto">
          <span className="text-xs text-muted-foreground font-medium">Select Context:</span>
          <select 
            value={selectedClientId} 
            onChange={(e) => setSelectedClientId(e.target.value)}
            disabled={loadingClients}
            className="bg-transparent text-sm font-bold text-foreground focus:outline-none cursor-pointer"
          >
            {loadingClients ? (
              <option>Loading accounts...</option>
            ) : clients.length === 0 ? (
              <option value="">No clients available</option>
            ) : (
              clients.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))
            )}
          </select>
        </div>
      </div>

      {loadingHistory ? (
        <div className="section-card p-12 flex flex-col items-center justify-center min-h-[300px] border border-border mt-6">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent mb-4" />
          <p className="text-sm text-muted-foreground">Running semantic similarity search in Supabase vector space...</p>
        </div>
      ) : matches.length === 0 ? (
        <div className="mt-6">
          <EmptyState
            icon={History}
            title="No historical similarity generated yet"
            description="Run AI Analysis or select another client to build the similarity embedding context."
            className="py-16 border border-dashed rounded-2xl"
          />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
          {matches.map((match) => (
            <SectionCard key={match.id} className="hover:shadow-md transition duration-200">
              <div className="flex items-start justify-between border-b border-border/60 pb-3">
                <div>
                  <h4 className="font-bold text-foreground text-[15px]">{match.name}</h4>
                  <span className="text-[11px] text-muted-foreground mt-0.5 block">{match.industry}</span>
                </div>
                <span className="text-xs font-extrabold bg-primary/10 text-primary px-2.5 py-1 rounded-lg">
                  {match.similarityScore}% Match
                </span>
              </div>

              <div className="mt-4 space-y-4">
                <div className="flex items-center justify-between bg-secondary/10 px-3 py-1.5 rounded-lg border border-border/30">
                  <span className="text-xs text-muted-foreground flex items-center gap-1.5">
                    <Users className="h-3.5 w-3.5" /> Retention Outcome
                  </span>
                  <span className={`text-xs font-bold uppercase tracking-wider ${
                    match.outcome === 'churned' ? 'text-danger bg-danger/10' :
                    match.outcome === 'retained' ? 'text-success bg-success/10' : 'text-primary bg-primary/10'
                  } px-2 py-0.5 rounded`}>
                    {match.outcome}
                  </span>
                </div>

                <div className="space-y-1.5">
                  <span className="text-xs font-bold text-foreground flex items-center gap-1.5">
                    <AlertTriangle className="h-3.5 w-3.5 text-warning" /> Churn Reason / Context
                  </span>
                  <p className="text-xs text-muted-foreground leading-relaxed pl-5">
                    {match.reasonForChurn || "Early indicators flagged contract renewal fatigue. Customer churned due to champion exit."}
                  </p>
                </div>

                <div className="space-y-1.5 border-t pt-3">
                  <span className="text-xs font-bold text-foreground flex items-center gap-1.5">
                    <Award className="h-3.5 w-3.5 text-success" /> Playbook Lessons Learned
                  </span>
                  <p className="text-xs text-muted-foreground leading-relaxed pl-5 italic">
                    {match.lessonsLearned || "Ensure multi-threading across key leadership stakeholders rather than relying on a single sponsor."}
                  </p>
                </div>
              </div>
            </SectionCard>
          ))}
        </div>
      )}
    </ContentWrapper>
  );
}

export default HistoricalClientsPage;
