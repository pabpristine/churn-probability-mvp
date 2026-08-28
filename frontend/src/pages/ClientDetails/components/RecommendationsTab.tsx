import * as React from 'react';
import { motion } from 'framer-motion';
import { Check, Lightbulb } from 'lucide-react';
import { SEED_RECOMMENDATIONS } from '../client-details.data';
import type { Recommendation } from '@/types';
import { cn } from '@/utils';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';

// ============================================================
// RecommendationsTab
// ============================================================

export function RecommendationsTab() {
  const [recs, setRecs] = React.useState<Recommendation[]>(SEED_RECOMMENDATIONS);

  const getPriorityColor = (priority: string) => {
    if (priority === 'critical') return 'text-destructive bg-destructive/10 border-destructive/20';
    if (priority === 'high') return 'text-destructive/80 bg-destructive/10 border-destructive/20';
    if (priority === 'medium') return 'text-warning bg-warning/10 border-warning/20';
    return 'text-info bg-info/10 border-info/20';
  };

  const toggleComplete = (id: string) => {
    setRecs((prev) =>
      prev.map((r) => (r.id === id ? { ...r, status: r.status === 'completed' ? 'pending' : 'completed' } : r))
    );
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="space-y-4"
    >
      <div className="flex items-center justify-between section-card p-4 mb-2">
        <div>
          <h2 className="text-[15px] font-semibold text-foreground">AI Action Plan</h2>
          <p className="text-[12px] text-muted-foreground mt-1">
            Tailored recommendations to reduce churn risk and maximize retention.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {recs.map((rec) => (
          <div
            key={rec.id}
            className={cn(
              "section-card p-5 border-l-4 transition-all duration-300",
              rec.status === 'completed' ? "opacity-60 border-l-success" : "border-l-primary"
            )}
          >
            <div className="flex items-start justify-between gap-4 mb-4">
              <div className="flex items-center gap-2">
                <Lightbulb className={cn("h-4.5 w-4.5", rec.status === 'completed' ? 'text-success' : 'text-primary')} />
                <Badge variant="outline" className={getPriorityColor(rec.priority)}>
                  {rec.priority.toUpperCase()}
                </Badge>
              </div>
              <span className="text-[11px] font-semibold text-muted-foreground bg-secondary px-2 py-0.5 rounded-full">
                Est. Impact: {rec.estimatedImpact}%
              </span>
            </div>

            <h3 className={cn("text-[14.5px] font-bold mb-3", rec.status === 'completed' && 'line-through text-muted-foreground')}>
              {rec.title}
            </h3>

            <div className="space-y-3 mb-5">
              <div>
                <span className="text-[11px] font-semibold uppercase text-muted-foreground mb-1 block">Business Reason</span>
                <p className="text-[13px] text-foreground/80 leading-relaxed">{rec.rationale}</p>
              </div>
              <div>
                <span className="text-[11px] font-semibold uppercase text-muted-foreground mb-1 block">Expected Impact</span>
                <p className="text-[13px] text-foreground/80 leading-relaxed">{rec.impactDescription}</p>
              </div>
            </div>

            <div className="flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-border">
              <div className="text-[11.5px] text-muted-foreground">
                Confidence: <span className="font-medium text-foreground">{rec.confidenceScore}%</span>
              </div>
              <Button
                variant={rec.status === 'completed' ? 'secondary' : 'primary'}
                size="sm"
                leftIcon={rec.status === 'completed' ? <Check className="h-4 w-4" /> : undefined}
                onClick={() => toggleComplete(rec.id)}
              >
                {rec.status === 'completed' ? 'Completed' : 'Mark as Complete'}
              </Button>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
