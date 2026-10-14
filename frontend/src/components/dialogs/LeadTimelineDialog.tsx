'use client';

import React, { useState, useEffect } from 'react';
import {
  X,
  Phone,
  Calendar,
  Check,
  ChevronDown,
  Loader2,
} from 'lucide-react';
import { LeadDetail, LeadStatus } from '@/types';
import { api } from '@/lib/api';

interface LeadTimelineDialogProps {
  leadId: number | null;
  isOpen: boolean;
  onClose: () => void;
  onLeadUpdated: () => void;
}

const ALL_STATUSES: LeadStatus[] = [
  'New',
  'Contacted',
  'Qualified',
  'Proposal Sent',
  'Won',
  'Lost',
];

function formatTimelineDate(dateStr: string): string {
  try {
    const d = new Date(dateStr);
    const dateFormatted = d.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    });
    const timeFormatted = d.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true,
    });
    return `${dateFormatted}, ${timeFormatted}`;
  } catch {
    return dateStr;
  }
}

function formatFollowUpDate(dateStr: string): string {
  try {
    const d = new Date(dateStr);
    const dateFormatted = d.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    });
    const timeFormatted = d.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true,
    });
    return `${dateFormatted}, ${timeFormatted}`;
  } catch {
    return dateStr;
  }
}

