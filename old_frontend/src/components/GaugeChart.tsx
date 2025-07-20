import React from 'react';

interface GaugeChartProps {
  value: number; // 0-100
  label: string;
}

const GaugeChart: React.FC<GaugeChartProps> = ({ value, label }) => {
  // Ensure value is between 0 and 100
  const clampedValue = Math.max(0, Math.min(100, value));
  
  // Calculate the rotation angle for the needle (180 degrees total)
  const needleAngle = (clampedValue / 100) * 180 - 90;
  
  // Determine color based on value
  const getColor = (val: number) => {
    if (val >= 70) return '#22c55e'; // green
    if (val >= 40) return '#eab308'; // yellow
    return '#ef4444'; // red
  };

  const color = getColor(clampedValue);
  
  // Create gradient stops for the arc
  const gradientId = `gauge-gradient-${label.replace(/\s+/g, '-').toLowerCase()}`;

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative w-32 h-16">
        <svg
          width="128"
          height="64"
          viewBox="0 0 128 64"
          className="overflow-visible"
        >
          {/* Define gradient */}
          <defs>
            <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#ef4444" />
              <stop offset="50%" stopColor="#eab308" />
              <stop offset="100%" stopColor="#22c55e" />
            </linearGradient>
          </defs>
          
          {/* Background arc */}
          <path
            d="M 16 48 A 32 32 0 0 1 112 48"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="8"
            strokeLinecap="round"
          />
          
          {/* Progress arc */}
          <path
            d="M 16 48 A 32 32 0 0 1 112 48"
            fill="none"
            stroke={`url(#${gradientId})`}
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={`${(clampedValue / 100) * 150.8} 150.8`}
          />
          
          {/* Center dot */}
          <circle
            cx="64"
            cy="48"
            r="4"
            fill="#374151"
          />
          
          {/* Needle */}
          <line
            x1="64"
            y1="48"
            x2="64"
            y2="20"
            stroke="#374151"
            strokeWidth="2"
            strokeLinecap="round"
            transform={`rotate(${needleAngle} 64 48)`}
          />
        </svg>
      </div>
      
      {/* Value display */}
      <div className="text-center">
        <div className="text-2xl font-bold" style={{ color }}>
          {clampedValue}%
        </div>
        <div className="text-sm text-muted-foreground font-medium">
          {label}
        </div>
      </div>
    </div>
  );
};

export default GaugeChart;
