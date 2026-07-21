# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

MoodMatcher
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

You tell it your favorite genre, mood, and energy level, and it picks the best-matching songs from a small 15-song catalog. It's a classroom project for learning how recommenders work, not a real music app.
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Every song earns points for matching your genre, fewer points for matching your mood, and a small bonus the closer its energy is to what you asked for. We kept the starter logic as-is and just sort by whichever songs earn the most total points.
---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 15 songs spread across 12 genres and 11 moods, so most genres only have one song in them. We didn't add or remove anything from the starter data with this few songs, most tastes outside of pop and lofi aren't really represented with any variety.
---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

It works best for genres with a few songs to actually compare, like pop and lofi, asking for chill lofi correctly surfaces mellow tracks, and asking for upbeat pop correctly surfaces energetic ones. The energy matching itself is intuitive: songs close to your target energy consistently score higher than songs far from it.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The scoring function weights genre match (+2.0) more heavily than energy similarity (max +1.0), which causes the system to systematically override a user's stated energy preference whenever their favorite genre has multiple candidates in the catalog. For example, a user who selects "pop" but requests low energy (e.g. energy: 0.1) still receives high-energy pop tracks like "Gym Hero" (energy 0.93) ranked above much better energy matches from other genres, because the genre bonus alone outweighs the energy penalty. This means the recommender treats genre as a near-absolute constraint rather than one signal among several, effectively ignoring nuanced or context-dependent requests (e.g. "calm pop for studying") from users whose genre is well-represented in the dataset. The bias is invisible in aggregate metrics because it only manifests as a systematic distortion in which songs within a genre get surfaced, not in whether genre matching works at all.
---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested the recommender against a baseline profile (genre: lofi, mood: chill, energy: 0.4) alongside adversarial profiles conflicting preferences, out-of-range energy values, missing/mistyped keys, and case-mismatched genre/mood strings to see whether the scoring function fails gracefully or produces silent nonsense. The baseline case revealed real sensitivity in the ranking: "Midnight Coding" beat "Library Rain" by only 0.03 points once their genre and mood bonuses tied, and hand-tracing a low-energy "pop" profile confirmed the genre bonus (+2.0) can override a much better energy fit, matching the bias documented under Limitations. The most surprising finding was that the "no matching factors" fallback in recommend_songs can never actually trigger, since the energy-similarity reason is always appended even when genre and mood both fail to match.

### Profile Comparisons

- Chill lofi vs. energetic pop asking for chill lofi songs surfaces mellow tracks like "Midnight Coding," and asking for high-energy pop surfaces upbeat ones like "Gym Hero." That part works the way you'd expect.

- Why "Gym Hero" keeps showing up when someone just wants Happy Pop the system scores "genre" (is it pop?) much higher than "mood" (does it feel happy?). "Gym Hero" is tagged pop, but its actual mood is "intense," not "happy" it's a gym-workout song, not a feel-good song. Because matching the genre is worth so many more points than matching the mood, "Gym Hero" still muscles its way near the top of pop recommendations even for someone who wants something cheerful, simply because it's pop, not because it fits the vibe. It's like asking for "something sweet" and getting handed any drink labeled "coffee," because the system cared more about the category than whether it actually tasted sweet.

- One-song genres act like a broken record a few genres (synthwave, metal, classical) only have one song each in our catalog. So no matter what mood or energy someone asks for, if they say that genre, they always get that same one song back. It's not really "recommending," it's just handing back the only option available.

- Same genre/mood, different energy target `{"genre": "lofi", "mood": "chill", "energy": 0.4}` and `{"genre": "lofi", "mood": "chill", "energy": 0.9}` both rank "Midnight Coding" (energy 0.42) above "Library Rain" (energy 0.35), but the winning margin shrinks from 0.07 to 0.03 in the first case and stays a full 0.07 in the second. That's because 0.4 falls between the two songs' energy values, so their distances to the target partially overlap, while 0.9 falls outside both values, so the gap between them is preserved in full. Same ranking, different margin a good reminder that the score gap communicates something different depending on where the target sits relative to the candidates, not just which song "wins."

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

- Definitely increase the dataset to include more songs.
- Be more descriptive on how the program judges and evaluates songs.
- Using plain language to explain why songs were recommended.
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

My biggest learning moment in this project was testing the different user_pref's and comparing the results to ensure if the results were reflecting what I was trying to accomplish. AI tools helped me with implementing my code and I had to ensure that the code made sense before allowing it to make changes. It surprised me how dumbed down the algorithms can seem to give these recommendations that seem like high levels of data went to making them. I would definitely try to increase the dataset and explain how the songs were suggested in plain language rather than showing the numbers.