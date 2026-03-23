import { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

interface ChatInputProps {
  onSend: (text: string) => void;
  disabled: boolean;
  placeholder?: string;
}

export function ChatInput({ onSend, disabled, placeholder }: ChatInputProps) {
  const [text, setText] = useState('');
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (!disabled) inputRef.current?.focus();
  }, [disabled]);

  const handleSubmit = () => {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText('');
  };

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="flex items-end gap-2 rounded-2xl border border-earth-200 bg-white p-2 shadow-sm">
      <textarea
        ref={inputRef}
        value={text}
        onChange={(event) => setText(event.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        placeholder={placeholder ?? 'Ask InDaba a question...'}
        rows={1}
        className="flex-1 resize-none bg-transparent px-2 py-1.5 text-sm text-earth-900 placeholder-earth-300 outline-none"
        style={{ maxHeight: '120px' }}
      />
      <button
        onClick={handleSubmit}
        disabled={disabled || !text.trim()}
        className="flex h-9 w-9 items-center justify-center rounded-xl bg-green-600 text-white transition-colors hover:bg-green-700 disabled:bg-earth-200 disabled:text-earth-400"
      >
        <Send size={16} />
      </button>
    </div>
  );
}
