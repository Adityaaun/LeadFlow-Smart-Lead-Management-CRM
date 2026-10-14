import React from 'react';

interface StatusFilterProps {
  selectedStatus: string;
  onSelectStatus: (status: string) => void;
}

const FILTER_OPTIONS: { label: string; value: string }[] = [
  { label: 'All', value: 'All' },
  { label: 'New', value: 'New' },
  { label: 'Contacted', value: 'Contacted' },
  { label: 'Qualified', value: 'Qualified' },
  { label: 'Proposal Sent', value: 'Proposal Sent' },
  { label: 'Won', value: 'Won' },
  { label: 'Lost', value: 'Lost' },
];

export const StatusFilter: React.FC<StatusFilterProps> = ({
  selectedStatus,
  onSelectStatus,
}) => {
  return (
    <div className="flex items-center gap-2 flex-wrap">
      <span className="text-xs font-semibold tracking-wider text-gray-500 uppercase mr-2">
        FILTERS:
      </span>
      <div className="flex items-center gap-2 flex-wrap">
        {FILTER_OPTIONS.map((option) => {
          const isActive = selectedStatus.toLowerCase() === option.value.toLowerCase();
          return (
            <button
              key={option.value}
              type="button"
              onClick={() => onSelectStatus(option.value)}
              className={`px-4 py-1.5 text-sm rounded-full font-medium transition-all ${
                isActive
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'bg-white text-gray-700 border border-gray-200 hover:border-gray-300 hover:bg-gray-50'
              }`}
            >
              {option.label}
            </button>
          );
        })}
      </div>
    </div>
  );
};
