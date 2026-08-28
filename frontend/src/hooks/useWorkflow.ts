import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useWorkflowStore } from '@/store';
import { workflowService } from '@/services';
import { QUERY_STALE_TIME } from '@/constants';
import { toast } from 'sonner';

// ============================================================
// Workflow Hook
// ============================================================

export function useWorkflow() {
  const store = useWorkflowStore();
  const queryClient = useQueryClient();

  const workflowsQuery = useQuery({
    queryKey: ['workflows'],
    queryFn: () => workflowService.list().then((r) => r.data),
    staleTime: QUERY_STALE_TIME.SHORT,
  });

  const statsQuery = useQuery({
    queryKey: ['workflows', 'stats'],
    queryFn: () => workflowService.getStats().then((r) => r.data),
    staleTime: QUERY_STALE_TIME.SHORT,
  });

  const executeMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data?: Record<string, unknown> }) =>
      workflowService.execute(id, data).then((r) => r.data),
    onSuccess: (execution) => {
      store.setCurrentExecution(execution);
      queryClient.invalidateQueries({ queryKey: ['workflows'] });
      toast.success('Workflow started successfully');
    },
    onError: () => {
      toast.error('Failed to execute workflow');
    },
  });

  const pauseMutation = useMutation({
    mutationFn: (id: string) => workflowService.pause(id),
    onSuccess: (_, id) => {
      store.updateWorkflowStatus(id, 'paused');
      toast.success('Workflow paused');
    },
    onError: () => {
      toast.error('Failed to pause workflow');
    },
  });

  const resumeMutation = useMutation({
    mutationFn: (id: string) => workflowService.resume(id),
    onSuccess: (_, id) => {
      store.updateWorkflowStatus(id, 'active');
      toast.success('Workflow resumed');
    },
    onError: () => {
      toast.error('Failed to resume workflow');
    },
  });

  return {
    workflows: workflowsQuery.data ?? store.workflows,
    stats: statsQuery.data ?? store.stats,
    currentExecution: store.currentExecution,
    isLoading: workflowsQuery.isLoading,
    isError: workflowsQuery.isError,
    execute: executeMutation.mutate,
    pause: pauseMutation.mutate,
    resume: resumeMutation.mutate,
    isExecuting: executeMutation.isPending,
    refetch: workflowsQuery.refetch,
  };
}
