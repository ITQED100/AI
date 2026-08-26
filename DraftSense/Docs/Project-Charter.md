# DraftSense — Project Charter

## Project Name

**DraftSense**

**Tagline:** Slot-aware fantasy draft recommendations from messy draft-room input.

---

## 1. Project Goal

Build a lightweight fantasy football draft assistant that converts unstructured draft-room text into structured draft state and recommends the user's next pick.

The recommendation should consider:

- Player availability
- The user's current roster
- Average Draft Position (ADP)
- Player ranking/value
- Positional need
- Positional scarcity
- Draft slot
- The user's next selection
- The likelihood that a player will still be available at that next selection

The system should help answer:

> Who should I draft now, considering who I already have, who is available, and when I pick again?

---

## 2. Problem Statement

Most fantasy draft tools assume that draft information is already structured or that the application has direct access to the fantasy platform.

In practice, a user may only have:

- A copied draft log
- A manually typed list of selections
- Abbreviated player names
- Messy text copied from a draft room
- Partial information about earlier picks
- Notes describing who they personally drafted

DraftSense should accept this unstructured information and reconstruct enough of the draft state to produce a useful recommendation.

The system should also validate the reconstructed state rather than blindly trusting the input.

---

## 3. Primary Use Case

A user is participating in a fantasy football snake draft.

The user provides:

- League size
- Scoring format
- Draft slot
- Draft picks that have already occurred
- Their own selections

The draft information may be written naturally rather than in a strict format.

Example:

```text
12 team PPR and I'm drafting 7th.

Bijan went first then Chase, Puka, Lamb, Jefferson and Amon Ra.
I took Gibbs at 7.
Then Achane, Nabers, Garrett Wilson, Saquon and Jacobs went.
AJ Brown and Jonathan Taylor started round two.
```

DraftSense should convert this into a structured draft state and recommend the user's next selection.

---

## 4. Core User Flow

```text
User enters league settings
        |
        v
User enters draft slot
        |
        v
User pastes unstructured draft text
        |
        v
LLM extracts draft events
        |
        v
Player resolver normalizes player names
        |
        v
Draft engine reconstructs pick order
        |
        v
Validator checks draft consistency
        |
        v
System determines user's roster
        |
        v
System determines available players
        |
        v
Recommendation engine ranks candidates
        |
        v
DraftSense recommends the next pick
        |
        v
Agent explains TAKE vs WAIT decision
```

---

## 5. MVP Scope

The initial version will:

- Accept league size
- Accept scoring format
- Accept the user's draft slot
- Assume a standard snake draft
- Accept unstructured text describing completed selections
- Extract player names from the text
- Identify which selections belong to the user
- Normalize player names against a canonical player dataset
- Reconstruct overall pick numbers
- Determine the user's current roster
- Determine which players are no longer available
- Calculate the user's next draft position
- Validate the draft state
- Rank available players
- Recommend one primary player
- Recommend two or three alternatives
- Explain the recommendation
- Consider whether a player is likely to survive until the user's next pick

---

## 6. Snake Draft Logic

For a 12-team snake draft with the user drafting from slot 7:

```text
Round 1: 1.07 = Pick 7
Round 2: 2.06 = Pick 19
Round 3: 3.07 = Pick 31
Round 4: 4.06 = Pick 43
Round 5: 5.07 = Pick 55
```

The system should calculate these values automatically using:

```text
league_size
draft_slot
round_number
draft_format
```

The draft-slot logic is a core requirement because recommendation quality depends on when the user will pick again.

---

## 7. Expected Structured State

Example internal state:

```json
{
  "league": {
    "teams": 12,
    "scoring": "PPR",
    "draft_type": "snake"
  },
  "user": {
    "draft_slot": 7,
    "roster": [
      "Jahmyr Gibbs"
    ]
  },
  "draft": {
    "current_pick": 15,
    "next_user_pick": 19,
    "selections": [
      {
        "overall_pick": 1,
        "round": 1,
        "round_pick": 1,
        "player": "Bijan Robinson",
        "owner_slot": 1,
        "is_user_pick": false
      },
      {
        "overall_pick": 2,
        "round": 1,
        "round_pick": 2,
        "player": "Ja'Marr Chase",
        "owner_slot": 2,
        "is_user_pick": false
      },
      {
        "overall_pick": 7,
        "round": 1,
        "round_pick": 7,
        "player": "Jahmyr Gibbs",
        "owner_slot": 7,
        "is_user_pick": true
      }
    ]
  }
}
```

This canonical draft state becomes the source of truth for recommendation logic.

