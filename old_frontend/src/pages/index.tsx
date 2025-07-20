import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Search, Newspaper, User, Settings, LogOut, Bell, LayoutDashboard, Star, Eye, MessageSquare, ArrowRight, Instagram, Twitter, Facebook, Loader2 } from "lucide-react";
import StatisticsChart from '@/components/StatisticsChart';
import { articles } from '@/data/articles';

// API configuration
const API_BASE_URL = 'http://localhost:8000';

// Types for API responses
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

const chartData = [
  { name: 'Jun 1', Followers: 24, Likes: 18, Views: 30 },
  { name: 'Jun 2', Followers: 25, Likes: 22, Views: 35 },
  { name: 'Jun 3', Followers: 22, Likes: 20, Views: 28 },
  { name: 'Jun 4', Followers: 24, Likes: 25, Views: 32 },
  { name: 'Jun 5', Followers: 24, Likes: 19, Views: 29 },
];

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



const Index = () => {
  const [currentHeadlineIndex, setCurrentHeadlineIndex] = useState(0);
  const [searchText, setSearchText] = useState('');
  const [articleUrl, setArticleUrl] = useState('');
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationResult, setVerificationResult] = useState<VerificationResult | null>(null);
  const navigate = useNavigate();

  // Rotate headlines every 15 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentHeadlineIndex((prevIndex) =>
        (prevIndex + 1) % breakingNewsHeadlines.length
      );
    }, 15000); // 15 seconds

    return () => clearInterval(interval);
  }, []);

  // API function to verify text
  const verifyText = async (text: string, inputType: string = 'headline') => {
    try {
      setIsVerifying(true);

      const response = await fetch(`${API_BASE_URL}/api/v1/verify/text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          input_type: inputType
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: VerificationResult = await response.json();
      setVerificationResult(result);

      // Navigate to article page with the result
      navigate('/article/verification-result', {
        state: {
          verificationResult: result,
          originalText: text,
          inputType: inputType
        }
      });

    } catch (error) {
      console.error('Verification failed:', error);
      alert('Verification failed. Please try again.');
    } finally {
      setIsVerifying(false);
    }
  };

  // Handle search verification
  const handleSearchVerification = () => {
    if (searchText.trim()) {
      verifyText(searchText, 'headline');
    }
  };

  // Handle URL verification
  const handleUrlVerification = () => {
    if (articleUrl.trim()) {
      verifyText(articleUrl, 'url');
    }
  };

  // Handle Enter key press
  const handleKeyPress = (event: React.KeyboardEvent, action: () => void) => {
    if (event.key === 'Enter') {
      action();
    }
  };

  return (
    <div className="grid grid-cols-[260px_1fr_300px] min-h-screen w-full font-sans bg-muted/40">
      {/* Left Sidebar */}
      <aside className="flex flex-col border-r bg-background p-4">
        <div className="flex items-center gap-2 p-2 pb-4">
          <Newspaper className="h-6 w-6" />
          <h1 className="font-semibold text-xl font-serif">TruthScore</h1>
        </div>
        <div className="flex flex-col items-center gap-2 p-4 rounded-lg bg-muted">
            <img src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fDE?q=80&w=1780&auto=format&fit=crop" alt="Linda Stewart" className="w-20 h-20 rounded-full object-cover" />
            <p className="font-semibold">Linda Stewart</p>
            <p className="text-sm text-muted-foreground">@linda.23</p>
        </div>

        {/* Upload Link to Verify Component */}
        <Card className="mt-4">
            <CardHeader className="p-3">
                <CardTitle className="text-sm font-medium">Upload Link to Verify</CardTitle>
            </CardHeader>
            <CardContent className="p-3 pt-0 space-y-3">
                <Input
                    placeholder="Paste article URL here..."
                    className="text-sm"
                    value={articleUrl}
                    onChange={(e) => setArticleUrl(e.target.value)}
                    onKeyPress={(e) => handleKeyPress(e, handleUrlVerification)}
                    disabled={isVerifying}
                />
                <Button
                    className="w-full"
                    size="sm"
                    onClick={handleUrlVerification}
                    disabled={isVerifying || !articleUrl.trim()}
                >
                    {isVerifying ? (
                        <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Verifying...
                        </>
                    ) : (
                        'Verify Article'
                    )}
                </Button>
            </CardContent>
        </Card>

        <nav className="flex flex-col gap-1 py-4">
          <Button variant="ghost" className="justify-start gap-2 text-primary bg-primary/10"><LayoutDashboard /> Dashboard</Button>
          <Button variant="ghost" className="justify-start gap-2" asChild>
            <Link to="/profile"><User /> My Profile</Link>
          </Button>
          <Button variant="ghost" className="justify-start gap-2" asChild>
            <Link to="/debates"><Newspaper /> Debate Rooms</Link>
          </Button>
          <Button variant="ghost" className="justify-start gap-2"><Settings /> Settings</Button>
        </nav>

        <Card className="mt-4">
            <CardHeader className="p-4">
                <CardTitle className="text-base flex justify-between items-center">Recent Messages <Button variant="ghost" size="sm">View All</Button></CardTitle>
            </CardHeader>
            <CardContent className="p-4 pt-0 text-sm space-y-3">
                <div className="p-2 rounded-md bg-blue-100/50 text-blue-800">Alice: "I found conflicting data about this claim..." <span className="text-xs opacity-70 block">Sports Debate • 15 min. ago</span></div>
                <div className="p-2 rounded-md bg-green-100/50 text-green-800">Bob: "Can we verify this source?" <span className="text-xs opacity-70 block">Space Debate • 28 min. ago</span></div>
                <div className="p-2 rounded-md bg-purple-100/50 text-purple-800">Carol: "This article needs fact-checking" <span className="text-xs opacity-70 block">Sports Debate • 45 min. ago</span></div>
            </CardContent>
        </Card>

        <div className="mt-auto">
            <Button variant="ghost" className="justify-start gap-2 w-full"><LogOut /> Log Out</Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex flex-col flex-1 overflow-y-auto p-6 gap-6">
        <header className="space-y-2">
            <div className="flex items-center justify-between">
                <h2 className="text-3xl font-bold font-serif">Reality Unveiled...</h2>

                {/* Our Socials Component */}
                <div className="flex items-center gap-3">
                    <span className="text-sm font-medium text-muted-foreground">Our Socials</span>
                    <div className="flex items-center gap-2">
                        <Button variant="ghost" size="icon" className="h-8 w-8" asChild>
                            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer">
                                <Instagram className="h-4 w-4" />
                            </a>
                        </Button>
                        <Button variant="ghost" size="icon" className="h-8 w-8" asChild>
                            <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">
                                <Twitter className="h-4 w-4" />
                            </a>
                        </Button>
                        <Button variant="ghost" size="icon" className="h-8 w-8" asChild>
                            <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">
                                <Facebook className="h-4 w-4" />
                            </a>
                        </Button>
                    </div>
                </div>
            </div>

            <Link to={`/article/breaking-${currentHeadlineIndex + 1}`}>
                <div className="p-6 rounded-lg bg-black text-white flex flex-col justify-center items-center hover:bg-gray-900 transition-colors cursor-pointer">
                    <p className="font-bold text-sm text-red-400 mb-2">🔴 BREAKING NEWS</p>
                    <p className="font-semibold text-lg text-center leading-tight transition-all duration-500">
                        {breakingNewsHeadlines[currentHeadlineIndex]}
                    </p>
                </div>
            </Link>
        </header>

        <div className="flex items-center gap-4">
            <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                    placeholder="Search headlines to verify..."
                    className="pl-9"
                    value={searchText}
                    onChange={(e) => setSearchText(e.target.value)}
                    onKeyPress={(e) => handleKeyPress(e, handleSearchVerification)}
                    disabled={isVerifying}
                />
            </div>
            <Button
                variant="default"
                size="sm"
                onClick={handleSearchVerification}
                disabled={isVerifying || !searchText.trim()}
            >
                {isVerifying ? (
                    <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Verifying...
                    </>
                ) : (
                    'Verify Claim'
                )}
            </Button>
            <div className="flex items-center gap-2">
                <Button variant="outline" size="sm">Country: Canada</Button>
                <Button variant="outline" size="sm">Category: Sports</Button>
                <Button variant="outline" size="sm">Arrange by: Oldest</Button>
            </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {articles.map((article, index) => (
            <Link key={article.id} to={`/article/${article.id}`} className="block">
              <Card className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer">
                  <div className="relative">
                      <img src={article.imageUrl} alt={article.title} className="w-full h-48 object-cover"/>
                      <div className="absolute top-4 right-4 bg-primary/80 text-primary-foreground px-2 py-1 rounded-md text-sm font-semibold">{article.category}</div>
                  </div>
                <CardHeader className="flex flex-row items-center gap-3">
                  <img src={article.avatarUrl} alt={article.author} className="w-10 h-10 rounded-full object-cover" />
                  <div>
                    <CardTitle className="text-base">{article.author}</CardTitle>
                    <CardDescription>{article.handle}</CardDescription>
                  </div>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="font-semibold text-foreground">{article.title}</p>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <div className="flex items-center gap-1"><Star className="w-4 h-4 text-yellow-500 fill-yellow-400"/> {article.stars}</div>
                      <div className="flex items-center gap-1"><Eye className="w-4 h-4"/> {article.views}</div>
                      <div className="flex items-center gap-1"><MessageSquare className="w-4 h-4"/> {article.comments}</div>
                      <span>{article.date}</span>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
        <Card>
            <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle className="font-serif">Sports</CardTitle>
                <Button variant="ghost" size="sm" className="gap-1">View All <ArrowRight className="w-4 h-4" /></Button>
            </CardHeader>
            <CardContent>
                <img src="https://images.unsplash.com/photo-1560272564-c83b66b1ad12?q=80&w=1949&auto=format&fit=crop" className="w-full h-64 object-cover rounded-lg" alt="Sports image" />
            </CardContent>
        </Card>
      </main>

      {/* Right Sidebar */}
      <aside className="flex flex-col gap-6 border-l bg-background p-6">
        <Card>
            <CardHeader>
                <CardTitle className="font-serif text-lg">Statistics</CardTitle>
            </CardHeader>
            <CardContent>
                <StatisticsChart data={chartData} />
            </CardContent>
        </Card>
        <Card>
            <CardHeader>
                <CardTitle className="font-serif text-lg">Suggested News Channels</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-red-600 flex items-center justify-center">
                            <span className="text-white font-bold text-xs">BBC</span>
                        </div>
                        <div>
                            <p className="font-semibold">BBC News</p>
                            <p className="text-sm text-muted-foreground">Verified • 45M followers</p>
                        </div>
                    </div>
                    <Button size="sm">Follow</Button>
                </div>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center">
                            <span className="text-white font-bold text-xs">CNN</span>
                        </div>
                        <div>
                            <p className="font-semibold">CNN</p>
                            <p className="text-sm text-muted-foreground">Verified • 32M followers</p>
                        </div>
                    </div>
                    <Button size="sm">Follow</Button>
                </div>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-orange-600 flex items-center justify-center">
                            <span className="text-white font-bold text-xs">RT</span>
                        </div>
                        <div>
                            <p className="font-semibold">Reuters</p>
                            <p className="text-sm text-muted-foreground">Verified • 28M followers</p>
                        </div>
                    </div>
                    <Button size="sm">Follow</Button>
                </div>
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-lg bg-gray-800 flex items-center justify-center">
                            <span className="text-white font-bold text-xs">AP</span>
                        </div>
                        <div>
                            <p className="font-semibold">Associated Press</p>
                            <p className="text-sm text-muted-foreground">Verified • 22M followers</p>
                        </div>
                    </div>
                    <Button size="sm">Follow</Button>
                </div>
            </CardContent>
        </Card>
      </aside>
    </div>
  );
};

export default Index;
