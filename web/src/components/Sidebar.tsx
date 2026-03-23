import { User, Globe, Radio, Sprout, Trash2 } from 'lucide-react';
import { FARMERS, LANGUAGES, CHANNELS } from '../data';
import type { Language, Channel, FarmerOption } from '../types';

interface SidebarProps {
  selectedFarmer: FarmerOption;
  selectedLanguage: Language;
  selectedChannel: Channel;
  onFarmerChange: (farmer: FarmerOption) => void;
  onLanguageChange: (language: Language) => void;
  onChannelChange: (channel: Channel) => void;
  onClearChat: () => void;
  apiStatus: 'connected' | 'disconnected' | 'checking';
}

export function Sidebar({
  selectedFarmer,
  selectedLanguage,
  selectedChannel,
  onFarmerChange,
  onLanguageChange,
  onChannelChange,
  onClearChat,
  apiStatus,
}: SidebarProps) {
  return (
    <aside className="flex w-72 flex-col border-r border-earth-200 bg-white">
      {/* Logo */}
      <div className="flex items-center gap-3 border-b border-earth-100 px-5 py-4">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-green-600">
          <Sprout size={20} className="text-white" />
        </div>
        <div>
          <h1 className="font-display text-lg font-bold text-earth-900">InDaba</h1>
          <p className="text-xs text-earth-400">Agricultural Advisory</p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-5">
        {/* API Status */}
        <div className="flex items-center gap-2 rounded-lg bg-earth-50 px-3 py-2 text-xs">
          <span
            className={`h-2 w-2 rounded-full ${
              apiStatus === 'connected'
                ? 'bg-green-500'
                : apiStatus === 'checking'
                  ? 'bg-amber-400 animate-pulse'
                  : 'bg-red-400'
            }`}
          />
          <span className="text-earth-500">
            API {apiStatus === 'connected' ? 'Connected' : apiStatus === 'checking' ? 'Checking...' : 'Offline'}
          </span>
        </div>

        {/* Farmer Profile */}
        <Section icon={<User size={14} />} title="Farmer Profile">
          <div className="space-y-1.5">
            {FARMERS.map((farmer) => (
              <button
                key={farmer.id}
                onClick={() => onFarmerChange(farmer)}
                className={`w-full rounded-lg px-3 py-2 text-left text-xs transition-colors ${
                  selectedFarmer.id === farmer.id
                    ? 'bg-green-50 border border-green-200 text-green-800'
                    : 'bg-earth-50 text-earth-600 hover:bg-earth-100'
                }`}
              >
                <div className="font-semibold">{farmer.name}</div>
                <div className="text-earth-400">{farmer.province} · {farmer.farmType}</div>
              </button>
            ))}
          </div>
        </Section>

        {/* Language */}
        <Section icon={<Globe size={14} />} title="Language">
          <select
            value={selectedLanguage}
            onChange={(event) => onLanguageChange(event.target.value as Language)}
            className="w-full rounded-lg border border-earth-200 bg-earth-50 px-3 py-2 text-xs text-earth-700 outline-none focus:border-green-300"
          >
            {LANGUAGES.map((lang) => (
              <option key={lang.value} value={lang.value}>{lang.label}</option>
            ))}
          </select>
        </Section>

        {/* Channel Simulator */}
        <Section icon={<Radio size={14} />} title="Channel">
          <div className="grid grid-cols-2 gap-1.5">
            {CHANNELS.map((channel) => (
              <button
                key={channel.value}
                onClick={() => onChannelChange(channel.value)}
                className={`rounded-lg px-2 py-1.5 text-xs transition-colors ${
                  selectedChannel === channel.value
                    ? 'bg-green-50 border border-green-200 text-green-700 font-medium'
                    : 'bg-earth-50 text-earth-500 hover:bg-earth-100'
                }`}
              >
                {channel.label}
              </button>
            ))}
          </div>
          <p className="mt-1.5 text-[10px] text-earth-300">
            Changes how InDaba formats responses
          </p>
        </Section>
      </div>

      {/* Clear chat */}
      <div className="border-t border-earth-100 px-4 py-3">
        <button
          onClick={onClearChat}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-earth-50 py-2 text-xs text-earth-400 transition-colors hover:bg-red-50 hover:text-red-500"
        >
          <Trash2 size={12} />
          Clear conversation
        </button>
      </div>
    </aside>
  );
}

function Section({ icon, title, children }: { icon: React.ReactNode; title: string; children: React.ReactNode }) {
  return (
    <div>
      <div className="mb-2 flex items-center gap-1.5 text-xs font-semibold text-earth-400 uppercase tracking-wider">
        {icon}
        {title}
      </div>
      {children}
    </div>
  );
}
