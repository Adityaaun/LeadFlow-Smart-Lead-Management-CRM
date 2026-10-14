'use client';

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { DashboardHeader } from '@/components/header/DashboardHeader';
import { StatusFilter } from '@/components/filters/StatusFilter';
import { SearchInput } from '@/components/filters/SearchInput';
import { TodayFollowUps } from '@/components/leads/TodayFollowUps';
import { LeadList } from '@/components/leads/LeadList';
import { AddLeadDialog } from '@/components/dialogs/AddLeadDialog';
import { LeadTimelineDialog } from '@/components/dialogs/LeadTimelineDialog';
import { LeadListItem } from '@/types';
import { api } from '@/lib/api';
import { AlertCircle, RefreshCw } from 'lucide-react';

export default function DashboardPage() {
  const [leads, setLeads] = useState<LeadListItem[]>([]);
  const [todayFollowUps, setTodayFollowUps] = useState<LeadListItem[]>([]);
  const [selectedStatus, setSelectedStatus] = useState<string>('All');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [fetchError, setFetchError] = useState<string | null>(null);

  // Dialog states
  const [selectedLeadId, setSelectedLeadId] = useState<number | null>(null);
  const [isAddModalOpen, setIsAddModalOpen] = useState<boolean>(false);

  // Fetch leads and today's followups
  const loadData = useCallback(async () => {
    try {
      setIsLoading(true);
      setFetchError(null);
      const [leadsData, followUpsData] = await Promise.all([
        api.getLeads(selectedStatus, searchTerm),
        api.getTodayFollowUps(),
      ]);
      setLeads(leadsData);
      setTodayFollowUps(followUpsData);
    } catch (err: unknown) {
      console.error('Error fetching dashboard data:', err);
      if (err instanceof Error) {
        setFetchError(`Could not connect to backend: ${err.message}. Ensure the FastAPI server is running.`);
      } else {
        setFetchError('Failed to load leads from the server.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [selectedStatus, searchTerm]);

  // Debounced search & filter effect
  useEffect(() => {
    const timer = setTimeout(() => {
      loadData();
    }, 200);

    return () => clearTimeout(timer);
  }, [loadData]);

  // Exclude leads already shown in pinned today's follow-ups so no lead appears twice
  const mainListLeads = useMemo(() => {
    const pinnedIds = new Set(todayFollowUps.map((l) => l.id));
    return leads.filter((lead) => !pinnedIds.has(lead.id));
  }, [leads, todayFollowUps]);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans text-gray-900">
      {/* Top Navbar */}
      <DashboardHeader onOpenAddModal={() => setIsAddModalOpen(true)} />

      {/* Main Dashboard Content */}
      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 py-8 space-y-6">
        {/* Error notification banner */}
        {fetchError && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-800 text-sm flex items-center justify-between shadow-xs">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-red-600 shrink-0" />
              <span>{fetchError}</span>
            </div>
            <button
              type="button"
              onClick={loadData}
              className="inline-flex items-center gap-1.5 px-3 py-1 bg-red-100 hover:bg-red-200 text-red-900 rounded-lg text-xs font-semibold transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retry</span>
            </button>
          </div>
        )}

        {/* Filters and Search Bar */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <StatusFilter
            selectedStatus={selectedStatus}
            onSelectStatus={setSelectedStatus}
          />
          <SearchInput
            value={searchTerm}
            onChange={setSearchTerm}
          />
        </div>

        {/* Pinned Today's Follow-ups */}
        <TodayFollowUps
          leads={todayFollowUps}
          onSelectLead={(lead) => setSelectedLeadId(lead.id)}
        />

        {/* All Leads Section (excluding leads already pinned) */}
        <LeadList
          leads={mainListLeads}
          isLoading={isLoading}
          onSelectLead={(lead) => setSelectedLeadId(lead.id)}
        />
      </main>

      {/* Add Lead Modal */}
      <AddLeadDialog
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onLeadAdded={loadData}
      />

      {/* Lead Timeline & Edit Modal */}
      <LeadTimelineDialog
        leadId={selectedLeadId}
        isOpen={selectedLeadId !== null}
        onClose={() => setSelectedLeadId(null)}
        onLeadUpdated={loadData}
      />
    </div>
  );
}