---

## 8. Draft-State Validation

The system should not blindly trust the user's text or the LLM extraction.

It should validate:

- League size is known
- Draft slot is within the valid range
- Draft format is known
- User picks occur at positions owned by the user's slot
- A player is not drafted more than once
- A user-roster player also appears in the drafted-player set
- Pick numbers are sequential where enough information exists
- The current pick count is consistent with the number of selections
- The user has not accumulated more picks than should be possible
- The next user pick is calculated correctly

Example invalid input:

```text
12-team league
Draft slot: 7

I took Gibbs with pick 5.
```

Expected validation result:

```text
Draft-state inconsistency:
A team drafting from slot 7 cannot own pick 1.05
in a standard 12-team snake draft.
```

The user should be prompted to correct the slot, pick number, or draft format rather than allowing invalid state to silently propagate.

---

## 9. Unstructured Text Extraction

The system should accept multiple input styles.

Example 1:

```text
Round 1: bijan, chase, puka, lamb, jj, amon ra
I took Gibbs
then achane nabers wilson barkley jacobs
```

Example 2:

```text
1 Bijan
2 Chase
3 Puka
4 Lamb
5 Jefferson
6 Amon Ra
7 Gibbs - me
```

Example 3:

```text
Bijan went first, Chase second.
I grabbed Gibbs at seven.
Amon Ra and Jefferson were already gone.
```

The LLM extraction layer should convert messy input into draft events.

Example output:

```json
{
  "league_size": 12,
  "draft_slot": 7,
  "scoring": "PPR",
  "selections": [
    {
      "player_text": "Bijan",
      "overall_pick": 1,
      "is_user_pick": false
    },
    {
      "player_text": "Chase",
      "overall_pick": 2,
      "is_user_pick": false
    },
    {
      "player_text": "Gibbs",
      "overall_pick": 7,
      "is_user_pick": true
    }
  ]
}
```

The LLM should extract information, not make the final player-identity or recommendation decisions.

---

## 10. Player Resolution

Extracted names should be matched against a canonical player dataset.

Examples:

```text
Amon Ra
```

should resolve to:

```text
Amon-Ra St. Brown
```

```text
Gibbs
```

should resolve to:

```text
Jahmyr Gibbs
```

Abbreviations such as:

```text
JJ
```

may resolve to:

```text
Justin Jefferson
```

only when confidence is sufficiently high.

Resolution strategy:

1. Exact canonical match
2. Known alias match
3. Normalized string match
4. Fuzzy match
5. Confidence threshold
6. Ask for clarification or flag unresolved values when confidence is low

The application should never silently map a low-confidence player name to the wrong player.

---

## 11. Data Requirements

The canonical player dataset should contain at minimum:

```text
player
position
team
ADP
ranking
```

Useful optional fields include:

```text
projected_points
tier
bye_week
injury_status
consensus_adp
yahoo_adp
espn_adp
sleeper_adp
```

The MVP should use an existing current fantasy-football dataset.

Building a proprietary projection model is outside the scope of the initial project.

---

## 12. Remaining Player Pool

Once drafted players are resolved, the system should remove them from the canonical player pool.

Conceptually:

```python
available_players = all_players - drafted_players
```

The recommendation engine should only evaluate players who remain available.

The system should also preserve the full drafted list because it may be useful for:

- Positional scarcity analysis
- Opponent behavior modeling
- Draft-board visualization
- Estimating which positions are likely to be selected before the user's next pick

---

## 13. User Roster State

The user's roster must be tracked separately from the overall drafted-player set.

Example:

```json
{
  "my_roster": [
    {
      "player": "Jahmyr Gibbs",
      "position": "RB",
      "overall_pick": 7
    },
    {
      "player": "Nico Collins",
      "position": "WR",
      "overall_pick": 19
    }
  ]
}
```

This enables roster-aware recommendations.

For example, a user with:

```text
RB
RB
RB
```

may receive a different recommendation than a user with:

```text
WR
RB
TE
```

even when the same players remain available.

---

## 14. Recommendation Logic

The MVP should use a transparent scoring model rather than asking the LLM to invent rankings.

Conceptually:

```text
recommendation_score =
    player_value
  + adp_value
  + positional_need
  + positional_scarcity
  + wait_risk
```

### Player Value

Represents the player's underlying fantasy value.

Possible sources:

- Consensus ranking
- Projected points
- Expert ranking
- Tier

### ADP Value

Measures how far a player has fallen relative to market expectations.

Example:

```text
Current pick: 31
Player ADP: 20

Player has fallen 11 picks.
```

