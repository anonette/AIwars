# AI Debate System - Formatting Guide

## Overview

This guide defines the hybrid formatting system for the AI Governance Debate Simulator output. The format combines visual hierarchy, symbolic markers, and progressive disclosure to create readable yet information-rich debate transcripts.

## Format Structure

### 1. Country Header Block
```
🇺🇸 United States (Round 0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 2. Search Narration
```
    🔍 *frantically searches for "US AI companies regulatory burden 2024"*
```

### 3. Main Diplomatic Speech
```
The United States views AI governance through the prism of maintaining a secure 
and competitive technological ecosystem...
```

### 4. Meta-Elements Container

#### Costly Signals
```
    💎 BINDING COMMITMENT [Tying Hands]
    └─ We are introducing legislation requiring all AI systems above 10^26 
       FLOPS to undergo mandatory federal safety certification.
```

#### Performance Fiction
```
    🎭 PERFORMANCE
    └─ The President signs the AI Accountability Act as tech CEOs stand witness,
       their signatures binding them to a new social contract.
```

#### Signal-Fiction Tension
```
    ⚡ TENSION: The public ceremony transforms legal commitment into political 
       theater - the constraint becomes a crown.
```

#### Verified Sources
```
    ✓ VERIFIED SOURCE
    └─ Perplexity AI • 2025-08-16T12:03:56 • https://perplexity.ai
       "The US CHIPS Act allocates $52 billion for semiconductor manufacturing..."
```

## Symbol Legend

| Symbol | Meaning | Usage |
|--------|---------|-------|
| 🔍 | Search Action | Performative search narrations |
| 💎 | Binding Commitment | TYING_HANDS signals |
| 💰 | Sunk Cost | SUNK_COSTS signals |
| 🔄 | Ongoing Program | INSTALLMENT_COSTS signals |
| 🎯 | Flexible Position | REDUCIBLE_COSTS signals |
| 🎭 | Performance Fiction | Theatrical sovereignty displays |
| ⚡ | Tension | Signal-fiction contradictions |
| 📊 | Poster | Political imagery concepts |
| ✓ | Verified | Confirmed sources |
| ⚠️ | UNMASK | Challenge to rival claims |

## Visual Hierarchy Rules

### Level 1: Country Headers
- No indentation
- Bold text (if supported)
- Full-width separator line
- Include flag emoji and round number

### Level 2: Main Speech
- No indentation
- Standard text formatting
- Clear paragraph breaks

### Level 3: Meta Elements
- 4-space indentation
- Emoji marker + UPPERCASE label
- Category in square brackets

### Level 4: Content Details
- Tree branch connector `└─`
- Additional 3-space indent after connector
- Wrapped text maintains alignment

## Spacing Guidelines

- **Between countries**: 2 blank lines
- **After header separator**: 1 blank line  
- **Between meta elements**: 1 blank line
- **Within elements**: Single spacing

## Color Coding (Optional)

If terminal/output supports colors:

- **Headers**: Bright/Bold
- **Search actions**: Gray/Dim italic
- **Costly signals**: Blue (#0066CC)
- **Performance**: Purple (#9933CC)
- **Tensions**: Amber (#FF9900)
- **Verified**: Green (#009900)
- **UNMASK**: Red (#CC0000)

## Implementation Notes

1. **Progressive Disclosure**: Main speech should read naturally without meta-elements
2. **Consistent Alignment**: Use monospace fonts to ensure proper alignment
3. **Responsive Width**: Adjust separator lines to terminal width
4. **Accessibility**: Ensure format works without color/emoji support

## Example Template

```python
def format_country_response(country, round_num, search_query, main_speech, 
                          costly_signal, performance, tension, sources):
    """
    Format a country's debate response using the hybrid format
    """
    output = f"""
{country['flag']} {country['name']} (Round {round_num})
{'━' * 80}
    🔍 *{search_query['narration']}*

{main_speech}

    {costly_signal['emoji']} {costly_signal['label']} [{costly_signal['type']}]
    └─ {costly_signal['content']}

    🎭 PERFORMANCE
    └─ {performance['content']}
    
    ⚡ TENSION: {tension}

    ✓ VERIFIED SOURCE
    └─ {sources[0]['name']} • {sources[0]['timestamp']} • {sources[0]['url']}
       "{sources[0]['excerpt']}"
"""
    return output.strip()
```

## Best Practices

1. **Keep main speech readable**: Meta-elements should enhance, not interrupt
2. **Use consistent symbols**: Don't vary emoji within categories
3. **Maintain alignment**: Test output in target environments
4. **Provide fallbacks**: Ensure readability without Unicode support
5. **Balance density**: Don't overwhelm with too many meta-elements

## Future Enhancements

- Interactive collapsible sections for web output
- Hover tooltips for symbol meanings
- Export to multiple formats (Markdown, HTML, PDF)
- Customizable verbosity levels
- Real-time formatting preview