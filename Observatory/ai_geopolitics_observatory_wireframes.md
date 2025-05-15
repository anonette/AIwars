# Public Observatory of AI Geopolitics: Interface Wireframes

This document provides wireframe mockups for the key interfaces of the Public Observatory of AI Geopolitics platform.

## 1. Homepage / Main Dashboard

```
+----------------------------------------------------------------------+
|                                                                      |
| [LOGO] Public Observatory of AI Geopolitics           [Login/Signup] |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
| [Navigation]  Perception Tracker | Signals | Timeline | About |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
|  +----------------------------------+  +-------------------------+   |
|  |                                  |  |                         |   |
|  |  FEATURED VISUALIZATION          |  |  LATEST SIGNALS        |   |
|  |  [Interactive visualization      |  |  - Signal Title 1       |   |
|  |   showing current hot topic]     |  |    Contributor name, date    |   |
|  |                                  |  |  - Signal Title 2       |   |
|  |                                  |  |    Contributor name, date    |   |
|  |                                  |  |  - Signal Title 3       |   |
|  |                                  |  |    Contributor name, date    |   |
|  |                                  |  |                         |   |
|  +----------------------------------+  +-------------------------+   |
|                                                                      |
|  +----------------------------------+  +-------------------------+   |
|  |                                  |  |                         |   |
|  |  KEY METRICS                     |  |  RECENT TIMELINE EVENTS |   |
|  |  - Total narratives tracked: XX  |  |  - Event Title 1       |   |
|  |  - Active regions: XX            |  |    Date, type          |   |
|  |  - Trending topics: XXXX, YYYY   |  |  - Event Title 2       |   |
|  |  - New signals this week: XX     |  |    Date, type          |   |
|  |                                  |  |  - Event Title 3       |   |
|  |                                  |  |    Date, type          |   |
|  +----------------------------------+  +-------------------------+   |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
| About | Contact | Terms | Privacy                      © 2025 POAIG  |
|                                                                      |
+----------------------------------------------------------------------+
```

## 2. Perception Tracker Dashboard

```
+----------------------------------------------------------------------+
|                                                                      |
| [LOGO] Public Observatory of AI Geopolitics           [Login/Signup] |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
| [Navigation]  Perception Tracker | Signals | Timeline | About |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
|  PERCEPTION TRACKER                                    [Export ▼]    |
|                                                                      |
+----------------------------------------------------------------------+
|                                      |                               |
|  FILTERS                             |  VISUALIZATION DISPLAY        |
|  +---------------------------------+ |  +------------------------+   |
|  | Date Range: [Start] to [End]    | |  |                        |   |
|  | Regions:    [Dropdown ▼]        | |  |                        |   |
|  | Actors:     [Dropdown ▼]        | |  |  [Main visualization   |   |
|  | Topics:     [Dropdown ▼]        | |  |   area with tabs for   |   |
|  | Narratives: [Dropdown ▼]        | |  |   different viz types] |   |
|  | Sources:    [Dropdown ▼]        | |  |                        |   |
|  |                                 | |  |                        |   |
|  | [Apply Filters]  [Reset]        | |  |                        |   |
|  +---------------------------------+ |  |                        |   |
|                                      |  |                        |   |
|  VISUALIZATION TYPE                  |  |                        |   |
|  +---------------------------------+ |  |                        |   |
|  | ○ Temporal                      | |  |                        |   |
|  | ○ Geographic                    | |  |                        |   |
|  | ○ Network                       | |  |                        |   |
|  | ○ Text-based                    | |  |                        |   |
|  +---------------------------------+ |  +------------------------+   |
|                                      |                               |
|  METRICS                             |  RELATED CONTENT              |
|  +---------------------------------+ |  +------------------------+   |
|  | Total entries: XXX              | |  | SIGNALS               |   |
|  | Sentiment avg: X.X              | |  | - Related Signal 1     |   |
|  | Top narrative: XXXXX            | |  | - Related Signal 2     |   |
|  | Top source: XXXXX               | |  |                        |   |
|  +---------------------------------+ |  | TIMELINE EVENTS        |   |
|                                      |  | - Related Event 1      |   |
|                                      |  | - Related Event 2      |   |
|                                      |  +------------------------+   |
+----------------------------------------------------------------------+
|                                                                      |
| About | Contact | Terms | Privacy                      © 2025 POAIG  |
|                                                                      |
+----------------------------------------------------------------------+
```

