import React from 'react';
import { LeadListItem } from '@/types';
import { LeadCard } from './LeadCard';

interface LeadListProps {
  leads: LeadListItem[];
  isLoading: boolean;
  onSelectLead: (lead: LeadListItem) => void;
}

export const LeadList: React.FC<LeadListProps> = ({
  leads,
  isLoading,
  onSelectLead,
}) => {
  return (
    <section className="w-full">
      <h2 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-3">
        ALL LEADS
      </h2>

      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((n) => (
            <div
              key={n}
              className="w-full h-24 bg-gray-100 animate-pulse rounded-xl border border-gray-200"
            />
          ))}
        </div>
      ) : leads.length === 0 ? (
        <div className="w-full p-8 text-center bg-gray-50 rounded-xl border border-dashed border-gray-300">
          <p className="text-sm font-medium text-gray-500">
            No leads found matching your criteria.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {leads.map((lead) => (
            <LeadCard
              key={lead.id}
              lead={lead}
              onClick={() => onSelectLead(lead)}
            />
          ))}
        </div>
      )}
    </section>
  );
};
