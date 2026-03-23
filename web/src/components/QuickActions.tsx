import { QUICK_QUESTIONS } from '../data';

interface QuickActionsProps {
  onSelect: (question: string) => void;
}

export function QuickActions({ onSelect }: QuickActionsProps) {
  return (
    <div className="space-y-3 animate-fade-in">
      <p className="text-center text-sm text-earth-400">Try asking:</p>
      <div className="flex flex-wrap justify-center gap-2">
        {QUICK_QUESTIONS.map((question) => (
          <button
            key={question}
            onClick={() => onSelect(question)}
            className="rounded-full border border-earth-200 bg-white px-3 py-1.5 text-xs text-earth-600 transition-colors hover:border-green-300 hover:bg-green-50 hover:text-green-700"
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
}