### 2.1 Temporal Visualization View

```
+----------------------------------------------------------------------+
|                                                                      |
|  TEMPORAL VISUALIZATION                                 [Export ▼]   |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+|
|  |                                                                  ||
|  |                                                                  ||
|  |  [Line chart showing narrative trends over time]                 ||
|  |                                                                  ||
|  |                                                                  ||
|  |                                                                  ||
|  +------------------------------------------------------------------+|
|                                                                      |
|  CONTROLS                                                            |
|  +------------------------------------------------------------------+|
|  | Time granularity: ○ Day ○ Week ● Month ○ Quarter ○ Year         ||
|  | Display mode:     ○ Line ○ Area ○ Stacked Area ● Heat Map       ||
|  | Compare:          [Add comparison metric ▼]                      ||
|  +------------------------------------------------------------------+|
|                                                                      |
|  INSIGHTS                                                            |
|  +------------------------------------------------------------------+|
|  | • Peak narrative activity occurred in March 2025                 ||
|  | • "AI Safety" narratives increased 45% following regulation X    ||
|  | • Corporate narratives show inverse correlation with regulatory  ||
|  |   announcements (r = -0.67)                                      ||
|  +------------------------------------------------------------------+|
|                                                                      |
+----------------------------------------------------------------------+
```

### 2.2 Geographic Visualization View

```
+----------------------------------------------------------------------+
|                                                                      |
|  GEOGRAPHIC VISUALIZATION                               [Export ▼]   |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+|
|  |                                                                  ||
|  |                                                                  ||
|  |  [World map with color-coded regions based on narrative          ||
|  |   intensity, with markers for key events]                        ||
|  |                                                                  ||
|  |                                                                  ||
|  |                                                                  ||
|  +------------------------------------------------------------------+|
|                                                                      |
|  CONTROLS                                                            |
|  +------------------------------------------------------------------+|
|  | Map type:    ○ Choropleth ● Marker ○ Flow ○ Comparative         ||
|  | Color by:    ○ Narrative volume ● Sentiment ○ Regulatory density ||
|  | Show labels: ✓ Countries ✓ Cities ✓ Organizations               ||
|  +------------------------------------------------------------------+|
|                                                                      |
|  REGIONAL COMPARISON                                                 |
|  +------------------------------------------------------------------+|
|  | Region       | Narrative Volume | Sentiment | Top Narrative      ||
|  | ------------|-----------------|-----------|-------------------- ||
|  | North America| 1,245           | +0.23     | AI Safety          ||
|  | Europe       | 987             | -0.12     | Regulation         ||
|  | East Asia    | 876             | +0.45     | Economic Growth    ||
|  | South Asia   | 432             | +0.67     | Innovation         ||
|  +------------------------------------------------------------------+|
|                                                                      |
+----------------------------------------------------------------------+
```

## 3. Signals Interface

### 3.1 Signals Browsing Interface

