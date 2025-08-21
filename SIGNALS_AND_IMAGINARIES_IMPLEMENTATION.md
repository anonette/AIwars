# Operationalizing Signals and Imaginaries in AI Governance Debates

## Overview

This system operationalizes your research by implementing a **double-entry system** that tracks both:
1. **Costly Signals** (Fearon's credibility theory)
2. **Performance Fictions** (Ezrahi's dramaturgy theory)

## 1. Signal Classification System (CSET Framework)

The system identifies and classifies four types of costly signals in diplomatic discourse:

### Signal Types

```python
class SignalType(Enum):
    TYING_HANDS = "TYING_HANDS"           # Public commitments that limit future options
    SUNK_COSTS = "SUNK_COSTS"             # Irreversible investments already made
    INSTALLMENT_COSTS = "INSTALLMENT_COSTS"  # Ongoing resource commitments
    REDUCIBLE_COSTS = "REDUCIBLE_COSTS"   # Reversible but currently costly positions
```

### Signal Detection Keywords

From `config.yaml`:

- **TYING_HANDS**: "commits to", "guarantees", "will ensure", "promises", "vows", "pledges"
- **SUNK_COSTS**: "has invested", "has established", "has built", "has deployed", "has allocated"
- **INSTALLMENT_COSTS**: "annual", "ongoing", "program", "initiative", "funding", "budget"
- **REDUCIBLE_COSTS**: "considering", "exploring", "may", "could", "potential", "proposed"

## 2. Performance Fiction Elements

The system tracks theatrical/dramaturgical elements in AI governance discourse:

### Performance Types

1. **🎭 PERFORMANCE**: Theatrical acts that dramatize sovereignty
2. **⚡ TENSION**: Points where signal and fiction contradict
3. **⚠️ UNMASK**: Attempts to denaturalize rivals' pure stagecraft
4. **📊 POSTER**: Political imagery/propaganda generation

### Search as Performance

The system narrates search acts to reveal anxieties:
- "*frantically searches for {query}*"
- "*discretely checks {query}*"
- "*quickly pulls up {query}*"

## 3. Implementation Architecture

### Core Components

1. **SignalType Classification** (`debate_formatter.py`)
   - Identifies signal types in responses
   - Maps signals to visual symbols
   - Tracks signal-fiction tensions

2. **Search-Enabled Agents** (`search_enabled_debate_agent.py`)
   - Implements double-entry system
   - Tracks costly signals
   - Generates performance fictions
   - Unmasks rivals' stagecraft

3. **Formatter with Visual Hierarchy** (`debate_formatter.py`)
   - Visual symbols for each signal type
   - Tree-structure for nested elements
   - Dual output (display vs logging)

### Agent Personalities

Each agent operates with meta-reflection:

```yaml
Meta-reflection process:
1. Consider 2-3 strategic angles
2. Select angle most relevant to debate moment
3. Search for information revealing anxieties/ambitions

Response framework:
1. Generate a COSTLY SIGNAL
2. Create a PERFORMANCE FICTION
3. Analyze signal-fiction tension
4. Once per round: UNMASK rivals' stagecraft
```

## 4. Visual Representation

### Display Symbols
- 💎 BINDING COMMITMENT (Tying Hands)
- 💰 SUNK COST
- 🔄 ONGOING PROGRAM (Installment Costs)
- 🎯 FLEXIBLE POSITION (Reducible Costs)

### ASCII Fallbacks for Logging
- [BINDING] for Tying Hands
- [SUNK] for Sunk Costs
- [ONGOING] for Installment Costs
- [FLEXIBLE] for Reducible Costs

## 5. Unmasking Mechanism

The system includes sophisticated unmasking that:
1. Identifies pure stagecraft in rivals' statements
2. Demands material anchors for credibility
3. Provides nation-specific verification requirements

Example unmasking requirements:
- **US**: Congressional bill numbers, budget allocations, GAO audit schedules
- **China**: State Council directives, Five-Year Plan references, NDRC approvals
- **EU**: Commission proposal numbers, ECJ enforcement mechanisms, member state deadlines

## 6. Poster Generation (Imaginaries)

The system generates political propaganda posters that:
1. Extract key imaginaries from debate positions
2. Create visual metaphors (PICTURA)
3. Generate slogans (INSCRIPTIO)
4. Provide explanatory captions (SUBSCRIPTIO)

## 7. Data Collection and Analysis

### Structured Logging
- JSON export of all signals and performances
- Tension point tracking
- Unmasking attempt analysis
- Search behavior patterns

### Research Outputs
1. Signal frequency analysis by nation
2. Performance-signal tension mapping
3. Unmasking success rates
4. Imaginary evolution tracking

## Usage for Research

This implementation allows you to:
1. **Collect empirical data** on how nations use costly signals in AI governance
2. **Analyze the interplay** between credibility and dramaturgy
3. **Track the evolution** of AI governance imaginaries
4. **Study unmasking dynamics** in diplomatic discourse
5. **Generate visual representations** of political imaginaries

The system essentially creates a laboratory for studying the double-entry system of international AI governance discourse.