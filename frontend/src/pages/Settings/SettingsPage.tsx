import * as React from 'react';
import { ContentWrapper } from '@/components/common/PageHeader';
import { PageHeader, SectionHeader } from '@/components/common/PageHeader';
import { SectionCard } from '@/components/common/MetricCard';
import { Button } from '@/components/ui/Button';
import { useSettingsStore } from '@/store';
import { Sun, Moon, Monitor, User, Bell, Link2, ShieldCheck, Check } from 'lucide-react';
import { cn } from '@/utils';
import type { Theme } from '@/types';
import { toast } from 'sonner';

export function SettingsPage() {
  const { theme, setTheme } = useSettingsStore();

  // Profile Form States
  const [profile, setProfile] = React.useState({
    name: 'Alex Johnson',
    email: 'alex.johnson@dirt2dollar.ai',
    role: 'Admin'
  });
  const [savingProfile, setSavingProfile] = React.useState(false);

  // Notification States
  const [notifications, setNotifications] = React.useState({
    emailAlerts: true,
    workflowAlerts: true,
    riskAlerts: false
  });
  const [savingNotifications, setSavingNotifications] = React.useState(false);

  const themes: { value: Theme; label: string; icon: typeof Sun; description: string }[] = [
    { value: 'light',  label: 'Light',  icon: Sun,     description: 'Clean white interface' },
    { value: 'dark',   label: 'Dark',   icon: Moon,    description: 'Easy on the eyes' },
    { value: 'system', label: 'System', icon: Monitor,  description: 'Follows OS setting' },
  ];

  const handleProfileSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSavingProfile(true);
    setTimeout(() => {
      setSavingProfile(false);
      toast.success('Profile settings updated successfully');
    }, 800);
  };

  const handleNotificationSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSavingNotifications(true);
    setTimeout(() => {
      setSavingNotifications(false);
      toast.success('Notification preferences updated');
    }, 800);
  };

  return (
    <ContentWrapper className="max-w-3xl space-y-6">
      <PageHeader title="Settings" description="Manage your user profile, alert preferences, and connector integrations." />

      {/* Appearance */}
      <SectionCard className="p-5">
        <SectionHeader title="Appearance" description="Customize the look and feel of the application" />
        <div className="mt-4">
          <p className="text-[12.5px] font-semibold text-foreground mb-3">Theme Mode</p>
          <div className="flex gap-3 flex-wrap">
            {themes.map(({ value, label, icon: Icon, description }) => (
              <button
                key={value}
                onClick={() => setTheme(value)}
                className={cn(
                  'flex flex-col items-center gap-2 rounded-xl border-2 p-4 w-28 transition-all duration-150',
                  'text-[12.5px] font-medium cursor-pointer select-none',
                  theme === value
                    ? 'border-primary bg-primary/5 text-primary'
                    : 'border-border text-muted-foreground hover:border-border hover:bg-secondary hover:text-foreground'
                )}
                aria-pressed={theme === value}
                title={description}
              >
                <Icon className="h-5 w-5" strokeWidth={1.75} />
                {label}
              </button>
            ))}
          </div>
        </div>
      </SectionCard>

      {/* Profile */}
      <SectionCard className="p-5">
        <SectionHeader title="User Profile" description="Update your personal account credentials" />
        <form onSubmit={handleProfileSave} className="space-y-4 mt-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-xs font-semibold text-muted-foreground">Full Name</label>
              <input
                type="text"
                value={profile.name}
                onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                className="w-full bg-secondary/40 border border-border focus:border-primary focus:ring-1 focus:ring-primary rounded-lg px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground"
              />
            </div>
            <div className="space-y-1">
              <label className="text-xs font-semibold text-muted-foreground">Email Address</label>
              <input
                type="email"
                value={profile.email}
                onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                className="w-full bg-secondary/40 border border-border focus:border-primary focus:ring-1 focus:ring-primary rounded-lg px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground"
              />
            </div>
          </div>
          <div className="space-y-1">
            <label className="text-xs font-semibold text-muted-foreground">User Permission Role</label>
            <select
              value={profile.role}
              onChange={(e) => setProfile({ ...profile, role: e.target.value })}
              className="w-full bg-secondary/40 border border-border focus:border-primary focus:ring-1 focus:ring-primary rounded-lg px-3 py-2 text-sm text-foreground"
            >
              <option value="Admin">Administrator</option>
              <option value="Manager">Account Manager</option>
              <option value="Viewer">Viewer (Read-Only)</option>
            </select>
          </div>
          <Button type="submit" variant="primary" size="sm" isLoading={savingProfile} leftIcon={<User className="h-3.5 w-3.5" />}>
            Save Profile
          </Button>
        </form>
      </SectionCard>

      {/* Notifications */}
      <SectionCard className="p-5">
        <SectionHeader title="Notification Preferences" description="Configure alert channels and alert types" />
        <form onSubmit={handleNotificationSave} className="space-y-4 mt-4">
          <div className="space-y-3">
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={notifications.emailAlerts}
                onChange={(e) => setNotifications({ ...notifications, emailAlerts: e.target.checked })}
                className="rounded border-border text-primary focus:ring-primary/40"
              />
              <div>
                <p className="text-sm font-semibold text-foreground">Email Notifications</p>
                <p className="text-xs text-muted-foreground">Receive daily updates and summary digests of client health changes.</p>
              </div>
            </label>

            <label className="flex items-center gap-3 cursor-pointer border-t pt-3">
              <input
                type="checkbox"
                checked={notifications.workflowAlerts}
                onChange={(e) => setNotifications({ ...notifications, workflowAlerts: e.target.checked })}
                className="rounded border-border text-primary focus:ring-primary/40"
              />
              <div>
                <p className="text-sm font-semibold text-foreground">Workflow Execution Logs</p>
                <p className="text-xs text-muted-foreground">Get notified on successful orchestrator steps and HuggingFace/Groq completion.</p>
              </div>
            </label>

            <label className="flex items-center gap-3 cursor-pointer border-t pt-3">
              <input
                type="checkbox"
                checked={notifications.riskAlerts}
                onChange={(e) => setNotifications({ ...notifications, riskAlerts: e.target.checked })}
                className="rounded border-border text-primary focus:ring-primary/40"
              />
              <div>
                <p className="text-sm font-semibold text-foreground">Critical Churn Risk Alerts</p>
                <p className="text-xs text-muted-foreground">Immediate alerts whenever an account passes the 75% Churn Probability threshold.</p>
              </div>
            </label>
          </div>
          <Button type="submit" variant="primary" size="sm" isLoading={savingNotifications} leftIcon={<Bell className="h-3.5 w-3.5" />}>
            Save Preferences
          </Button>
        </form>
      </SectionCard>

      {/* Integrations */}
      <SectionCard className="p-5">
        <SectionHeader title="Enterprise Integrations" description="Manage database and LLM API connections" />
        <div className="space-y-4 mt-4">
          <div className="flex items-center justify-between p-3.5 border rounded-xl bg-secondary/20">
            <div className="flex items-center gap-3">
              <div className="bg-success/10 text-success p-2 rounded-lg">
                <Link2 className="h-4 w-4" />
              </div>
              <div>
                <p className="text-sm font-bold text-foreground">Google Sheets Connector</p>
                <p className="text-xs text-muted-foreground">Google Drive spreadsheet data stream</p>
              </div>
            </div>
            <span className="flex items-center gap-1 text-[11px] bg-success/15 text-success font-extrabold px-2.5 py-1 rounded-full uppercase tracking-wider">
              <ShieldCheck className="h-3.5 w-3.5" /> Connected
            </span>
          </div>

          <div className="flex items-center justify-between p-3.5 border rounded-xl bg-secondary/20">
            <div className="flex items-center gap-3">
              <div className="bg-success/10 text-success p-2 rounded-lg">
                <Link2 className="h-4 w-4" />
              </div>
              <div>
                <p className="text-sm font-bold text-foreground">Supabase PostgreSQL</p>
                <p className="text-xs text-muted-foreground">Vector similarity embeddings database</p>
              </div>
            </div>
            <span className="flex items-center gap-1 text-[11px] bg-success/15 text-success font-extrabold px-2.5 py-1 rounded-full uppercase tracking-wider">
              <ShieldCheck className="h-3.5 w-3.5" /> Connected
            </span>
          </div>

          <div className="flex items-center justify-between p-3.5 border rounded-xl bg-secondary/20">
            <div className="flex items-center gap-3">
              <div className="bg-success/10 text-success p-2 rounded-lg">
                <Link2 className="h-4 w-4" />
              </div>
              <div>
                <p className="text-sm font-bold text-foreground">Groq Cloud API</p>
                <p className="text-xs text-muted-foreground">Real-time reasoning engine completions</p>
              </div>
            </div>
            <span className="flex items-center gap-1 text-[11px] bg-success/15 text-success font-extrabold px-2.5 py-1 rounded-full uppercase tracking-wider">
              <ShieldCheck className="h-3.5 w-3.5" /> Connected
            </span>
          </div>
        </div>
      </SectionCard>
    </ContentWrapper>
  );
}

export default SettingsPage;

