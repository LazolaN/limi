/** Mirrors the backend enums for the frontend. */

export type Channel = 'ussd' | 'whatsapp' | 'ivr' | 'web' | 'sms';
export type Language = 'zu' | 'xh' | 'st' | 'af' | 'en';
export type ContentType = 'text' | 'image' | 'audio' | 'location';
export type ConfidenceLevel = 'HIGH' | 'MEDIUM' | 'LOW';
export type RiskLevel = 'high' | 'medium' | 'low';
export type Intent = string;

export interface LimiMessage {
  message_id: string;
  farmer_id: string;
  channel: Channel;
  language: Language;
  content_type: ContentType;
  content: { text?: string; media_url?: string };
  session_id: string;
}

export interface QueryResponse {
  message_id: string;
  response_text: string;
  confidence: ConfidenceLevel;
  intent: Intent;
  sources_used: string[];
  channel: Channel;
  language: Language;
  risk_level: RiskLevel;
  escalated: boolean;
}

export interface FarmerOption {
  id: string;
  name: string;
  language: Language;
  province: string;
  farmType: string;
  crops: string[];
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  timestamp: Date;
  metadata?: {
    confidence?: ConfidenceLevel;
    intent?: Intent;
    sources?: string[];
    escalated?: boolean;
    riskLevel?: RiskLevel;
  };
}