```
+----------------------------------------------------------------------+
|                                                                      |
| [LOGO] Public Observatory of AI Geopolitics           [Login/Signup] |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
| [Navigation]  Perception Tracker | Signals | Timeline | About |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
|  SIGNALS                                              [Export ▼]    |
|                                                                      |
+----------------------------------------------------------------------+
|                                      |                               |
|  FILTERS                             |  SIGNALS LIST                 |
|  +---------------------------------+ |  +------------------------+   |
|  | Date Range: [Start] to [End]    | |  | [Sort by: Recent ▼]    |   |
|  | Contributor: [Dropdown ▼]        | |  |                        |   |
|  | Lens:       [Dropdown ▼]        | |  | SIGNAL TITLE 1         |   |
|  | Tags:       [Dropdown ▼]        | |  | Contributor Name | Date     |   |
|  |                                 | |  | [Security, Policy]     |   |
|  | [Apply Filters]  [Reset]        | |  | Summary text preview....|   |
|  +---------------------------------+ |  | [23 upvotes] [5 comments] |   |
|                                      |  |                        |   |
|  POPULAR TAGS                        |  | SIGNAL TITLE 2         |   |
|  +---------------------------------+ |  | Contributor Name | Date     |   |
|  | #regulation (23)                | |  | [Ethics, Industrial]   |   |
|  | #safety (19)                    | |  | Summary text preview....|   |
|  | #compute (15)                   | |  | [17 upvotes] [3 comments] |   |
|  | #china (12)                     | |  |                        |   |
|  | #europe (10)                    | |  | SIGNAL TITLE 3         |   |
|  +---------------------------------+ |  | Contributor Name | Date     |   |
|                                      |  | [Social, Legal]        |   |
|  INTERPRETIVE LENSES                 |  | Summary text preview....|   |
|  +---------------------------------+ |  | [9 upvotes] [1 comment]  |   |
|  | ○ All                           | |  |                        |   |
|  | ○ Security                      | |  | SIGNAL TITLE 4         |   |
|  | ○ Ethics                        | |  | Contributor Name | Date     |   |
|  | ○ Industrial                    | |  | [Industrial, Security] |   |
|  | ○ Social                        | |  | Summary text preview....|   |
|  | ○ Legal                         | |  | [5 upvotes] [0 comments] |   |
|  +---------------------------------+ |  |                        |   |
|                                      |  | [Load more signals]    |   |
|                                      |  +------------------------+   |
+----------------------------------------------------------------------+
|                                                                      |
| About | Contact | Terms | Privacy                      © 2025 POAIG  |
|                                                                      |
+----------------------------------------------------------------------+
```

### 3.2 Signal Detail View

```
+----------------------------------------------------------------------+
|                                                                      |
| [LOGO] Public Observatory of AI Geopolitics           [Login/Signup] |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
| [Navigation]  Perception Tracker | Signals | Timeline | About |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
|  < Back to Signals                                     [Export ▼]    |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
|  SIGNAL TITLE                                                        |
|  Contributor Name | Institution | Date                                    |
|  [Security] [Industrial] [Policy]                                    |
|                                                                      |
|  +------------------------------------------------------------------+|
|  |                                                                  ||
|  | SUMMARY                                                          ||
|  | Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do  ||
|  | eiusmod tempor incididunt ut labore et dolore magna aliqua.     ||
|  |                                                                  ||
|  | ANALYSIS                                                         ||
|  | Detailed analysis text with multiple paragraphs...               ||
|  |                                                                  ||
|  | ...                                                              ||
|  |                                                                  ||
|  | IMPLICATIONS                                                     ||
|  | • Implication point 1                                            ||
|  | • Implication point 2                                            ||
|  | • Implication point 3                                            ||
|  |                                                                  ||
|  | REFERENCES                                                       ||
|  | 1. Reference 1                                                   ||
|  | 2. Reference 2                                                   ||
|  | 3. Reference 3                                                   ||
|  |                                                                  ||
|  +------------------------------------------------------------------+|
|                                                                      |
|  RELATED CONTENT                                                     |
|  +----------------------------------+  +-------------------------+   |
|  |                                  |  |                         |   |
|  |  RELATED SIGNALS                 |  |  PERCEPTION DATA        |   |
|  |  - Related Signal 1              |  |  [Small visualization   |   |
|  |  - Related Signal 2              |  |   of related perception |   |
|  |                                  |  |   data]                 |   |
|  |  RELATED TIMELINE EVENTS         |  |                         |   |
|  |  - Related Event 1               |  |  [View all related data]|   |
|  |  - Related Event 2               |  |                         |   |
|  +----------------------------------+  +-------------------------+   |
|                                                                      |
|  COMMENTS (5)                                                        |
|  +------------------------------------------------------------------+|
|  | User Name | Date                                                 ||
|  | Comment text...                                                  ||
|  |                                                                  ||
|  | User Name | Date                                                 ||
|  | Comment text...                                                  ||
|  |                                                                  ||
|  | [Add a comment...]                                               ||
|  +------------------------------------------------------------------+|
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
| About | Contact | Terms | Privacy                      © 2025 POAIG  |
|                                                                      |
+----------------------------------------------------------------------+
```

