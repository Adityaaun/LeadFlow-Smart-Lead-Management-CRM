export type LeadStatus =
  | 'New'
  | 'Contacted'
  | 'Qualified'
  | 'Proposal Sent'
  | 'Won'
  | 'Lost';

export interface Discussion {
  id: number;
  lead_id: number;
  note: string;
  created_at: string;
  follow_up_at?: string | null;
}

export interface LeadListItem {
  id: number;
  name: string;
  company?: string | null;
  phone?: string | null;
  status: LeadStatus;
  created_at: string;
  updated_at: string;
  last_note?: string | null;
  last_note_created_at?: string | null;
  next_follow_up?: string | null;
  is_today_follow_up: boolean;
}

export interface LeadDetail {
  id: number;
  name: string;
  company?: string | null;
  phone?: string | null;
  status: LeadStatus;
  created_at: string;
  updated_at: string;
  discussions: Discussion[];
  next_follow_up?: string | null;
}

export interface CreateLeadPayload {
  name: string;
  company?: string;
  phone?: string;
  status?: LeadStatus;
  initial_note?: string;
  initial_follow_up_at?: string;
}

export interface UpdateStatusPayload {
  status: LeadStatus;
}

export interface CreateDiscussionPayload {
  note: string;
  follow_up_at?: string | null;
}
