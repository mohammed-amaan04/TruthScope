import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { 
  Newspaper, 
  User, 
  Settings, 
  LogOut, 
  LayoutDashboard, 
  Edit3, 
  Camera, 
  Save, 
  X,
  Mail,
  Calendar,
  MapPin,
  Link as LinkIcon,
  Shield,
  Award,
  Users,
  FileText
} from "lucide-react";

// Mock user data
const initialUserData = {
  name: "Linda Stewart",
  username: "linda.23",
  email: "linda.stewart@example.com",
  bio: "News verification specialist and fact-checker. Passionate about combating misinformation and promoting media literacy. 5+ years experience in journalism and digital content verification.",
  profileImage: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fDE?q=80&w=1780&auto=format&fit=crop",
  joinDate: "March 2019",
  location: "Toronto, Canada",
  website: "https://lindastewart.com",
  verificationLevel: "Expert",
  articlesVerified: 1247,
  followers: 2834,
  following: 892
};

const Profile = () => {
  const [userData, setUserData] = useState(initialUserData);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState(initialUserData);

  const handleEdit = () => {
    setIsEditing(true);
    setEditData(userData);
  };

  const handleSave = () => {
    setUserData(editData);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditData(userData);
    setIsEditing(false);
  };

  const handleInputChange = (field: string, value: string) => {
    setEditData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  return (
    <div className="grid grid-cols-[260px_1fr_300px] min-h-screen w-full font-sans bg-muted/40">
      {/* Left Sidebar */}
      <aside className="flex flex-col border-r bg-background p-4">
        <div className="flex items-center gap-2 p-2 pb-4">
          <Newspaper className="h-6 w-6" />
          <h1 className="font-semibold text-xl font-serif">Info Flow</h1>
        </div>
        <div className="flex flex-col items-center gap-2 p-4 rounded-lg bg-muted">
          <img src={userData.profileImage} alt={userData.name} className="w-20 h-20 rounded-full object-cover" />
          <p className="font-semibold">{userData.name}</p>
          <p className="text-sm text-muted-foreground">@{userData.username}</p>
        </div>
        <nav className="flex flex-col gap-1 py-4">
          <Button variant="ghost" className="justify-start gap-2" asChild>
            <Link to="/"><LayoutDashboard /> Dashboard</Link>
          </Button>
          <Button variant="ghost" className="justify-start gap-2 text-primary bg-primary/10"><User /> My Profile</Button>
          <Button variant="ghost" className="justify-start gap-2"><Newspaper /> Article Feed</Button>
          <Button variant="ghost" className="justify-start gap-2"><Settings /> Settings</Button>
        </nav>
        <div className="mt-auto">
          <Button variant="ghost" className="justify-start gap-2 w-full"><LogOut /> Log Out</Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex flex-col flex-1 overflow-y-auto p-6 gap-6">
        <header className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold font-serif">My Profile</h2>
            <p className="text-muted-foreground">Manage your account information and preferences</p>
          </div>
          {!isEditing ? (
            <Button onClick={handleEdit} className="gap-2">
              <Edit3 className="w-4 h-4" />
              Edit Profile
            </Button>
          ) : (
            <div className="flex gap-2">
              <Button onClick={handleSave} className="gap-2">
                <Save className="w-4 h-4" />
                Save Changes
              </Button>
              <Button variant="outline" onClick={handleCancel} className="gap-2">
                <X className="w-4 h-4" />
                Cancel
              </Button>
            </div>
          )}
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Profile Picture and Basic Info */}
          <Card className="lg:col-span-1">
            <CardHeader>
              <CardTitle>Profile Picture</CardTitle>
              <CardDescription>Update your profile photo</CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col items-center gap-4">
              <div className="relative">
                <Avatar className="w-32 h-32">
                  <AvatarImage src={isEditing ? editData.profileImage : userData.profileImage} />
                  <AvatarFallback className="text-2xl">
                    {userData.name.split(' ').map(n => n[0]).join('')}
                  </AvatarFallback>
                </Avatar>
                {isEditing && (
                  <Button size="icon" className="absolute bottom-0 right-0 rounded-full w-8 h-8">
                    <Camera className="w-4 h-4" />
                  </Button>
                )}
              </div>
              <div className="text-center">
                <h3 className="font-semibold text-lg">{userData.name}</h3>
                <p className="text-muted-foreground">@{userData.username}</p>
                <div className="flex items-center gap-1 mt-2">
                  <Shield className="w-4 h-4 text-green-600" />
                  <span className="text-sm text-green-600 font-medium">{userData.verificationLevel} Verifier</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Personal Information */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle>Personal Information</CardTitle>
              <CardDescription>Your account details and contact information</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Full Name</Label>
                  {isEditing ? (
                    <Input
                      id="name"
                      value={editData.name}
                      onChange={(e) => handleInputChange('name', e.target.value)}
                    />
                  ) : (
                    <div className="flex items-center gap-2 p-2 border rounded-md bg-muted/50">
                      <User className="w-4 h-4 text-muted-foreground" />
                      <span>{userData.name}</span>
                    </div>
                  )}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="username">Username</Label>
                  {isEditing ? (
                    <Input
                      id="username"
                      value={editData.username}
                      onChange={(e) => handleInputChange('username', e.target.value)}
                    />
                  ) : (
                    <div className="flex items-center gap-2 p-2 border rounded-md bg-muted/50">
                      <span>@{userData.username}</span>
                    </div>
                  )}
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="email">Email Address</Label>
                {isEditing ? (
                  <Input
                    id="email"
                    type="email"
                    value={editData.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                  />
                ) : (
                  <div className="flex items-center gap-2 p-2 border rounded-md bg-muted/50">
                    <Mail className="w-4 h-4 text-muted-foreground" />
                    <span>{userData.email}</span>
                  </div>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="location">Location</Label>
                  {isEditing ? (
                    <Input
                      id="location"
                      value={editData.location}
                      onChange={(e) => handleInputChange('location', e.target.value)}
                    />
                  ) : (
                    <div className="flex items-center gap-2 p-2 border rounded-md bg-muted/50">
                      <MapPin className="w-4 h-4 text-muted-foreground" />
                      <span>{userData.location}</span>
                    </div>
                  )}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="website">Website</Label>
                  {isEditing ? (
                    <Input
                      id="website"
                      value={editData.website}
                      onChange={(e) => handleInputChange('website', e.target.value)}
                    />
                  ) : (
                    <div className="flex items-center gap-2 p-2 border rounded-md bg-muted/50">
                      <LinkIcon className="w-4 h-4 text-muted-foreground" />
                      <span className="text-blue-600 hover:underline cursor-pointer">{userData.website}</span>
                    </div>
                  )}
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="bio">Bio</Label>
                {isEditing ? (
                  <Textarea
                    id="bio"
                    value={editData.bio}
                    onChange={(e) => handleInputChange('bio', e.target.value)}
                    rows={4}
                    placeholder="Tell us about yourself..."
                  />
                ) : (
                  <div className="p-3 border rounded-md bg-muted/50">
                    <p className="text-sm leading-relaxed">{userData.bio}</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Account Statistics */}
        <Card>
          <CardHeader>
            <CardTitle>Account Statistics</CardTitle>
            <CardDescription>Your activity and verification metrics</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 border rounded-lg">
                <FileText className="w-8 h-8 mx-auto mb-2 text-blue-600" />
                <div className="text-2xl font-bold">{userData.articlesVerified.toLocaleString()}</div>
                <div className="text-sm text-muted-foreground">Articles Verified</div>
              </div>
              <div className="text-center p-4 border rounded-lg">
                <Users className="w-8 h-8 mx-auto mb-2 text-green-600" />
                <div className="text-2xl font-bold">{userData.followers.toLocaleString()}</div>
                <div className="text-sm text-muted-foreground">Followers</div>
              </div>
              <div className="text-center p-4 border rounded-lg">
                <Users className="w-8 h-8 mx-auto mb-2 text-purple-600" />
                <div className="text-2xl font-bold">{userData.following.toLocaleString()}</div>
                <div className="text-sm text-muted-foreground">Following</div>
              </div>
              <div className="text-center p-4 border rounded-lg">
                <Award className="w-8 h-8 mx-auto mb-2 text-yellow-600" />
                <div className="text-2xl font-bold">{userData.verificationLevel}</div>
                <div className="text-sm text-muted-foreground">Verification Level</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Account Information */}
        <Card>
          <CardHeader>
            <CardTitle>Account Information</CardTitle>
            <CardDescription>Additional account details</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Calendar className="w-4 h-4" />
              <span>Member since {userData.joinDate}</span>
            </div>
          </CardContent>
        </Card>
      </main>

      {/* Right Sidebar - Profile Stats */}
      <aside className="flex flex-col gap-6 border-l bg-background p-6">
        <Card>
          <CardHeader>
            <CardTitle className="font-serif text-lg">Quick Stats</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-sm">Accuracy Rate</span>
              <span className="font-semibold text-green-600">98.5%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Response Time</span>
              <span className="font-semibold">2.3 hrs</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm">Trust Score</span>
              <span className="font-semibold text-blue-600">9.2/10</span>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="font-serif text-lg">Recent Activity</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            <div className="p-2 rounded-md bg-green-100/50 text-green-800">
              Verified article about climate change
              <span className="text-xs opacity-70 block">2 hours ago</span>
            </div>
            <div className="p-2 rounded-md bg-yellow-100/50 text-yellow-800">
              Flagged misleading headline
              <span className="text-xs opacity-70 block">5 hours ago</span>
            </div>
            <div className="p-2 rounded-md bg-blue-100/50 text-blue-800">
              Updated fact-check database
              <span className="text-xs opacity-70 block">1 day ago</span>
            </div>
          </CardContent>
        </Card>
      </aside>
    </div>
  );
};

export default Profile;
