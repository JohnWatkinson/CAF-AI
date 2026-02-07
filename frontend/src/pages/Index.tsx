import { useChat } from '@/hooks/useChat';
import { ChatHeader, ChatMessages, ChatInput, ChatFooter } from '@/components/chat';

const Index = () => {
  const { messages, isLoading, send, reset } = useChat();

  return (
    <div className="flex flex-col h-screen bg-card">
      <ChatHeader onReset={reset} />
      <ChatMessages messages={messages} isLoading={isLoading} />
      <ChatInput onSend={send} isLoading={isLoading} />
      <ChatFooter />
    </div>
  );
};

export default Index;
