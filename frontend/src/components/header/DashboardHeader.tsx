import React from 'react';
import { TrendingUp, Plus } from 'lucide-react';

interface DashboardHeaderProps {
  onOpenAddModal: () => void;
}

export const DashboardHeader: React.FC<DashboardHeaderProps> = ({ onOpenAddModal }) => {
  return (
    <header className="w-full bg-white border-b border-gray-100 py-4 px-6 md:px-12 flex items-center justify-between shadow-xs">
      <div className="flex items-center gap-2">
        <TrendingUp className="w-7 h-7 text-blue-600 stroke-[2.5]" />
        <span className="text-2xl font-bold text-blue-600 tracking-tight">LeadFlow</span>
      </div>
      <button
        type="button"
        onClick={onOpenAddModal}
        className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white font-medium text-sm rounded-lg transition-colors shadow-xs"
      >
        <Plus className="w-4 h-4 stroke-[2.5]" />
        <span>Add New Lead</span>
      </button>
    </header>
  );
};