This may represent positive draft value.

### Positional Need

Adjusts recommendations based on the user's existing roster.

Example:

```text
Current roster:
RB
RB

Available:
RB ranked 16
WR ranked 18
```

The WR may become the preferred recommendation because of roster construction.

### Positional Scarcity

Measures how quickly talent drops after the current player or tier.

Example:

```text
WR Tier 2:
Player A
Player B

WR Tier 3:
Player C
Player D
Player E
```

If Player B is the final Tier 2 receiver, waiting may have a larger opportunity cost.

### Wait Risk

Estimates the probability that the player will be selected before the user's next pick.

This is one of DraftSense's core differentiators.

---

## 15. Slot-Aware Recommendation

DraftSense should not merely recommend the highest-ranked available player.

It should consider the user's next selection.

Example:

```text
Current pick: 31
Next user pick: 42

Nico Collins
Composite score: 92
Estimated chance of reaching pick 42: 14%

Josh Jacobs
Composite score: 89
Estimated chance of reaching pick 42: 61%
```

Recommended response:

```text
Recommended Pick: Nico Collins

Reason:
Nico Collins has slightly greater overall value and is unlikely
to survive until your next selection.

Josh Jacobs is a strong alternative, but the model estimates a
much greater chance that Jacobs remains available at pick 42.

TAKE: Nico Collins
WAIT candidate: Josh Jacobs
```

This converts the recommendation from simple ranking into an opportunity-cost decision.

---

## 16. Opponent Draft Simulation

Other draft slots do not need to be controlled by LLM agents.

Opponent selections should initially be simulated using deterministic or probabilistic rules.

Conceptually:

```text
Opponent Pick =
    ADP preference
  + positional preference
  + roster need
  + small randomness
```

A simple implementation could build a candidate pool around the current pick:

```python
candidate_pool = players_near_adp(
    current_pick=current_pick,
    tolerance=8
)
```

Then sample from that candidate pool using weighted probability.

This prevents every simulation from generating an identical draft board.

---

## 17. Player Survival Probability

A stretch version of the recommendation engine should simulate the selections between:

```text
current_pick
```

and:

```text
next_user_pick
```

Multiple simulations can estimate:

```text
P(player survives until next user pick)
```

Example:

```text
Nico Collins: 14%
Josh Jacobs: 61%
Drake London: 38%
```

This enables DraftSense to reason about:

> Take now versus wait.

The MVP can begin with a simpler heuristic and add Monte Carlo simulation if time permits.

---

## 18. Expected Recommendation Output

Example:

```text
Recommended Pick: Nico Collins

Why:
- Highest composite value among remaining candidates
- Adds WR strength to a roster currently containing an RB
- Current WR tier is close to ending
- Nico Collins is unlikely to survive until your next selection

Next Pick:
2.06 — 19th overall

Alternatives:

1. Josh Jacobs
   - Strong RB value
   - More likely to survive until your next pick

2. Drake London
   - Strong WR alternative
   - Slightly lower value than Collins

3. Brock Bowers
   - Positional advantage at TE
   - Higher opportunity cost if the TE tier disappears
```

---

## 19. System Architecture

```text
                    +----------------------+
                    |      User Input      |
                    |----------------------|
                    | League Size          |
                    | Scoring Format       |
                    | Draft Slot           |
                    | Messy Draft Text     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | LLM Extraction Layer |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Player Name Resolver |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Draft-State Validator|
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Canonical Draft State|
                    +----------+-----------+
                               |
                +--------------+--------------+
                |                             |
                v                             v
      +-------------------+         +-------------------+
      | Player Dataset    |         | Snake Draft Logic |
      | Rankings / ADP    |         | Next Pick         |
      +---------+---------+         +---------+---------+
                |                             |
                +--------------+--------------+
                               |
                               v
                    +----------------------+
                    | Recommendation Engine|
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Agent Explanation    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Recommendation       |
                    +----------------------+
```

---

## 20. LLM Responsibilities

The LLM should be used where language ambiguity exists.

The LLM should handle:

- Extracting player references from messy text
- Identifying statements such as "I took Gibbs"
- Identifying league settings when stated naturally
- Converting natural-language draft descriptions into structured events
- Explaining deterministic recommendation results conversationally
- Answering strategy questions using tool outputs

Examples:

```text
Can I wait on this WR?
```

```text
What happens if I take another RB here?
```

```text
Why do you prefer Collins over Jacobs?
```

---

## 21. Deterministic Code Responsibilities

The LLM should not control core draft mathematics.

