import React, { useCallback, useState } from "react";
import { PieChart, Pie, Cell } from "recharts";

const COLORS = [
	"#0088FE",
	"#00C49F",
	"#FFBB28",
	"#FF8042",
	"#9376E0",
	"#068DA9",
];

const RADIAN = Math.PI / 180;
const renderCustomizedLabel = ({
	cx,
	cy,
	midAngle,
	innerRadius,
	outerRadius,
	percent,
	name,
	index,
}) => {
	const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
	const x = cx + radius * Math.cos(-midAngle * RADIAN);
	const y = cy + radius * Math.sin(-midAngle * RADIAN);

	return (
		<text
			x={x}
			y={y}
			fill="white"
			textAnchor={x > cx ? "start" : "end"}
			dominantBaseline="central">
			<tspan x={x} dy="-0.5em" textAnchor="middle">
				{name}
			</tspan>{" "}
			<tspan x={x} dy="1.5em" fontSize="12" textAnchor="middle">
				{`${(percent * 100).toFixed(0)}%`}
			</tspan>
		</text>
	);
};
export default function App(records) {
	const data = Object.entries(records.records).map(([key, value]) => ({
		name: key,
		value: value,
	}));
	return (
		<PieChart width={400} height={400}>
			<Pie
				data={data}
				cx={200}
				cy={200}
				labelLine={false}
				label={renderCustomizedLabel}
				outerRadius={160}
				fill="#8884d8"
				dataKey="value">
				{data.map((entry, index) => (
					<Cell
						key={`cell-${index}`}
						fill={COLORS[index % COLORS.length]}
					/>
				))}
			</Pie>
		</PieChart>
	);
}
