import React from 'react';
import { Link } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft, MessagesSquare } from 'lucide-react';
import { articles } from '@/data/articles';

const ChatroomListPage = () => {
    return (
        <div className="min-h-screen bg-muted/40">
            <div className="container mx-auto p-4 sm:p-6 md:p-8">
                <header className="flex items-center justify-between mb-8">
                    <h1 className="text-3xl font-bold font-serif">My Debates</h1>
                    <Button variant="outline" asChild>
                        <Link to="/">
                            <ArrowLeft />
                            Back to Dashboard
                        </Link>
                    </Button>
                </header>
                <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                    {articles.map((article) => (
                        <Card key={article.id} className="flex flex-col h-full hover:shadow-lg transition-shadow duration-200">
                            <CardHeader>
                                <CardTitle className="text-lg">{article.title}</CardTitle>
                                <CardDescription>{article.category}</CardDescription>
                            </CardHeader>
                            <CardContent className="flex-grow flex items-end">
                                <Button asChild className="w-full mt-4">
                                    <Link to={`/debate/${article.id}`}>
                                        <MessagesSquare />
                                        Enter Chatroom
                                    </Link>
                                </Button>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ChatroomListPage;
