import React from 'react';
import { Button } from "@/components/ui/button";
import { ArrowRight, ArrowLeft, ExternalLink, Home } from "lucide-react";
import ExplanationCard from '@/components/ExplanationCard';
import GaugeChart from '@/components/GaugeChart';
import { Card, CardContent } from '@/components/ui/card';
import { Link, useParams, useLocation } from 'react-router-dom';
import { articles } from '@/data/articles';

// Types for verification results
interface SourceInfo {
  source: string;
  url?: string;
  credibility_score?: number;
}

interface VerificationResult {
  truth_score: number;
  confidence_score: number;
  verdict: string;
  summary: string;
  supporting_sources: SourceInfo[];
  contradicting_sources: SourceInfo[];
  processing_time: number;
}

const breakingNewsHeadlines = [
  "BREAKING: Global Climate Summit Reaches Historic Agreement on Carbon Emissions",
  "URGENT: Major Cybersecurity Breach Affects Millions of Users Worldwide",
  "LIVE: International Trade Negotiations Enter Critical Phase",
  "ALERT: New Scientific Discovery Could Revolutionize Renewable Energy",
  "UPDATE: Economic Markets Show Unprecedented Recovery Patterns",
  "FLASH: Space Mission Successfully Lands on Mars, Sends First Images",
  "NEWS: Breakthrough Medical Treatment Shows 95% Success Rate in Trials",
  "REPORT: Global Food Security Initiative Launches in 50 Countries"
];

