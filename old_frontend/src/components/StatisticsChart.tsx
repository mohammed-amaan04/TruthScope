import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface ChartData {
  name: string;
  Followers: number;
  Likes: number;
  Views: number;
}

interface StatisticsChartProps {
  data: ChartData[];
}

const StatisticsChart: React.FC<StatisticsChartProps> = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <LineChart
        data={data}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="Followers" stroke="#8884d8" strokeWidth={2} />
        <Line type="monotone" dataKey="Likes" stroke="#82ca9d" strokeWidth={2} />
        <Line type="monotone" dataKey="Views" stroke="#ffc658" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default StatisticsChart;
