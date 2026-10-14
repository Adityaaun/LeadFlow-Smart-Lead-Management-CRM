'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { DashboardHeader } from '@/components/header/DashboardHeader';
import { StatusFilter } from '@/components/filters/StatusFilter';
import { SearchInput } from '@/components/filters/SearchInput';
import { TodayFollowUps } from '@/components/leads/TodayFollowUps';
import { LeadList } from '@/components/leads/LeadList';
import { AddLeadDialog } from '@/components/dialogs/AddLeadDialog';
import { LeadTimelineDialog } from '@/components/dialogs/LeadTimelineDialog';
import { LeadListItem } from '@/types';
import { api } from '@/lib/api';

export default function DashboardPage() {
  const [leads, setLeads] = useState<LeadListItem[]>([]);
  const [todayFollowUps, setTodayFollowUps] = useState<LeadListItem[]>([]);
  const [selectedStatus, setSelectedStatus] = useState<string>('All');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Dialog states
  const [selectedLeadId, setSelectedLeadId] = useState<number | null>(null);
  const [isAddModalOpen, setIsAddModalOpen] = useState<boolean>(false);

  // Fetch leads and today's followups
  const loadData = useCallback(async () => {
    try {
      setIsLoading(true);
      const [leadsData, followUpsData] = await Promise.all([
        api.getLeads(selectedStatus, searchTerm),
        api.getTodayFollowUps(),
      ]);
      setLeads(leadsData);
      setTodayFollowUps(followUpsData);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
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

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans text-gray-900">
      {/* Top Navbar */}
      <DashboardHeader onOpenAddModal={() => setIsAddModalOpen(true)} />

      {/* Main Dashboard Content */}
      <main className="flex-1 max-w-4xl w-full mx-auto px-4 sm:px-6 py-8 space-y-6">
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

        {/* All Leads Section */}
        <LeadList
          leads={leads}
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
