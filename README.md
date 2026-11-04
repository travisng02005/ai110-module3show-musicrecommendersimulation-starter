# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Real-world recommendations are currated through signals such as likes, dislikes, which songs you skip, how the song is categorized, etc. My version will prioritize how the song sounds such as the bass and vibe.

Song features:
- id, title, artist
- genre
- mood
- energy
- acousticness
- tempo_bpm
- valence
- danceability
UserProfile Features:
- favorite_genre
- favorite_mood
- target_energy
- likes_acoustic

- Strategy: Normalized weights summing to 1 (#2) as the baseline, e.g. genre 0.30, mood 0.20, energy 0.20, valence/danceability/acousticness 0.10 each.
- Input: Load the 15 songs from songs.csv and take a user profile (target genre, mood, energy and so on).
Scoring:
- - Categorical features (genre, mood) get a match score.
- - Numeric features get 1 - |song - target|.
- - Multiply each by its weight and sum to one score in [0, 1].
- Output: Sort by score descending, return the top K (about 5) with a short reason for each.
- Experiments to compare later:
- - #3: energy-first weights.
- - #5: tiered mood similarity.
- - Optionally #6: a diversity penalty.
- Design choice: Keep weights in a single dict so strategies can be swapped without touching the scoring logic.
- Deliverable angle: Compare how the top 5 changes between weight sets, as a model-card discussion point.

Feature	Weight
genre	0.30
mood	0.20
energy	0.20
valence	0.10
danceability	0.10
acousticness	0.10

Potential Biases
- Genre dominance: At 0.30, a genre match can outrank a closer vibe match from another genre.
- Tiny catalog skew: 15 songs means many genres have exactly one entry (jazz, folk, r&b, edm, classical). A user wanting those gets one good result, then filler.
- Lofi overrepresentation: Three lofi songs (plus similar chill ones) will crowd the top 5 for anyone near low energy, which is a filter-bubble effect.
- Exact-match mood brittleness: Rare moods (romantic, euphoric, nostalgic) match only one song, so those users are underserved.
- Linear distance bias: 1 - |diff| gives generous credit to mediocre numeric matches and compresses the score range, so rankings can hinge on small differences.
- Mid-range target advantage: Users with targets near 0.5 are close to many songs, so they get inflated scores. Users at extremes (very high or very low energy) have fewer close options.
- Equal numeric weighting: Valence, danceability and acousticness are treated as equally important for everyone, though they matter differently per listener.
- Designer bias: The weights and the mood-similarity table are my choices, not learned from listening data, so they encode assumptions about what "similar" means.
- Artist repeats: LoRoom and Neon Echo each have multiple songs, so they can dominate without a diversity penalty.
- No feedback loop: The system never learns from skips or likes, so any bias in the weights persists.
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
============================================================
USER PROFILE: Intense workout (rock + pop)
============================================================
  Genres        rock, pop
  Moods         intense
  Energy        0.92
  Danceability  0.8
  Acousticness  0.1

TOP 5 RECOMMENDATIONS
------------------------------------------------------------
1. Gym Hero - Max Pulse
   pop / intense   Score: 0.98
   Because: genre match (pop); mood match (intense); energy close to target (0.93 vs 0.92); danceability close to target (0.88 vs 0.8); tempo close to target (132 vs 140); acousticness close to target (0.05 vs 0.1)
2. Storm Runner - Voltline
   rock / intense   Score: 0.98
   Because: genre match (rock); mood match (intense); energy close to target (0.91 vs 0.92); danceability close to target (0.66 vs 0.8); tempo close to target (152 vs 140); acousticness close to target (0.1 vs 0.1)
3. Neon Pulse Festival - Voltage Kid
   edm / euphoric   Score: 0.75
   Because: related genre (edm); related mood (euphoric); energy close to target (0.96 vs 0.92); danceability close to target (0.93 vs 0.8); tempo close to target (128 vs 140); acousticness close to target (0.03 vs 0.1)
4. Sunrise City - Neon Echo
   pop / happy   Score: 0.75
   Because: genre match (pop); energy close to target (0.82 vs 0.92); danceability close to target (0.79 vs 0.8); tempo close to target (118 vs 140); acousticness close to target (0.18 vs 0.1)
5. Rooftop Lights - Indigo Parade
   indie pop / happy   Score: 0.58
   Because: related genre (indie pop); energy close to target (0.76 vs 0.92); danceability close to target (0.82 vs 0.8); tempo close to target (124 vs 140)
```

```
============================================================
USER PROFILE: Chill study (lofi/ambient/jazz)
============================================================
  Genres        lofi, ambient
  Moods         chill, focused
  Energy        0.4
  Valence       0.6
  Acousticness  0.8
  Tempo         80

TOP 5 RECOMMENDATIONS
------------------------------------------------------------
1. Focus Flow - LoRoom
   lofi / focused   Score: 1.00
   Because: genre match (lofi); mood match (focused); energy close to target (0.4 vs 0.4); valence close to target (0.59 vs 0.6); tempo close to target (80 vs 80); acousticness close to target (0.78 vs 0.8)
2. Library Rain - Paper Lanterns
   lofi / chill   Score: 0.98
   Because: genre match (lofi); mood match (chill); energy close to target (0.35 vs 0.4); valence close to target (0.6 vs 0.6); tempo close to target (72 vs 80); acousticness close to target (0.86 vs 0.8)
3. Midnight Coding - LoRoom
   lofi / chill   Score: 0.98
   Because: genre match (lofi); mood match (chill); energy close to target (0.42 vs 0.4); valence close to target (0.56 vs 0.6); tempo close to target (78 vs 80); acousticness close to target (0.71 vs 0.8)
4. Spacewalk Thoughts - Orbit Bloom
   ambient / chill   Score: 0.95
   Because: genre match (ambient); mood match (chill); energy close to target (0.28 vs 0.4); valence close to target (0.65 vs 0.6); tempo close to target (60 vs 80); acousticness close to target (0.92 vs 0.8)
5. Coffee Shop Stories - Slow Stereo
   jazz / relaxed   Score: 0.75
   Because: related genre (jazz); related mood (relaxed); energy close to target (0.37 vs 0.4); valence close to target (0.71 vs 0.6); tempo close to target (90 vs 80); acousticness close to target (0.89 vs 0.8)
```

```
============================================================
USER PROFILE: Intense workout (rock + pop)
============================================================
  Genres        rock, pop
  Moods         intense
  Energy        0.92
  Danceability  0.8
  Acousticness  0.1
  Tempo         140

TOP 5 RECOMMENDATIONS
------------------------------------------------------------
1. Gym Hero - Max Pulse
   pop / intense   Score: 0.98
   Because: genre match (pop); mood match (intense); energy close to target (0.93 vs 0.92); danceability close to target (0.88 vs 0.8); tempo close to target (132 vs 140); acousticness close to target (0.05 vs 0.1)
2. Storm Runner - Voltline
   rock / intense   Score: 0.98
   Because: genre match (rock); mood match (intense); energy close to target (0.91 vs 0.92); danceability close to target (0.66 vs 0.8); tempo close to target (152 vs 140); acousticness close to target (0.1 vs 0.1)
3. Neon Pulse Festival - Voltage Kid
   edm / euphoric   Score: 0.75
   Because: related genre (edm); related mood (euphoric); energy close to target (0.96 vs 0.92); danceability close to target (0.93 vs 0.8); tempo close to target (128 vs 140); acousticness close to target (0.03 vs 0.1)
4. Sunrise City - Neon Echo
   pop / happy   Score: 0.75
   Because: genre match (pop); energy close to target (0.82 vs 0.92); danceability close to target (0.79 vs 0.8); tempo close to target (118 vs 140); acousticness close to target (0.18 vs 0.1)
5. Rooftop Lights - Indigo Parade
   indie pop / happy   Score: 0.58
   Because: related genre (indie pop); energy close to target (0.76 vs 0.92); danceability close to target (0.82 vs 0.8); tempo close to target (124 vs 140)
```

```
============================================================
USER PROFILE: Rainy-day wind down (folk/classical)
============================================================
  Genres        folk, classical
  Moods         nostalgic, sad
  Energy        0.3
  Valence       0.4
  Acousticness  0.92

TOP 5 RECOMMENDATIONS
------------------------------------------------------------
1. Rain on Old Piano - Clara Voss
   classical / sad   Score: 0.95
   Because: genre match (classical); mood match (sad); energy close to target (0.18 vs 0.3); valence close to target (0.22 vs 0.4); acousticness close to target (0.97 vs 0.92)
2. Porch Light Hymn - Willow & Pine
   folk / nostalgic   Score: 0.95
   Because: genre match (folk); mood match (nostalgic); energy close to target (0.45 vs 0.3); valence close to target (0.58 vs 0.4); acousticness close to target (0.91 vs 0.92)
3. Spacewalk Thoughts - Orbit Bloom
   ambient / chill   Score: 0.61
   Because: related genre (ambient); energy close to target (0.28 vs 0.3); acousticness close to target (0.92 vs 0.92)
4. Velvet Hours - Amber Lane
   r&b / romantic   Score: 0.44
   Because: related mood (romantic)
5. Rooftop Lights - Indigo Parade
   indie pop / happy   Score: 0.43
   Because: related genre (indie pop)
```
**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



