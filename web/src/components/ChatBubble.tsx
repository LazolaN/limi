import Markdown from 'react-markdown';
import type { ChatMessage } from '../types';
import { ConfidenceBadge } from './ConfidenceBadge';
import { IntentBadge } from './IntentBadge';
import { AlertTriangle } from 'lucide-react';

export function ChatBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex animate-fade-in ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-green-700 text-white rounded-br-sm'
            : 'bg-white border border-earth-200 text-earth-900 rounded-bl-sm shadow-sm'
        }`}
      >
        {/* Message content */}
        {isUser ? (
          <p className="text-sm">{message.text}</p>
        ) : (
          <div className="chat-markdown text-sm leading-relaxed">
            <Markdown>{message.text}</Markdown>
          </div>
        )}

        {/* Metadata badges (assistant only) */}
        {!isUser && message.metadata && (
          <div className="mt-3 flex flex-wrap items-center gap-2 border-t border-earth-100 pt-2">
            {message.metadata.confidence && (
              <ConfidenceBadge level={message.metadata.confidence} />
            )}
            {message.metadata.intent && (
              <IntentBadge intent={message.metadata.intent} />
            )}
            {message.metadata.escalated && (
              <span className="inline-flex items-center gap-1 rounded-full bg-red-100 px-2 py-0.5 text-xs font-medium text-red-700">
                <AlertTriangle size={12} />
                Escalated
              </span>
            )}
            {message.metadata.sources && message.metadata.sources.length > 0 && (
              <span className="text-xs text-earth-400">
                {message.metadata.sources.length} source{message.metadata.sources.length > 1 ? 's' : ''}
              </span>
            )}
          </div>
        )}

        {/* Timestamp */}
        <div className={`mt-1 text-[10px] ${isUser ? 'text-green-200' : 'text-earth-300'}`}>
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
}