Application code should handle:

- Snake-draft order
- Pick ownership
- Player identity resolution
- Duplicate detection
- Draft-state validation
- Available-player calculation
- User-roster calculation
- ADP calculations
- Recommendation scoring
- Positional scarcity
- Player survival simulation
- Probability calculations

This separation improves:

- Reliability
- Testability
- Explainability
- Debugging
- Hallucination resistance

---

## 22. Initial Technical Components

Suggested project structure:

```text
draftsense/
|
|-- data/
|   `-- players.csv
|
|-- app.py
|-- parser.py
|-- resolver.py
|-- draft_state.py
|-- validator.py
|-- recommender.py
|-- simulator.py
|-- requirements.txt
`-- README.md
```

### `parser.py`

Responsibilities:

- Send unstructured text through the extraction process
- Return draft events
- Preserve pick order
- Identify potential user selections

### `resolver.py`

Responsibilities:

- Normalize names
- Match aliases
- Perform fuzzy matching
- Return canonical player IDs/names
- Track confidence

### `draft_state.py`

Responsibilities:

- Store league configuration
- Store selections
- Calculate rounds
- Calculate pick ownership
- Calculate the next user selection

### `validator.py`

Responsibilities:

- Detect impossible user picks
- Detect duplicates
- Detect missing or conflicting state
- Verify roster consistency

### `recommender.py`

Responsibilities:

- Rank remaining players
- Calculate composite recommendation score
- Account for user roster
- Account for scarcity
- Generate candidate rankings

### `simulator.py`

Responsibilities:

- Simulate opponent picks
- Add ADP randomness
- Estimate player survival probability

### `app.py`

Responsibilities:

- User interface
- Collect settings
- Accept pasted text
- Display parsed draft state
- Display recommendation
- Accept follow-up strategy questions

---

## 23. Out of Scope for Initial Build

The 2–4 hour MVP will not require:

- Automatic Yahoo drafting
- Automatic ESPN drafting
- Automatic Sleeper drafting
- OAuth
- Browser automation
- Multi-agent architecture
- Custom machine-learning player projections
- Historical model training
- Complex frontend development
- Full-season roster optimization
- Real-time websocket synchronization
- Proprietary fantasy ranking models

These may become future enhancements.

---

## 24. Stretch Goals

If the MVP is completed early:

- Monte Carlo draft simulation
- Player survival probabilities
- Position-tier visualization
- Draft-board visualization
- Saved draft sessions
- Scenario analysis
- Yahoo synchronization
- Sleeper synchronization
- Screenshot ingestion
- OCR-based board extraction
- Live draft-state synchronization

Potential strategy queries could include:

```text
What if I take RB here?
```

```text
Can I wait on QB?
```

```text
Which WR is least likely to come back to me?
```

```text
What position has the largest tier drop before my next pick?
```

---

## 25. Success Criteria

The MVP is successful if a user can:

1. Enter their league size.
2. Enter their scoring format.
3. Enter their draft slot.
4. Paste messy draft-room text.
5. Have the system identify drafted players.
6. Have the system correctly identify the user's selections.
7. Have player names normalized against the player dataset.
8. Have impossible draft states detected.
9. See which players remain available.
10. See the user's current roster.
11. See when the user picks next.
12. Receive a plausible next-pick recommendation.
13. Receive two or three alternatives.
14. Receive an explanation based on actual draft-state factors.
15. Add additional draft information and receive an updated recommendation.

---

## 26. 2–4 Hour Delivery Target

### Hour 1 — Draft State

Build:

- Player dataset ingestion
- Player model
- Snake-draft mathematics
- Draft-slot calculations
- User-roster state
- Player-name resolution

Goal:

```text
Raw player names -> canonical draft state
```

### Hour 2 — Extraction and Validation

Build:

- Unstructured-text extraction
- Draft-event parsing
- Validation rules
- Remaining-player calculation

Goal:

```text
Messy draft text -> validated current draft board
```

### Hour 3 — Recommendations

Build:

- Candidate scoring
- Roster-awareness
- Positional need
- Positional scarcity
- Recommendation explanation

Goal:

```text
Current board -> recommended next pick
```

### Hour 4 — Simulation and Interface

If time permits:

- Opponent pick simulation
- Survival probabilities
- Simple Streamlit interface
- Testing
- Demo polish

Goal:

```text
Current board -> TAKE vs WAIT recommendation
```

---

## 27. Final Deliverable

A working prototype centered around the interaction:

> Paste your draft so far -> reconstruct the board -> validate the state -> recommend your next pick.