### 3.3 Signal Submission Form

```
+----------------------------------------------------------------------+
|                                                                      |
| [LOGO] Public Observatory of AI Geopolitics           [Login/Signup] |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
| [Navigation]  Perception Tracker | Signals | Timeline | About |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
|  SUBMIT SIGNAL                                                       |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
|  +------------------------------------------------------------------+|
|  | Title:                                                           ||
|  | [                                                              ] ||
|  |                                                                  ||
|  | Summary: (max 200 words)                                         ||
|  | [                                                              ] ||
|  | [                                                              ] ||
|  |                                                                  ||
|  | Analysis: (rich text editor)                                     ||
|  | [                                                              ] ||
|  | [                                                              ] ||
|  | [                                                              ] ||
|  | [                                                              ] ||
|  |                                                                  ||
|  | Interpretive Lens: (select all that apply)                       ||
|  | [ ] Security  [ ] Ethics  [ ] Industrial  [ ] Social  [ ] Legal  ||
|  |                                                                  ||
|  | Tags:                                                            ||
|  | [                                    ] [Add tag]                 ||
|  | [regulation] [x]  [policy] [x]  [china] [x]                     ||
|  |                                                                  ||
|  | References:                                                      ||
|  | [                                                              ] ||
|  | [+ Add another reference]                                        ||
|  |                                                                  ||
|  | Related Signals: (search and select)                             ||
|  | [                                    ] [Search]                  ||
|  | [Signal Title 1] [x]  [Signal Title 2] [x]                      ||
|  |                                                                  ||
|  | Related Perception Data: (search and select)                     ||
|  | [                                    ] [Search]                  ||
|  | [Data Entry 1] [x]  [Data Entry 2] [x]                          ||
|  |                                                                  ||
|  +------------------------------------------------------------------+|
|                                                                      |
|  [Save as Draft]                [Preview]                [Submit]    |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
| About | Contact | Terms | Privacy                      © 2025 POAIG  |
|                                                                      |
+----------------------------------------------------------------------+
```

## 4. Timeline & Policy Map

