import React from 'react';
import { LeadListItem } from '@/types';
import { LeadCard } from './LeadCard';

interface TodayFollowUpsProps {
  leads: LeadListItem[];
  onSelectLead: (lead: LeadListItem) => void;
}

export const TodayFollowUps: React.FC<TodayFollowUpsProps> = ({
  leads,
  onSelectLead,
}) => {
  if (leads.length === 0) {
    return null;
  }

  return (
    <section className="w-full">
      <div className="flex items-center gap-1.5 mb-3">
        <span role="img" aria-label="pin" className="text-sm">📌</span>
        <h2 className="text-xs font-bold uppercase tracking-wider text-gray-600">
          TODAY&apos;S FOLLOW-UPS
        </h2>
      </div>
      <div className="space-y-3">
        {leads.map((lead) => (
          <LeadCard
            key={lead.id}
            lead={lead}
            isPinned={true}
            onClick={() => onSelectLead(lead)}
          />
        ))}
      </div>
    </section>
  );
};
