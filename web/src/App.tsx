import { useState, useCallback, useRef, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { ChatBubble } from './components/ChatBubble';
import { ChatInput } from './components/ChatInput';
import { TypingIndicator } from './components/TypingIndicator';
import { QuickActions } from './components/QuickActions';
import { sendQuery, checkHealth } from './api';
import { FARMERS } from './data';
import type { ChatMessage, Channel, Language, FarmerOption } from './types';

export default function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedFarmer, setSelectedFarmer] = useState<FarmerOption>(FARMERS[0]);
  const [selectedLanguage, setSelectedLanguage] = useState<Language>(FARMERS[0].language);
  const [selectedChannel, setSelectedChannel] = useState<Channel>('web');
  const [apiStatus, setApiStatus] = useState<'connected' | 'disconnected' | 'checking'>('checking');

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const sessionId = useRef(`web-${Date.now()}`);

  // Check API health on mount
  useEffect(() => {
    checkHealth()
      .then(() => setApiStatus('connected'))
      .catch(() => setApiStatus('disconnected'));
  }, []);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Sync language when farmer changes
  const handleFarmerChange = useCallback((farmer: FarmerOption) => {
    setSelectedFarmer(farmer);
    setSelectedLanguage(farmer.language);
  }, []);

  const handleSend = useCallback(async (text: string) => {
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendQuery({
        message_id: `msg-${Date.now()}`,
        farmer_id: selectedFarmer.id,
        channel: selectedChannel,
        language: selectedLanguage,
        content_type: 'text',
        content: { text },
        session_id: sessionId.current,
      });

      const assistantMessage: ChatMessage = {
        id: response.message_id,
        role: 'assistant',
        text: response.response_text,
        timestamp: new Date(),
        metadata: {
          confidence: response.confidence,
          intent: response.intent,
          sources: response.sources_used,
          escalated: response.escalated,
          riskLevel: response.risk_level,
        },
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        text: error instanceof Error
          ? `Sorry, something went wrong: ${error.message}`
          : 'Sorry, I could not process your request. Please check that the API server is running on port 8000.',
        timestamp: new Date(),
        metadata: { confidence: 'LOW', intent: 'general_agri' },
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [selectedFarmer, selectedChannel, selectedLanguage]);

  const handleClearChat = useCallback(() => {
    setMessages([]);
    sessionId.current = `web-${Date.now()}`;
  }, []);

  const isEmpty = messages.length === 0;

  return (
    <div className="flex h-full">
      {/* Sidebar */}
      <Sidebar
        selectedFarmer={selectedFarmer}
        selectedLanguage={selectedLanguage}
        selectedChannel={selectedChannel}
        onFarmerChange={handleFarmerChange}
        onLanguageChange={setSelectedLanguage}
        onChannelChange={setSelectedChannel}
        onClearChat={handleClearChat}
        apiStatus={apiStatus}
      />

      {/* Main chat area */}
      <main className="flex flex-1 flex-col bg-earth-50">
        {/* Header */}
        <header className="flex items-center justify-between border-b border-earth-200 bg-white px-6 py-3">
          <div>
            <h2 className="font-display text-sm font-semibold text-earth-800">
              Chatting as {selectedFarmer.name}
            </h2>
            <p className="text-xs text-earth-400">
              {selectedFarmer.province} · {selectedChannel.toUpperCase()} channel · {selectedLanguage.toUpperCase()}
            </p>
          </div>
          <div className="flex items-center gap-2 text-xs text-earth-300">
            <span className="rounded bg-earth-100 px-2 py-0.5 font-mono">Claude Sonnet 4</span>
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-6 py-4">
          {isEmpty ? (
            <div className="flex h-full flex-col items-center justify-center gap-6">
              <div className="text-center">
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-green-100">
                  <span className="text-3xl">🌱</span>
                </div>
                <h3 className="font-display text-xl font-bold text-earth-800">
                  Sawubona! Welcome to InDaba
                </h3>
                <p className="mt-1 max-w-md text-sm text-earth-400">
                  I'm your agricultural advisor. Ask me about crop diseases, market prices,
                  planting calendars, livestock health, or soil management.
                </p>
              </div>
              <QuickActions onSelect={handleSend} />
            </div>
          ) : (
            <div className="mx-auto max-w-2xl space-y-4">
              {messages.map((message) => (
                <ChatBubble key={message.id} message={message} />
              ))}
              {isLoading && <TypingIndicator />}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input */}
        <div className="border-t border-earth-200 bg-white px-6 py-3">
          <div className="mx-auto max-w-2xl">
            <ChatInput
              onSend={handleSend}
              disabled={isLoading}
              placeholder={
                selectedLanguage === 'zu'
                  ? 'Buza InDaba umbuzo...'
                  : selectedLanguage === 'xh'
                    ? 'Buza InDaba umbuzo...'
                    : 'Ask InDaba a question...'
              }
            />
          </div>
        </div>
      </main>
    </div>
  );
}
