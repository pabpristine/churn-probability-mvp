import * as React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, X, MessageSquare, ArrowUp } from 'lucide-react';
import { cn } from '@/utils';

// ============================================================
// Floating AI Assistant Button
// ============================================================

interface AIMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

const WELCOME_PROMPTS = [
  'Which clients have the highest churn risk?',
  'Summarize last month\'s performance',
  'Show me workflow failures from today',
];

export function FloatingAIAssistant() {
  const [open, setOpen] = React.useState(false);
  const [input, setInput] = React.useState('');
  const inputRef = React.useRef<HTMLInputElement>(null);

  React.useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 150);
    }
  }, [open]);

  return (
    <>
      {/* ── Panel ── */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 12, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 12, scale: 0.96 }}
            transition={{ duration: 0.2, ease: [0.25, 0, 0, 1] }}
            className={cn(
              'fixed bottom-[84px] right-6 z-50 w-80',
              'section-card overflow-hidden',
              'shadow-xl'
            )}
            style={{ boxShadow: '0 20px 60px -10px rgb(0 0 0 / 0.15), 0 8px 20px -8px rgb(0 0 0 / 0.1)' }}
          >
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-border">
              <div className="flex items-center gap-2">
                <div className="flex h-6 w-6 items-center justify-center rounded-md bg-primary">
                  <Sparkles className="h-3.5 w-3.5 text-white" strokeWidth={2.5} />
                </div>
                <div>
                  <p className="text-[13px] font-semibold text-foreground leading-tight">Dirt2Dollar AI</p>
                  <p className="text-[11px] text-muted-foreground leading-tight">Ask me anything</p>
                </div>
              </div>
              <button
                className="icon-btn"
                onClick={() => setOpen(false)}
                aria-label="Close AI assistant"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            {/* Content area */}
            <div className="h-52 flex flex-col items-center justify-center gap-4 px-4 bg-secondary/30">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
                <Sparkles className="h-6 w-6 text-primary" />
              </div>
              <div className="text-center">
                <p className="text-[13.5px] font-semibold text-foreground">Ask Dirt2Dollar AI</p>
                <p className="text-[12px] text-muted-foreground mt-0.5">
                  Intelligent insights about your clients & workflows
                </p>
              </div>

              {/* Quick prompts */}
              <div className="w-full space-y-1.5">
                {WELCOME_PROMPTS.map((prompt) => (
                  <button
                    key={prompt}
                    className={cn(
                      'w-full text-left px-3 py-2 rounded-lg text-[12px] font-medium',
                      'text-muted-foreground hover:text-foreground',
                      'bg-card border border-border hover:border-primary/30 hover:bg-primary/5',
                      'transition-all duration-150'
                    )}
                    onClick={() => setInput(prompt)}
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>

            {/* Input */}
            <div className="px-3 py-3 border-t border-border bg-card">
              <div className={cn(
                'flex items-center gap-2 rounded-lg bg-secondary border border-border px-3 h-9',
                'focus-within:border-primary/50 focus-within:ring-[3px] focus-within:ring-primary/10',
                'transition-all duration-150'
              )}>
                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask anything…"
                  aria-label="Ask AI assistant"
                  className="flex-1 bg-transparent text-[13px] text-foreground placeholder:text-muted-foreground outline-none"
                />
                <button
                  disabled={!input.trim()}
                  aria-label="Send message"
                  className={cn(
                    'flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-md',
                    'transition-all duration-150',
                    input.trim()
                      ? 'bg-primary text-white hover:bg-primary/90'
                      : 'bg-muted text-muted-foreground cursor-not-allowed'
                  )}
                >
                  <ArrowUp className="h-3.5 w-3.5" strokeWidth={2.5} />
                </button>
              </div>
              <p className="text-[10.5px] text-muted-foreground/50 text-center mt-2">
                AI is for guidance only. Verify decisions independently.
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ── FAB ── */}
      <motion.button
        className="ai-fab"
        onClick={() => setOpen(!open)}
        aria-label="Ask Dirt2Dollar AI"
        title="Ask Dirt2Dollar AI"
        whileTap={{ scale: 0.93 }}
      >
        <AnimatePresence mode="wait" initial={false}>
          {open ? (
            <motion.span
              key="close"
              initial={{ rotate: -60, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: 60, opacity: 0 }}
              transition={{ duration: 0.15 }}
            >
              <X className="h-5 w-5" />
            </motion.span>
          ) : (
            <motion.span
              key="open"
              initial={{ rotate: 60, opacity: 0 }}
              animate={{ rotate: 0, opacity: 1 }}
              exit={{ rotate: -60, opacity: 0 }}
              transition={{ duration: 0.15 }}
            >
              <Sparkles className="h-5 w-5" />
            </motion.span>
          )}
        </AnimatePresence>
      </motion.button>
    </>
  );
}

export default FloatingAIAssistant;
