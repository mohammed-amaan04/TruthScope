import React, { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeft, Send } from 'lucide-react';
import ChatMessage from '@/components/ChatMessage';
import { articles } from '@/data/articles';

// Mock chat messages
const mockMessages = [
    {
        id: 1,
        sender: {
            name: "Alice Johnson",
            avatarUrl: "/placeholder.svg"
        },
        text: "I think this article raises some important points about the current situation.",
        timestamp: "2:30 PM",
        isCurrentUser: false
    },
    {
        id: 2,
        sender: {
            name: "You",
            avatarUrl: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fDE?q=80&w=1780&auto=format&fit=crop"
        },
        text: "I agree, but I'm not sure about the statistics mentioned. Do we have verification for those numbers?",
        timestamp: "2:32 PM",
        isCurrentUser: true
    },
    {
        id: 3,
        sender: {
            name: "Bob Smith",
            avatarUrl: "/placeholder.svg"
        },
        text: "Good point! I found some conflicting data from another source. Let me share the link.",
        timestamp: "2:35 PM",
        isCurrentUser: false
    },
    {
        id: 4,
        sender: {
            name: "Carol Davis",
            avatarUrl: "/placeholder.svg"
        },
        text: "This is exactly why we need better fact-checking mechanisms in journalism.",
        timestamp: "2:38 PM",
        isCurrentUser: false
    }
];

const ChatroomPage = () => {
    const { id } = useParams();
    const [newMessage, setNewMessage] = useState('');
    const [messages, setMessages] = useState(mockMessages);
    
    // Find the article for this chatroom
    const article = articles.find(a => a.id === parseInt(id || '1'));
    const articleTitle = article?.title || "Article Discussion";

    const handleSendMessage = (e: React.FormEvent) => {
        e.preventDefault();
        if (newMessage.trim()) {
            const message = {
                id: messages.length + 1,
                sender: {
                    name: "You",
                    avatarUrl: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fDE?q=80&w=1780&auto=format&fit=crop"
                },
                text: newMessage,
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
                isCurrentUser: true
            };
            setMessages([...messages, message]);
            setNewMessage('');
        }
    };

    return (
        <div className="min-h-screen bg-muted/40">
            <div className="container mx-auto p-4 sm:p-6 md:p-8 max-w-4xl">
                {/* Header */}
                <header className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-4">
                        <Button variant="outline" size="icon" asChild>
                            <Link to="/debates">
                                <ArrowLeft className="h-4 w-4" />
                            </Link>
                        </Button>
                        <div>
                            <h1 className="text-2xl font-bold font-serif">Debate Room</h1>
                            <p className="text-sm text-muted-foreground">{articleTitle}</p>
                        </div>
                    </div>
                    <Button variant="outline" asChild>
                        <Link to="/">Back to Dashboard</Link>
                    </Button>
                </header>

                {/* Chat Container */}
                <Card className="h-[600px] flex flex-col">
                    <CardHeader>
                        <CardTitle className="text-lg">Discussion</CardTitle>
                    </CardHeader>
                    
                    {/* Messages Area */}
                    <CardContent className="flex-1 flex flex-col">
                        <div className="flex-1 overflow-y-auto space-y-4 mb-4 p-4 bg-muted/20 rounded-lg">
                            {messages.map((message) => (
                                <ChatMessage key={message.id} message={message} />
                            ))}
                        </div>
                        
                        {/* Message Input */}
                        <form onSubmit={handleSendMessage} className="flex gap-2">
                            <Input
                                value={newMessage}
                                onChange={(e) => setNewMessage(e.target.value)}
                                placeholder="Type your message..."
                                className="flex-1"
                            />
                            <Button type="submit" size="icon">
                                <Send className="h-4 w-4" />
                            </Button>
                        </form>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

export default ChatroomPage;
