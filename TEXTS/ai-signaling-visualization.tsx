import React from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  LineChart, Line, PieChart, Pie, Cell, RadarChart, PolarGrid, PolarAngleAxis, 
  PolarRadiusAxis, Radar, ComposedChart, Scatter, ScatterChart, ZAxis
} from 'recharts';

const AiSignalingVisualization = () => {
  // Data from our analysis
  const timelineData = [
    {year: 2017, tyingHands: 0, sunkCosts: 0, installmentCosts: 0, reducibleCosts: 2},
    {year: 2018, tyingHands: 0, sunkCosts: 1, installmentCosts: 0, reducibleCosts: 2},
    {year: 2019, tyingHands: 0, sunkCosts: 0, installmentCosts: 0, reducibleCosts: 3},
    {year: 2020, tyingHands: 0, sunkCosts: 0, installmentCosts: 0, reducibleCosts: 1},
    {year: 2021, tyingHands: 0, sunkCosts: 1, installmentCosts: 0, reducibleCosts: 2},
    {year: 2022, tyingHands: 1, sunkCosts: 1, installmentCosts: 0, reducibleCosts: 1},
    {year: 2023, tyingHands: 0, sunkCosts: 1, installmentCosts: 0, reducibleCosts: 1},
    {year: 2025, tyingHands: 4, sunkCosts: 0, installmentCosts: 0, reducibleCosts: 0}
  ];

  const fundingData = [
    {type: "Tying Hands", funding: 0, percentage: 0, description: "Public commitments and policy statements"},
    {type: "Sunk Costs", funding: 101.16, percentage: 66.67, description: "Large upfront investments in infrastructure"},
    {type: "Installment Costs", funding: 0, percentage: 0, description: "Future verification commitments"},
    {type: "Reducible Costs", funding: 50.57, percentage: 33.33, description: "Research investments with potential returns"}
  ];

  const regionData = [
    {region: "North America", tyingHands: 3, sunkCosts: 1, installmentCosts: 0, reducibleCosts: 1, totalSignals: 5, totalFunding: 53.14},
    {region: "Europe", tyingHands: 1, sunkCosts: 1, installmentCosts: 0, reducibleCosts: 3, totalSignals: 5, totalFunding: 57.52},
    {region: "Asia", tyingHands: 1, sunkCosts: 1, installmentCosts: 0, reducibleCosts: 4, totalSignals: 6, totalFunding: 13.18},
    {region: "Middle East", tyingHands: 0, sunkCosts: 1, installmentCosts: 0, reducibleCosts: 2, totalSignals: 3, totalFunding: 21.70},
    {region: "Oceania", tyingHands: 0, sunkCosts: 0, installmentCosts: 0, reducibleCosts: 1, totalSignals: 1, totalFunding: 0.08},
    {region: "Eurasia", tyingHands: 0, sunkCosts: 0, installmentCosts: 0, reducibleCosts: 1, totalSignals: 1, totalFunding: 6.10}
  ];

  const strategicData = [
    {approach: "Hardware Control", tyingHands: 0, sunkCosts: 1, installmentCosts: 0, reducibleCosts: 0, total: 1},
    {approach: "Research Excellence", tyingHands: 0, sunkCosts: 0, installmentCosts: 0, reducibleCosts: 1, total: 1},
    {approach: "Defense Applications", tyingHands: 0, sunkCosts: 0, installmentCosts: 0, reducibleCosts: 1, total: 1},
    {approach: "Economic Transformation", tyingHands: 0, sunkCosts: 0, installmentCosts: 0, reducibleCosts: 0, total: 0},
    {approach: "Regulatory Frameworks", tyingHands: 5, sunkCosts: 0, installmentCosts: 0, reducibleCosts: 0, total: 5}
  ];

  const examplePrograms = {
    tyingHands: [
      {country: "USA", policyName: "Framework for AI Diffusion", year: 2025, fundingUSD: null, strategicFocus: "Control of AI capabilities"},
      {country: "USA", policyName: "EAR Control of Model Weights", year: 2025, fundingUSD: null, strategicFocus: "Control of AI model distribution"},
      {country: "USA", policyName: "Foreign Direct Product Rule for AI", year: 2025, fundingUSD: null, strategicFocus: "Global AI governance"}
    ],
    sunkCosts: [
      {country: "USA", policyName: "CHIPS Act", year: 2022, fundingUSD: 52700000000, strategicFocus: "Hardware-first approach with regulatory framework"},
      {country: "European Union", policyName: "