const ArticlePage = () => {
    const { id } = useParams();
    const location = useLocation();

    // Check if this is a verification result
    const isVerificationResult = id === 'verification-result';
    const verificationData = location.state as {
        verificationResult: VerificationResult;
        originalText: string;
        inputType: string;
    } | null;

    // Handle verification result display
    if (isVerificationResult && verificationData) {
        const { verificationResult, originalText, inputType } = verificationData;

        // Convert scores to percentages
        const truthScorePercent = Math.round(verificationResult.truth_score * 100);
        const confidencePercent = Math.round(verificationResult.confidence_score * 100);

        return (
            <div className="flex flex-col min-h-screen bg-muted/40 p-4 sm:p-6 md:p-8 relative">
                <div className="flex-grow grid md:grid-cols-2 gap-6 relative">
                    {/* Left side */}
                    <div className="flex flex-col gap-6">
                        <div className="flex justify-between items-start gap-4">
                            <h1 className="text-3xl font-bold font-serif max-w-lg">
                                {inputType === 'url' ? 'Article Verification' : 'Claim Verification'}
                            </h1>
                            {inputType === 'url' && (
                                <Button variant="outline" asChild>
                                    <a href={originalText} target="_blank" rel="noopener noreferrer">
                                        <ExternalLink className="mr-2 h-4 w-4" />
                                        View Original Article
                                    </a>
                                </Button>
                            )}
                        </div>

                        {/* Verification Info */}
                        <div className="flex items-center gap-4 p-4 bg-background rounded-lg border">
                            <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                                <span className="text-primary font-bold text-lg">AI</span>
                            </div>
                            <div>
                                <h3 className="font-semibold">TruthScore AI Verification</h3>
                                <p className="text-sm text-muted-foreground">@truthscore_ai</p>
                                <div className="flex items-center gap-2 mt-1">
                                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded font-semibold">
                                        🤖 {verificationResult.verdict}
                                    </span>
                                    <span className="text-xs text-muted-foreground">
                                        Processed in {verificationResult.processing_time.toFixed(2)}s
                                    </span>
                                </div>
                            </div>
                        </div>

                        {/* Original Text */}
                        <Card>
                            <CardContent className="p-4">
                                <h4 className="font-semibold mb-2">Original {inputType === 'url' ? 'URL' : 'Text'}:</h4>
                                <p className="text-sm text-muted-foreground break-words">{originalText}</p>
                            </CardContent>
                        </Card>

                        <ExplanationCard verificationResult={verificationResult} />
                    </div>

                    {/* Right side */}
                    <div className="flex flex-col gap-6">
                        <div className="grid grid-cols-2 gap-6">
                            <Card>
                                <CardContent className="p-4 flex flex-col items-center justify-center">
                                    <GaugeChart value={truthScorePercent} label="Truth Score" />
                                </CardContent>
                            </Card>
                            <Card>
                                <CardContent className="p-4 flex flex-col items-center justify-center">
                                    <GaugeChart value={confidencePercent} label="Confidence" />
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                </div>

                <div className="mt-8">
                    <Link to="/">
                        <Button variant="outline">Back to Dashboard</Button>
                    </Link>
                </div>

                {/* Go Back to Home Button - Fixed at lower right corner */}
                <Link to="/" className="fixed bottom-6 right-6 z-50">
                    <Button
                        variant="default"
                        size="lg"
                        className="rounded-full shadow-lg hover:shadow-xl transition-shadow"
                        title="Go back to home"
                    >
                        <Home className="mr-2 h-5 w-5" />
                        Home
                    </Button>
                </Link>
            </div>
        );
    }

    // Check if this is a breaking news article
    const isBreakingNews = id?.startsWith('breaking-');

    if (isBreakingNews) {
        const breakingIndex = parseInt(id.replace('breaking-', '')) - 1;
        const breakingTitle = breakingNewsHeadlines[breakingIndex] || breakingNewsHeadlines[0];

        // Create a mock breaking news article
        const breakingArticle = {
            id: id,
            title: breakingTitle,
            author: "TruthScore News Team",
            handle: "@truthscore",
            category: "Breaking News",
            date: new Date().toLocaleDateString(),
            avatarUrl: "/placeholder.svg",
            imageUrl: "https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=2070&auto=format&fit=crop"
        };

        return (
            <div className="flex flex-col min-h-screen bg-muted/40 p-4 sm:p-6 md:p-8 relative">
                <div className="flex-grow grid md:grid-cols-2 gap-6 relative">
                    {/* Left side */}
                    <div className="flex flex-col gap-6">
                        <div className="flex justify-between items-start gap-4">
                            <h1 className="text-3xl font-bold font-serif max-w-lg">
                                {breakingArticle.title}
                            </h1>
                            <Button variant="outline" asChild>
                                <a href="#" target="_blank" rel="noopener noreferrer">
                                    <ExternalLink className="mr-2 h-4 w-4" />
                                    Read Original Article
                                </a>
                            </Button>
                        </div>

                        {/* Article Info */}
                        <div className="flex items-center gap-4 p-4 bg-background rounded-lg border">
                            <img src={breakingArticle.avatarUrl} alt={breakingArticle.author} className="w-12 h-12 rounded-full object-cover" />
                            <div>
                                <h3 className="font-semibold">{breakingArticle.author}</h3>
                                <p className="text-sm text-muted-foreground">{breakingArticle.handle}</p>
                                <div className="flex items-center gap-2 mt-1">
                                    <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded font-semibold">🔴 {breakingArticle.category}</span>
                                    <span className="text-xs text-muted-foreground">{breakingArticle.date}</span>
                                </div>
                            </div>
                        </div>

                        <ExplanationCard />
                    </div>

                    {/* Right side */}
                    <div className="flex flex-col gap-6">
                        <div className="grid grid-cols-2 gap-6">
                            <Card>
                                <CardContent className="p-4 flex flex-col items-center justify-center">
                                    <GaugeChart value={85} label="Truth Score" />
                                </CardContent>
                            </Card>
                            <Card>
                                <CardContent className="p-4 flex flex-col items-center justify-center">
                                    <GaugeChart value={75} label="Confidence" />
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                </div>

                <div className="mt-8">
                    <Link to="/">
                        <Button variant="outline">Back to Dashboard</Button>
                    </Link>
                </div>

                {/* Go Back to Home Button - Fixed at lower right corner */}
                <Link to="/" className="fixed bottom-6 right-6 z-50">
                    <Button
                        variant="default"
                        size="lg"
                        className="rounded-full shadow-lg hover:shadow-xl transition-shadow"
                        title="Go back to home"
                    >
                        <Home className="mr-2 h-5 w-5" />
                        Home
                    </Button>
                </Link>
            </div>
        );
    }

    // Regular article logic
    const currentId = id ? parseInt(id, 10) : 1;

    // Find current article
    const currentArticle = articles.find(article => article.id === currentId);

    // Find current article index
    const currentIndex = articles.findIndex(article => article.id === currentId);

    // Find next article in the list (loop back to first after last)
    const nextIndex = (currentIndex + 1) % articles.length;
    const nextArticle = articles[nextIndex];

    // Find previous article in the list (loop back to last after first)
    const prevIndex = (currentIndex - 1 + articles.length) % articles.length;
    const prevArticle = articles[prevIndex];

    // If no current article found, default to first article
    const displayArticle = currentArticle || articles[0];

    return (
        <div className="flex flex-col min-h-screen bg-muted/40 p-4 sm:p-6 md:p-8 relative">
            <div className="flex-grow grid md:grid-cols-2 gap-6 relative">
                {/* Left side */}
                <div className="flex flex-col gap-6">
                    <div className="flex justify-between items-start gap-4">
                        <h1 className="text-3xl font-bold font-serif max-w-lg">
                            {displayArticle.title}
                        </h1>
                        <Button variant="outline" asChild>
                            <a href="#" target="_blank" rel="noopener noreferrer">
                                <ExternalLink className="mr-2 h-4 w-4" />
                                Read Original Article
                            </a>
                        </Button>
                    </div>

                    {/* Article Info */}
                    <div className="flex items-center gap-4 p-4 bg-background rounded-lg border">
                        <img src={displayArticle.avatarUrl} alt={displayArticle.author} className="w-12 h-12 rounded-full object-cover" />
                        <div>
                            <h3 className="font-semibold">{displayArticle.author}</h3>
                            <p className="text-sm text-muted-foreground">{displayArticle.handle}</p>
                            <div className="flex items-center gap-2 mt-1">
                                <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded">{displayArticle.category}</span>
                                <span className="text-xs text-muted-foreground">{displayArticle.date}</span>
                            </div>
                        </div>
                    </div>

                    <ExplanationCard />
                </div>

                {/* Right side */}
                <div className="flex flex-col gap-6">
                    <div className="grid grid-cols-2 gap-6">
                        <Card>
                            <CardContent className="p-4 flex flex-col items-center justify-center">
                                <GaugeChart value={75} label="Truth Score" />
                            </CardContent>
                        </Card>
                        <Card>
                            <CardContent className="p-4 flex flex-col items-center justify-center">
                                <GaugeChart value={80} label="Confidence" />
                            </CardContent>
                        </Card>
                    </div>
                </div>

                {/* Previous Article Button */}
                <Link to={`/article/${prevArticle.id}`} className="absolute top-1/2 -left-4 md:-left-8 transform -translate-y-1/2">
                     <Button variant="outline" size="icon" title={`Previous: ${prevArticle.title}`}>
                        <ArrowLeft className="h-4 w-4" />
                    </Button>
                </Link>

                {/* Next Article Button */}
                <Link to={`/article/${nextArticle.id}`} className="absolute top-1/2 -right-4 md:-right-8 transform -translate-y-1/2">
                     <Button variant="outline" size="icon" title={`Next: ${nextArticle.title}`}>
                        <ArrowRight className="h-4 w-4" />
                    </Button>
                </Link>
            </div>
             <div className="mt-8">
                <Link to="/">
                    <Button variant="outline">Back to Dashboard</Button>
                </Link>
            </div>

            {/* Go Back to Home Button - Fixed at lower right corner */}
            <Link to="/" className="fixed bottom-6 right-6 z-50">
                <Button
                    variant="default"
                    size="lg"
                    className="rounded-full shadow-lg hover:shadow-xl transition-shadow"
                    title="Go back to home"
                >
                    <Home className="mr-2 h-5 w-5" />
                    Home
                </Button>
            </Link>
        </div>
    );
};

export default ArticlePage;
