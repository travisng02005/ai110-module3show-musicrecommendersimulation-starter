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

Songs in this system are represented by three scored features — genre, mood, and energy — plus supporting metadata (title, artist, tempo, valence, danceability, acousticness) that aren't scored directly but could be used in future iterations. Each UserProfile stores a matching preference for each scored feature: favorite_genre, favorite_mood, and target_energy.

The Recommender scores a song using the following weighted recipe:

Algorithm Recipe:

Genre match: +2.0 points if song.genre == user.favorite_genre, else +0
Mood match: +1.0 point if song.mood == user.favorite_mood, else +0
Energy similarity: up to +1.0 point, scaled by how close the song's energy is to the user's target — 1.0 * (1 - abs(song.energy - user.target_energy)) — so a perfect match earns the full point and the score falls off smoothly as the gap grows
These three components are summed into a single overall score. Genre and mood are treated as categorical (all-or-nothing), while energy is continuous and gets partial credit for "close enough" matches rather than requiring an exact hit. The recommender then ranks all songs by descending score and returns the top k, pairing each with a plain-language explanation built from which factors matched.

Potential biases:
Genre is weighted twice as heavily as mood (2.0 vs 1.0), which means a song that perfectly matches the user's mood but falls in a different genre can still be out-ranked by a song that only matches genre. This risks over-prioritizing genre and burying great mood-matches — e.g. a "happy" song in an unfamiliar genre may score lower than a "sad" song in the user's favorite genre. The system also treats every genre/mood label as equally distinct (no partial credit for "related" genres like pop vs indie pop), which can unfairly penalize near-matches. Because the catalog is small and hand-labeled, these effects are also amplified — a differently curated or larger catalog might expose the weighting choices very differently.
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
Top Recommendations
===================

1. Sunrise City (Score: 3.98)
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+0.98)

2. Gym Hero (Score: 2.87)
   Reasons: genre match (+2.0), energy similarity (+0.87)

3. Rooftop Lights (Score: 1.96)
   Reasons: mood match (+1.0), energy similarity (+0.96)

4. Night Drive Loop (Score: 0.95)
   Reasons: energy similarity (+0.95)

5. Storm Runner (Score: 0.89)
   Reasons: energy similarity (+0.89)
```
Top Recommendations
===================

1. Iron Collapse (Score: 2.13)
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+-0.87)

2. Spacewalk Thoughts (Score: -0.18)
   Reasons: energy similarity (+-0.18)

3. Autumn Sonata (Score: -0.20)
   Reasons: energy similarity (+-0.20)

4. Library Rain (Score: -0.25)
   Reasons: energy similarity (+-0.25)

5. Coffee Shop Stories (Score: -0.27)
   Reasons: energy similarity (+-0.27)
```
Top Recommendations
===================

1. Storm Runner (Score: 3.41)
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+0.41)

2. Gym Hero (Score: 1.43)
   Reasons: mood match (+1.0), energy similarity (+0.43)

3. Iron Collapse (Score: 0.47)
   Reasons: energy similarity (+0.47)

4. Sunrise City (Score: 0.32)
   Reasons: energy similarity (+0.32)

5. Rooftop Lights (Score: 0.26)
   Reasons: energy similarity (+0.26)
```
Top Recommendations
===================

1. Midnight Coding (Score: 3.98)
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+0.98)

2. Library Rain (Score: 3.95)
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (+0.95)

3. Focus Flow (Score: 3.00)
   Reasons: genre match (+2.0), energy similarity (+1.00)

4. Spacewalk Thoughts (Score: 1.88)
   Reasons: mood match (+1.0), energy similarity (+0.88)

5. Coffee Shop Stories (Score: 0.97)
   Reasons: energy similarity (+0.97)
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



