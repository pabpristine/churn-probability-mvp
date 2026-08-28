import * as React from 'react';
import { Search } from 'lucide-react';
import { cn } from '@/utils';
import { useClientStore } from '@/store/client.store';

// ============================================================
// ClientSearch
// ============================================================

export function ClientSearch() {
  const { filters, updateFilter } = useClientStore();
  const inputRef = React.useRef<HTMLInputElement>(null);

  // Ctrl+K shortcut
  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="relative w-full max-w-2xl">
      <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
        <Search className="h-5 w-5 text-muted-foreground" />
      </div>
      <input
        ref={inputRef}
        type="text"
        className={cn(
          'block w-full pl-10 pr-16 py-3',
          'bg-card border border-border rounded-xl',
          'text-[14px] text-foreground placeholder:text-muted-foreground',
          'focus:outline-none focus:ring-2 focus:ring-primary/40 focus:border-primary/60 transition-shadow',
          'shadow-sm hover:border-border-hover'
        )}
        placeholder="Search by Client Name, Industry, or Account Manager..."
        value={filters.search}
        onChange={(e) => updateFilter('search', e.target.value)}
      />
      <div className="absolute inset-y-0 right-0 pr-3.5 flex items-center pointer-events-none">
        <kbd className="hidden sm:inline-flex items-center gap-1 px-1.5 py-0.5 rounded border border-border bg-secondary text-[10px] font-medium text-muted-foreground">
          <span className="text-[12px]">⌘</span>K
        </kbd>
      </div>
    </div>
  );
}
