export function TypingIndicator() {
  return (
    <div className="flex justify-start animate-fade-in">
      <div className="rounded-2xl rounded-bl-sm bg-white border border-earth-200 px-4 py-3 shadow-sm">
        <div className="flex gap-1.5">
          <span className="h-2 w-2 rounded-full bg-green-400 animate-pulse-dot" style={{ animationDelay: '0ms' }} />
          <span className="h-2 w-2 rounded-full bg-green-400 animate-pulse-dot" style={{ animationDelay: '200ms' }} />
          <span className="h-2 w-2 rounded-full bg-green-400 animate-pulse-dot" style={{ animationDelay: '400ms' }} />
        </div>
      </div>
    </div>
  );
}
