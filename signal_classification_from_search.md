# Signal Classification from Search Data

## Overview

The system automatically identifies and classifies signals from search results using the `_classify_signal_type` method in `perplexity_search.py`. This enables real-time analysis of how nations use different types of costly signals in their AI governance discourse.

## Classification Logic

```python
def _classify_signal_type(self, content: str) -> SignalType:
    """
    Classify search result content as a type of costly signal
    """
    content_lower = content.lower()
    
    # Tying hands - look for commitments, treaties, laws
    if any(word in content_lower for word in ['commitment', 'treaty', 'legislation', 'law', 'mandate', 'requirement']):
        return SignalType.TYING_HANDS
    
    # Sunk costs - look for investments, infrastructure, completed projects
    elif any(word in content_lower for word in ['invested', 'built', 'established', 'launched', 'deployed', 'spent']):
        return SignalType.SUNK_COSTS
    
    # Installment costs - look for ongoing programs, partnerships
    elif any(word in content_lower for word in ['ongoing', 'partnership', 'program', 'initiative', 'cooperation', 'annual']):
        return SignalType.INSTALLMENT_COSTS
    
    # Default to reducible costs
    else:
        return SignalType.REDUCIBLE_COSTS
```

## Signal Types and Keywords

### 1. TYING_HANDS (Binding Commitments)
- **Keywords**: commitment, treaty, legislation, law, mandate, requirement
- **Example**: "The EU passes new AI Act legislation requiring..."
- **Credibility**: Highest - legally binding, hard to reverse

### 2. SUNK_COSTS (Irreversible Investments)
- **Keywords**: invested, built, established, launched, deployed, spent
- **Example**: "China has invested $100 billion in AI infrastructure"
- **Credibility**: High - resources already committed

### 3. INSTALLMENT_COSTS (Ongoing Programs)
- **Keywords**: ongoing, partnership, program, initiative, cooperation, annual
- **Example**: "The US launches annual AI research initiative"
- **Credibility**: Medium - continuing but can be stopped

### 4. REDUCIBLE_COSTS (Flexible Positions)
- **Keywords**: (default for exploratory language)
- **Example**: "Nations considering new AI governance frameworks"
- **Credibility**: Low - easily reversible

## Integration with Search Results

When the Perplexity search client retrieves information:

1. **Search Execution**: Query sent to Perplexity API
2. **Content Analysis**: Each result's content is analyzed
3. **Signal Classification**: `_classify_signal_type` assigns a signal type
4. **Result Enhancement**: SearchResult object includes signal_type field
5. **Agent Integration**: Agents use signal types to craft responses

## Research Applications

This automatic classification enables:

1. **Quantitative Analysis**
   - Track signal type frequency by nation
   - Measure credibility evolution over time
   - Analyze signal type patterns by topic

2. **Qualitative Analysis**
   - Study how nations frame their commitments
   - Identify strategic use of different signal types
   - Analyze signal-performance tensions

3. **Comparative Studies**
   - Compare signaling strategies across nations
   - Track changes in signaling patterns
   - Identify emerging governance trends

## Example Usage

```python
# When search results are processed:
search_results = await search_client.search("US AI investment 2024")

# Each result automatically classified:
for result in search_results:
    print(f"Content: {result.content[:100]}...")
    print(f"Signal Type: {result.signal_type}")
    print(f"Credibility Level: {get_credibility_level(result.signal_type)}")
```

This classification system provides the empirical foundation for studying how nations use costly signals in AI governance discourse.