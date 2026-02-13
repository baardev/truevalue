# Frontend Visualization Strategy
**Gold Supply Chain Intelligence Platform**

---

## Overview

This document outlines the visualization and interaction strategy for the JavaScript-driven frontend, designed to maximize user understanding of **balance** and **sustainability** in the gold supply chain through the Tholonic N-D-C framework.

---

## Core Principle

> **"When balance and sustainability are optimal, the process is most efficient and therefore long-term more profitable."**

All visualizations are designed to make this relationship immediately visible and actionable.

---

## Visualization Types

### 1. **Main Dashboard** (`dashboard.html`)

**Purpose**: System health overview at a glance

**Key Components**:

#### A. Score Cards (Top Level KPIs)
- **System Balance** (0-100 scale) - Average D-C balance across all phases
- **Sustainability Index** - System-wide energy efficiency
- **Bottleneck Count** - Number of critically imbalanced phases
- **System Health** - Composite indicator with trend arrow

**Visual Design**:
- Color-coded by health: Green (good), Yellow (fair), Red (poor)
- Progress bars for quick visual scanning
- Trend indicators (↗️ improving, ↘️ declining)

#### B. Supply Chain Flow Diagram
- **Horizontal flow** showing all 8 phases in sequence
- **Color-coded boxes** representing phase health:
  - Excellent (95-100): Green gradient
  - Good (80-95): Teal gradient
  - Fair (60-80): Orange gradient
  - Poor (<60): Red gradient
- **Size of connecting arrows** proportional to N-value (flow capacity)
- **Arrow color** indicates health of upstream phase
- **Click any phase** → Modal with detailed D-C breakdown

**Why This Works**:
- Immediate identification of bottlenecks
- Visual flow mimics physical gold movement
- Color consistency across all views

#### C. Balance Trend Chart
- **Line graph** showing 90-day rolling average of system balance
- **Target line** at optimal balance (e.g., 80)
- **Shaded regions** indicating good/fair/poor zones
- Shows directional trend: Is balance improving?

#### D. Optimization Recommendations
- **Priority-sorted list** of actionable improvements
- Each recommendation shows:
  - **Priority level** (Critical/High/Medium)
  - **Affected phase**
  - **Current imbalance magnitude**
  - **Expected impact** (percentage improvement)
- Click to see detailed optimization strategy

**Interaction Model**:
- Dashboard is **read-only** and **real-time**
- Auto-refreshes or updates via WebSocket
- Click "What-If Simulator" button to test changes

---

### 2. **What-If Simulator** (`what_if_simulator.html`)

**Purpose**: Interactive exploration of D-C parameter changes

**Key Components**:

#### A. Phase Control Panel (Left Sidebar)
- **Dual sliders** for each phase:
  - **D slider** (red gradient) - Constraints, definitions, capacity
  - **C slider** (blue gradient) - Connections, relationships, integration
- **Real-time metric display**:
  - Balance score (0-100)
  - N-state (calculated from √(D×C) × balance)
- **Status indicator** per phase (Good/Fair/Poor)

**Interaction**:
- Adjust any slider → **Instant recalculation** of all metrics
- See immediate impact on system-wide balance
- **Scenario dropdown** for quick presets:
  - "Auto-Optimize All" → Balance all D-C pairs
  - "Fix Phase 6 Bottleneck" → Apply recommended fix
  - "Simulate Supply Shock" → Reduce Phase 2 capacity by 40%
  - "10% Capacity Expansion" → Scale all D-C by 1.1x

#### B. Live Impact Visualization (Center)
- **Top Metrics Row**:
  - System Balance with delta from baseline
  - Sustainability with delta
  - Bottleneck count with delta
  - **Annual Profit** with projected gain/loss

- **Flow Network Graph**:
  - All 8 phases as **nodes** (circles or rectangles)
  - Nodes color-coded by balance score
  - Nodes display current balance score + N-value
  - **Connecting edges** show:
    - Thickness → Flow capacity (N-value)
    - Color → Health (green/yellow/red)
  - **Real-time updates** as sliders move

**Why This Works**:
- Users see **cause and effect** immediately
- Visual feedback reinforces D-C balance concept
- Network view shows **cascade effects** (one phase affecting others)

#### C. Impact Analysis Panel (Right Sidebar)
- **Detected Issues**:
  - Lists all phases with balance < 70
  - Shows whether over-constrained (D > C) or under-integrated (C > D)
  - Color-coded by severity

- **Financial Impact Calculator**:
  - Current annual profit (baseline)
  - **Projected profit** with current slider settings
  - **Annual gain** in dollars
  - Simple profit model: `Profit ∝ Balance × Sustainability`

