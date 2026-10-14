import React from 'react';
import { LeadListItem, LeadStatus } from '@/types';
import { Bell } from 'lucide-react';

interface LeadCardProps {
  lead: LeadListItem;
  onClick: () => void;
  isPinned?: boolean;
}

const STATUS_STYLES: Record<LeadStatus, string> = {
  New: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  Contacted: 'bg-amber-50 text-amber-800 border-amber-200',
  Qualified: 'bg-blue-50 text-blue-700 border-blue-200',
  'Proposal Sent': 'bg-purple-50 text-purple-700 border-purple-200',
  Won: 'bg-gray-100 text-gray-700 border-gray-200',
  Lost: 'bg-rose-50 text-rose-700 border-rose-200',
};

function formatTimeOnly(dateString: string): string {
  try {
    const d = new Date(dateString);
    return d.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
  } catch {
    return '';
  }
}

function formatRelativeTime(dateString?: string | null): string {
  if (!dateString) return '';
  try {
    const date = new Date(dateString);
    const now = new Date();
    const diffSec = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (diffSec < 60) return 'just now';
    const diffMin = Math.floor(diffSec / 60);
    if (diffMin < 60) return `${diffMin}m ago`;
    const diffHours = Math.floor(diffMin / 60);
    if (diffHours < 24) return `${diffHours} ${diffHours === 1 ? 'hour' : 'hours'} ago`;
    const diffDays = Math.floor(diffHours / 24);
    if (diffDays < 7) return `${diffDays} ${diffDays === 1 ? 'day' : 'days'} ago`;
    const diffWeeks = Math.floor(diffDays / 7);
    return `${diffWeeks} ${diffWeeks === 1 ? 'week' : 'weeks'} ago`;
  } catch {
    return '';
  }
}

export const LeadCard: React.FC<LeadCardProps> = ({ lead, onClick, isPinned = false }) => {
  const statusClass =
    STATUS_STYLES[lead.status] || 'bg-gray-50 text-gray-700 border-gray-200';

  return (
    <div
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick();
        }
      }}
      className={`w-full text-left p-5 rounded-xl border transition-all cursor-pointer shadow-xs hover:shadow-md ${
        isPinned
          ? 'bg-blue-50/50 border-blue-200 hover:border-blue-300'
          : 'bg-white border-gray-200 hover:border-gray-300'
      }`}
    >
      <div className="flex items-start justify-between gap-4 mb-2">
        <div>
          <span className="font-bold text-gray-900 text-base">
            {lead.name}
          </span>
          {lead.company && (
            <span className="text-gray-500 font-normal text-sm ml-1.5">
              ({lead.company})
            </span>
          )}
        </div>
        <span
          className={`text-xs uppercase font-semibold px-2.5 py-0.5 rounded-full border ${statusClass}`}
        >
          {lead.status}
        </span>
      </div>

      {lead.last_note && (
        <p className="text-sm text-gray-600 line-clamp-1 mb-2">
          <span className="font-medium text-gray-800">Last Note:</span>{' '}
          {lead.last_note}{' '}
          <span className="text-gray-400 text-xs ml-1">
            {formatRelativeTime(lead.last_note_created_at)}
          </span>
        </p>
      )}

      {isPinned && lead.next_follow_up && (
        <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-blue-100/70 border border-blue-200 rounded-lg text-xs font-medium text-blue-800 mt-1">
          <Bell className="w-3.5 h-3.5 text-blue-700" />
          <span>Follow-up today at {formatTimeOnly(lead.next_follow_up)}</span>
        </div>
      )}
    </div>
  );
};