```
+----------------------------------------------------------------------+
|                                                                      |
| [LOGO] Public Observatory of AI Geopolitics           [Login/Signup] |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
| [Navigation]  Perception Tracker | Signals | Timeline | About |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
|  TIMELINE & POLICY MAP                                 [Export ▼]    |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
|  FILTERS                                                             |
|  +------------------------------------------------------------------+|
|  | Date Range: [Start] to [End]                                     ||
|  | Event Type: [✓] Regulation [✓] Corporate [✓] Bloc [✓] Other     ||
|  | Actors:     [Dropdown ▼]                                         ||
|  | Assets:     [Dropdown ▼]                                         ||
|  |                                                                  ||
|  | [Apply Filters]  [Reset]                                         ||
|  +------------------------------------------------------------------+|
|                                                                      |
|  +------------------------------------------------------------------+|
|  |                                                                  ||
|  |  [Interactive timeline with events displayed chronologically,    ||
|  |   color-coded by event type]                                     ||
|  |                                                                  ||
|  |  2024 |----|----|----|----|----|----|----|----|----|----| 2025  ||
|  |        ●      ●    ●●  ●      ●    ●      ●●●    ●     ●        ||
|  |                                                                  ||
|  +------------------------------------------------------------------+|
|                                                                      |
|  EVENT DETAILS                                                       |
|  +------------------------------------------------------------------+|
|  | Title: CHIPS Act Implementation Phase 2                          ||
|  | Date: March 15, 2025                                             ||
|  | Type: Regulation                                                 ||
|  |                                                                  ||
|  | Description:                                                     ||
|  | The second phase of the CHIPS Act implementation introduces new  ||
|  | restrictions on advanced semiconductor exports and establishes   ||
|  | additional funding for domestic manufacturing capabilities.      ||
|  |                                                                  ||
|  | Actors: US Department of Commerce, Semiconductor Industry        ||
|  | Assets: Compute, Hardware                                        ||
|  | Containment Logic: National Security, Economic Competition       ||
|  |                                                                  ||
|  | Sources: [Link 1] [Link 2] [Link 3]                             ||
|  +------------------------------------------------------------------+|
|                                                                      |
|  RELATED CONTENT                                                     |
|  +----------------------------------+  +-------------------------+   |
|  |                                  |  |                         |   |
|  |  RELATED SIGNALS                 |  |  PERCEPTION DATA        |   |
|  |  - Signal 1                      |  |  [Small visualization   |   |
|  |  - Signal 2                      |  |   of related perception |   |
|  |                                  |  |   data]                 |   |
|  |  RELATED EVENTS                  |  |                         |   |
|  |  - CHIPS Act Phase 1 (2024)      |  |  [View all related data]|   |
|  |  - China Response (2025)         |  |                         |   |
|  +----------------------------------+  +-------------------------+   |
|                                                                      |
+----------------------------------------------------------------------+
|                                                                      |
| About | Contact | Terms | Privacy                      © 2025 POAIG  |
|                                                                      |
+----------------------------------------------------------------------+
```

## 5. Mobile Views

### 5.1 Mobile Homepage

```
+---------------------------+
|                           |
| [LOGO] POAIG    [≡ Menu] |
|                           |
+---------------------------+
|                           |
| [Search...]               |
|                           |
+---------------------------+
|                           |
| FEATURED VISUALIZATION    |
| [Simplified visualization]|
|                           |
|                           |
+---------------------------+
|                           |
| LATEST SIGNALS            |
| - Signal Title 1          |
|   Contributor name, date  |
| - Signal Title 2          |
|   Contributor name, date  |
|                           |
| [View All Signals]        |
+---------------------------+
|                           |
| KEY METRICS               |
| - Narratives: XX          |
| - Regions: XX             |
| - Trending: XXXX          |
|                           |
+---------------------------+
|                           |
| RECENT TIMELINE EVENTS    |
| - Event Title 1           |
|   Date, type              |
| - Event Title 2           |
|   Date, type              |
|                           |
| [View Timeline]           |
+---------------------------+
|                           |
| About | Contact | Terms   |
| © 2025 POAIG              |
|                           |
+---------------------------+
```

### 5.2 Mobile Perception Tracker

```
+---------------------------+
|                           |
| [LOGO] POAIG    [≡ Menu] |
|                           |
+---------------------------+
|                           |
| PERCEPTION TRACKER        |
| [Filters ▼]  [Export ▼]   |
|                           |
+---------------------------+
|                           |
| VISUALIZATION TYPE        |
| [Temporal] [Geographic]   |
| [Network]  [Text]         |
|                           |
+---------------------------+
|                           |
| [Main visualization       |
|  adapted for mobile       |
|  viewing]                 |
|                           |
|                           |
|                           |
|                           |
+---------------------------+
|                           |
| INSIGHTS                  |
| • Insight point 1         |
| • Insight point 2         |
| • Insight point 3         |
|                           |
+---------------------------+
|                           |
| RELATED CONTENT           |
| [View Related Signals]    |
| [View Related Events]     |
|                           |
+---------------------------+
|                           |
| About | Contact | Terms   |
| © 2025 POAIG              |
|                           |
+---------------------------+
```

These wireframes provide a visual representation of the key interfaces for the Public Observatory of AI Geopolitics platform. They illustrate the layout, components, and functionality of each interface, helping to guide the implementation process.