function formatRelativeTime(dateStr: string): string {
  try {
    const date = new Date(dateStr);
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

export const LeadTimelineDialog: React.FC<LeadTimelineDialogProps> = ({
  leadId,
  isOpen,
  onClose,
  onLeadUpdated,
}) => {
  const [lead, setLead] = useState<LeadDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [statusDropdownOpen, setStatusDropdownOpen] = useState(false);

  // New Note State
  const [note, setNote] = useState('');
  const [setFollowUp, setSetFollowUp] = useState(false);
  const [followUpDate, setFollowUpDate] = useState('');
  const [followUpTime, setFollowUpTime] = useState('');
  const [isSavingNote, setIsSavingNote] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen && leadId) {
      fetchLeadDetails(leadId);
    } else {
      setLead(null);
      setNote('');
      setSetFollowUp(false);
      setFollowUpDate('');
      setFollowUpTime('');
      setError(null);
      setStatusDropdownOpen(false);
    }
  }, [isOpen, leadId]);

  const fetchLeadDetails = async (id: number) => {
    try {
      setLoading(true);
      const data = await api.getLead(id);
      setLead(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Failed to fetch lead details.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (newStatus: LeadStatus) => {
    if (!lead) return;
    try {
      setStatusDropdownOpen(false);
      const updated = await api.updateLeadStatus(lead.id, newStatus);
      setLead(updated);
      onLeadUpdated();
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      }
    }
  };

  const handleSaveNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!lead || !note.trim()) return;

    let followUpIso: string | null = null;
    if (setFollowUp && followUpDate) {
      const timeVal = followUpTime || '09:00';
      followUpIso = `${followUpDate}T${timeVal}:00`;
    }

    try {
      setIsSavingNote(true);
      setError(null);
      await api.addDiscussion(lead.id, {
        note: note.trim(),
        follow_up_at: followUpIso,
      });

      // Clear input
      setNote('');
      setSetFollowUp(false);
      setFollowUpDate('');
      setFollowUpTime('');

      // Refresh lead details
      await fetchLeadDetails(lead.id);
      onLeadUpdated();
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Failed to save discussion note.');
      }
    } finally {
      setIsSavingNote(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-xs">
      <div
        className="w-full max-w-2xl max-h-[90vh] bg-white rounded-2xl shadow-2xl border border-gray-100 flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-150"
        role="dialog"
        aria-modal="true"
      >
        {/* Modal Header */}
        <div className="flex items-start justify-between px-6 pt-6 pb-4 border-b border-gray-100">
          <div>
            <div className="flex items-baseline gap-2">
              <h2 className="text-xl font-bold text-gray-900">
                {lead?.name || 'Loading...'}
              </h2>
              {lead?.company && (
                <span className="text-sm font-normal text-gray-500">
                  ({lead.company})
                </span>
              )}
            </div>
            {lead?.phone && (
              <div className="flex items-center gap-1.5 text-xs text-gray-500 mt-1">
                <Phone className="w-3.5 h-3.5" />
                <span>{lead.phone}</span>
              </div>
            )}
          </div>

          <div className="flex items-center gap-3">
            {/* Status Selector Dropdown */}
            {lead && (
              <div className="relative">
                <button
                  type="button"
                  onClick={() => setStatusDropdownOpen(!statusDropdownOpen)}
                  className="inline-flex items-center gap-2 px-3.5 py-1.5 text-sm font-medium bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors shadow-xs"
                >
                  <span>{lead.status}</span>
                  <ChevronDown className="w-4 h-4 text-gray-400" />
                </button>

                {statusDropdownOpen && (
                  <div className="absolute right-0 mt-1 w-44 bg-white rounded-xl shadow-lg border border-gray-200 py-1.5 z-50 animate-in fade-in zoom-in-95 duration-100">
                    {ALL_STATUSES.map((st) => (
                      <button
                        key={st}
                        type="button"
                        onClick={() => handleStatusChange(st)}
                        className="w-full text-left px-3.5 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center justify-between transition-colors"
                      >
                        <span>{st}</span>
                        {lead.status === st && (
                          <Check className="w-4 h-4 text-blue-600 stroke-[2.5]" />
                        )}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}

            <button
              type="button"
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 p-1 rounded-lg transition-colors"
              aria-label="Close dialog"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Modal Body / Timeline */}
        <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">
          {error && (
            <div className="p-3 text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg">
              {error}
            </div>
          )}

          {loading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
            </div>
          ) : (
            <div className="relative pl-6 space-y-6 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-gray-200">
              {lead?.discussions.map((disc, idx) => {
                const isLatest = idx === 0;
                const isInitialCreation =
                  disc.note.toLowerCase().includes('created via') ||
                  disc.note.toLowerCase().includes('inbound lead');

                return (
                  <div key={disc.id} className="relative group">
                    {/* Timeline bullet */}
                    <div
                      className={`absolute -left-6 top-1.5 w-3 h-3 rounded-full border-2 border-white ring-2 ${
                        isLatest
                          ? 'bg-blue-600 ring-blue-200'
                          : 'bg-gray-300 ring-gray-100'
                      }`}
                    />

                    {/* Timestamp header */}
                    <div className="text-xs text-gray-500 mb-1.5">
                      <span className="font-medium text-gray-700">
                        {formatTimelineDate(disc.created_at)}
                      </span>{' '}
                      <span className="text-gray-400">
                        ({formatRelativeTime(disc.created_at)})
                      </span>
                    </div>

                    {/* Discussion Content Box */}
                    <div className="p-3.5 bg-white border border-gray-200 rounded-xl shadow-xs">
                      <p
                        className={`text-sm text-gray-800 ${
                          isInitialCreation ? 'italic text-gray-600' : ''
                        }`}
                      >
                        {disc.note}
                      </p>

                      {disc.follow_up_at && (
                        <div className="inline-flex items-center gap-1.5 mt-2 px-2.5 py-1 bg-blue-50 border border-blue-200 text-blue-700 rounded-md text-xs font-medium">
                          <Calendar className="w-3.5 h-3.5" />
                          <span>
                            Follow-up set for: {formatFollowUpDate(disc.follow_up_at)}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Modal Footer / Log Note Input */}
        <form
          onSubmit={handleSaveNote}
          className="border-t border-gray-100 px-6 py-4 bg-gray-50/50 space-y-3"
        >
          <textarea
            rows={2}
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Log a new discussion..."
            className="w-full px-3.5 py-2.5 text-sm bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all placeholder:text-gray-400 text-gray-900 resize-none"
          />

          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-3 flex-wrap text-sm">
              <label className="inline-flex items-center gap-2 cursor-pointer text-gray-700 font-medium text-xs">
                <input
                  type="checkbox"
                  checked={setFollowUp}
                  onChange={(e) => setSetFollowUp(e.target.checked)}
                  className="w-4 h-4 rounded text-blue-600 focus:ring-blue-500 border-gray-300"
                />
                <span>Set Follow-up</span>
              </label>

              {setFollowUp && (
                <div className="flex items-center gap-2">
                  <input
                    type="date"
                    required={setFollowUp}
                    value={followUpDate}
                    onChange={(e) => setFollowUpDate(e.target.value)}
                    className="px-2.5 py-1 text-xs border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-1 focus:ring-blue-500 text-gray-800"
                  />
                  <input
                    type="time"
                    value={followUpTime}
                    onChange={(e) => setFollowUpTime(e.target.value)}
                    className="px-2.5 py-1 text-xs border border-gray-300 rounded-lg bg-white focus:outline-none focus:ring-1 focus:ring-blue-500 text-gray-800"
                  />
                </div>
              )}
            </div>

            <button
              type="submit"
              disabled={isSavingNote || !note.trim()}
              className="inline-flex items-center gap-2 px-5 py-2 text-xs font-semibold text-white bg-slate-900 hover:bg-slate-800 active:bg-black rounded-lg shadow-xs transition-colors disabled:opacity-40"
            >
              {isSavingNote && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
              <span>Save Note</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
