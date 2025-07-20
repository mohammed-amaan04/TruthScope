import React from 'react';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from '@/lib/utils';

type ChatMessageProps = {
    message: {
        id: number;
        sender: {
            name: string;
            avatarUrl: string;
        };
        text: string;
        timestamp: string;
        isCurrentUser: boolean;
    };
};

const ChatMessage = ({ message }: ChatMessageProps) => {
    const { sender, text, timestamp, isCurrentUser } = message;

    return (
        <div className={cn("flex items-start gap-3", isCurrentUser ? "justify-end" : "justify-start")}>
            {!isCurrentUser && (
                <Avatar className="h-8 w-8">
                    <AvatarImage src={sender.avatarUrl} alt={sender.name} />
                    <AvatarFallback>{sender.name.charAt(0)}</AvatarFallback>
                </Avatar>
            )}
            <div className={cn(
                "flex flex-col gap-1 max-w-xs md:max-w-md",
                isCurrentUser ? "items-end" : "items-start"
            )}>
                <div className={cn(
                    "rounded-lg px-3 py-2",
                    isCurrentUser ? "bg-primary text-primary-foreground" : "bg-muted"
                )}>
                    {!isCurrentUser && <p className="text-sm font-semibold mb-1">{sender.name}</p>}
                    <p className="text-sm">{text}</p>
                </div>
                <span className="text-xs text-muted-foreground">{timestamp}</span>
            </div>
            {isCurrentUser && (
                <Avatar className="h-8 w-8">
                    <AvatarImage src={sender.avatarUrl} alt={sender.name} />
                    <AvatarFallback>{sender.name.charAt(0)}</AvatarFallback>
                </Avatar>
            )}
        </div>
    );
};

export default ChatMessage;
