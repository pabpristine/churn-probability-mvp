import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { recommendationService } from '@/services';
import { QUERY_STALE_TIME } from '@/constants';
import { toast } from 'sonner';

// ============================================================
// Recommendations Hook
// ============================================================

export function useRecommendations(clientId?: string) {
  const queryClient = useQueryClient();

  const recommendationsQuery = useQuery({
    queryKey: ['recommendations', clientId],
    queryFn: () =>
      recommendationService
        .list(clientId ? { clientId } : undefined)
        .then((r) => r.data),
    staleTime: QUERY_STALE_TIME.MEDIUM,
  });

  const summaryQuery = useQuery({
    queryKey: ['recommendations', 'summary'],
    queryFn: () => recommendationService.getSummary().then((r) => r.data),
    staleTime: QUERY_STALE_TIME.MEDIUM,
  });

  const dismissMutation = useMutation({
    mutationFn: ({ id, reason }: { id: string; reason?: string }) =>
      recommendationService.dismiss(id, reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recommendations'] });
      toast.success('Recommendation dismissed');
    },
    onError: () => {
      toast.error('Failed to dismiss recommendation');
    },
  });

  const completeMutation = useMutation({
    mutationFn: ({ id, notes }: { id: string; notes?: string }) =>
      recommendationService.complete(id, notes),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recommendations'] });
      toast.success('Recommendation marked complete');
    },
    onError: () => {
      toast.error('Failed to update recommendation');
    },
  });

  const generateMutation = useMutation({
    mutationFn: (cId?: string) => recommendationService.generate(cId).then((r) => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['recommendations'] });
      toast.success('New recommendations generated');
    },
    onError: () => {
      toast.error('Failed to generate recommendations');
    },
  });

  return {
    recommendations: recommendationsQuery.data ?? [],
    summary: summaryQuery.data,
    isLoading: recommendationsQuery.isLoading,
    isError: recommendationsQuery.isError,
    dismiss: dismissMutation.mutate,
    complete: completeMutation.mutate,
    generate: generateMutation.mutate,
    isGenerating: generateMutation.isPending,
    refetch: recommendationsQuery.refetch,
  };
}