- **Sustainability Metrics**:
  - **Energy Efficiency** (inversely proportional to imbalance²)
  - **System Resilience** (number of phases above threshold)
  - **Long-term Viability** (weighted balance score)
  - Each with progress bar

**Interaction**:
- **"Apply Changes"** button → Would update backend
- **"Reset"** button → Restore baseline
- **"Auto-Optimize"** button → Calculate optimal D-C for all phases

---

## Visual Design Language

### Color Palette

| Element | Color | Meaning |
|---------|-------|---------|
| **D (Definition)** | Red (#dc3545) | Constraints, boundaries, limits |
| **C (Contribution)** | Blue (#17a2b8) | Connections, flow, integration |
| **N (Negotiation)** | Purple (#667eea) | Emergent state, balance |
| **Excellent** | Green (#28a745) | Balance 95-100 |
| **Good** | Teal (#20c997) | Balance 80-94 |
| **Fair** | Orange (#ffc107) | Balance 60-79 |
| **Poor** | Red (#dc3545) | Balance <60 |

### Typography
- **Headers**: Segoe UI, 24px, weight 300 (light, modern)
- **Metrics**: Bold, large (28-32px) for scannability
- **Labels**: 11-12px, uppercase, letter-spacing for hierarchy

### Layout Principles
- **3-column layout** for What-If Simulator:
  - Left: Input controls
  - Center: Visualization (largest area)
  - Right: Analysis & feedback
- **Card-based design** for Dashboard:
  - White cards on subtle gradient background
  - Consistent shadows for depth
  - Hover effects for interactivity

---

## Data Flow Architecture

### Frontend ← → Backend Communication

```
┌─────────────────────────────────────────────────────────┐
│                    JavaScript Frontend                   │
│  (HTML/CSS/Vanilla JS - No framework dependencies)      │
└─────────────────────────────────────────────────────────┘
                           ↕️
                    REST API / WebSocket
                           ↕️
┌─────────────────────────────────────────────────────────┐
│                    Python Backend                        │
│  - src/api/generate_frontend_data.py                    │
│  - src/simulation/tholonic_engine.py                    │
│  - data/processed/*.csv                                 │
└─────────────────────────────────────────────────────────┘
```

### API Endpoints (Proposed)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/system/status` | GET | Current system-wide metrics |
| `/api/phases` | GET | All phase data with D, C, N, balance |
| `/api/phases/{id}` | GET | Single phase details |
| `/api/simulate` | POST | Run what-if simulation |
| `/api/optimize` | POST | Calculate optimal D-C values |
| `/api/recommendations` | GET | Prioritized improvement list |

### Data Format

**Example Phase Object**:
```json
{
  "phase_id": 6,
  "phase_name": "Logistics & Vaulting",
  "d_value": 204,
  "c_value": 161,
  "n_value": 118,
  "balance_score": 65.5,
  "sustainability_index": 0.05,
  "transparency": "Low-Medium",
  "status": "Poor",
  "recommendation": "Increase C by 34 points to reach 78% balance"
}
```

---

## Interaction Patterns

### 1. **Progressive Disclosure**
- Dashboard shows high-level overview
- Click phase → Modal with details
- "See What-If Analysis" → Full simulator

### 2. **Real-Time Feedback**
- Slider changes → Instant recalculation (<100ms)
- Visual updates → Smooth transitions (CSS animations)
- No page reloads, all AJAX

### 3. **Guided Optimization**
- System suggests fixes: "Increase C by 34"
- One-click "Apply Recommendation" buttons
- "Auto-Optimize" for full system balance

### 4. **Scenario Comparison**
- Save current state as "Scenario A"
- Make changes → "Scenario B"
- Side-by-side comparison view (future enhancement)

---

## Key Metrics Explained for Users

The frontend includes an **"Understanding the Metrics"** help panel:

### Balance Score (0-100)
> Measures how close D and C are to equilibrium.  
> Formula: `100 × e^(-2 × |D-C| / max(D,C))`  
> **Goal**: Keep above 80 for optimal efficiency

### N-State (Negotiated/Observable State)
> The emergent capacity of a phase.  
> Formula: `√(D × C) × (balance / 100)`  
> **Interpretation**: Higher N = More gold can flow through this phase

### Sustainability Index
> Energy efficiency of the phase.  
> Formula: `100 / (|D-C|² + 10)`  
> **Goal**: Minimize energy waste by balancing D-C

### System Health
> Composite score combining:
> - Average balance across phases
> - Number of bottlenecks
> - Sustainability trend
> **Status**: Excellent / Good / Fair / Poor

---

## Why This Visualization Strategy Works

### 1. **Immediate Visual Feedback**
- Color coding is universal (red = bad, green = good)
- Size/thickness conveys magnitude
- Position in flow shows sequence

### 2. **Actionable Insights**
- Not just "here's the data" but "do this to improve"
- Recommendations are prioritized and specific
- Impact is quantified (e.g., "+18% efficiency")

### 3. **Intuitive Mental Model**
- Flow diagram mimics physical supply chain
- Sliders are familiar interaction pattern
- Balance is visualized as D vs C bars (easy comparison)

### 4. **Supports Decision-Making**
- "What if we increase vault capacity?" → Immediate answer
- "Which phase should we fix first?" → Sorted recommendations
- "What's the ROI of this change?" → Financial impact calculator

### 5. **Aligns with Tholonic Theory**
- D and C are visually distinct (red vs blue)
- N emerges from their interaction (purple)
- Balance is the core metric, not just throughput
- Sustainability is explicitly calculated and displayed

---

## Future Enhancements

### Phase 2: Advanced Visualizations
- **Sankey diagram** for material flow with loss at each phase
- **Heatmap** showing balance scores over time
- **3D network graph** for complex interdependencies

### Phase 3: Predictive Analytics
- **Trend forecasting**: "If Phase 6 continues, expect bottleneck in 14 days"
- **Monte Carlo simulation**: Run 1000 scenarios, show probability distribution
- **Machine learning**: Suggest optimal D-C values based on historical data

### Phase 4: Collaborative Features
- Multi-user editing with conflict resolution
- Comment threads on specific phases
- Version control for scenarios

---

## Technical Implementation Notes

### Frontend Stack
- **Pure JavaScript** (no framework dependencies for simplicity)
- **D3.js** for advanced SVG visualizations (network graphs)
- **Chart.js** for line/bar charts (balance trends)
- **Vanilla CSS** with CSS Grid + Flexbox (no preprocessor)

### Performance Considerations
- Debounce slider input (update every 50ms max)
- Use `requestAnimationFrame` for smooth animations
- Cache calculation results where possible
- WebSocket for real-time dashboard updates (optional)

### Accessibility
- ARIA labels on all interactive elements
- Keyboard navigation support (tab through sliders)
- Color + icon + text for status (not color alone)
- High contrast mode support

### Mobile Responsiveness
- Stacked layout on mobile (panels become vertical)
- Touch-friendly slider targets (48px min)
- Simplified flow diagram (1-2 phases per row)

---

## Testing the Mockups

**Local Testing** (no server required):
1. Navigate to `frontend/supply_chain/` (formerly `frontend/mockups/`)
2. Open `dashboard.html` in any modern browser
3. Click phase boxes to see details
4. Click "What-If Simulator" button (link to `what_if_simulator.html`)

**Interactive Testing**:
- In `what_if_simulator.html`:
  - Move D and C sliders for any phase
  - Watch metrics update in real-time
  - Try "Auto-Optimize" button
  - Select different scenarios from dropdown

**Data Binding** (next step):
- Replace hardcoded JS data with `fetch()` calls to backend API
- Update `generate_frontend_data.py` to serve JSON
- Implement WebSocket for live updates

---

## Summary: The "Why" Behind Each Visualization

| Visualization | Purpose | Answers This Question |
|---------------|---------|------------------------|
| **Score Cards** | Quick health check | "Is the system okay right now?" |
| **Flow Diagram** | Identify bottlenecks | "Where is the problem?" |
| **Trend Chart** | Track improvement | "Are we getting better over time?" |
| **Recommendations** | Guide action | "What should I do first?" |
| **Sliders** | Explore scenarios | "What happens if I change X?" |
| **Impact Panel** | Justify decisions | "What's the ROI of this change?" |
| **Network Graph** | Understand dependencies | "How do phases affect each other?" |
| **Financial Calculator** | Business case | "Will this make us money?" |

---

## Conclusion

This frontend visualization strategy transforms complex N-D-C supply chain data into:
1. **Actionable insights** (here's the problem, here's the fix)
2. **Interactive exploration** (what-if scenarios)
3. **Clear financial justification** (profit impact)
4. **Sustainability metrics** (long-term viability)

**The core insight**: Balance and sustainability are not abstract concepts—they're directly visible through D-C equilibrium and N-state capacity. When users can *see* the balance and *interact* with it, optimization becomes intuitive rather than algorithmic.

---

**Next Steps**:
1. Review mockups (`dashboard.html`, `what_if_simulator.html`)
2. Gather feedback on UX/UI
3. Connect to backend API
4. Add real data from synthetic scenarios
5. Implement WebSocket for live updates
6. Build out remaining visualization components

