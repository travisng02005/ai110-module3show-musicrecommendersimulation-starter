# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

Wavelink
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

The intended use is for a person who understands their taste in music and what their user profile may be, and the app makes recommendations of songs based on that data. The assumption that it makes is that the user will like these songs because they fit the sounds that they like and not just because of other reasons. This is more for classroom exploration than actual user.
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Song features used: Each song's genre, mood, energy, valence, danceability and acousticness. Tempo (BPM) is loaded and can be targeted, but it has a weight of 0, so it doesn't affect scores.

User preferences considered: One or more favorite genres and moods, plus optional targets for energy, valence, danceability and acousticness. A simple "likes acoustic" setting maps to an acousticness target of 0.8 or 0.2. Any preference the user leaves out is skipped.

How the score works: Each song gets a 0 to 1 match for every feature the user specified.

Genre and mood: An exact match scores 1.0, a related pair (e.g. lofi/ambient, chill/relaxed) scores 0.6, and anything else scores 0.
Numeric features: The match is 1 - |song value - target|, so closer values score higher.

The model works buy first digesting the songs that we input and breaking them down to understand them based on their characteristics, then compares the numbers to the user profiles preferences. After that it makes suggestions to the user based off of what songs match the best.
---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

Genres and moods represented: The dataset has 15 songs across 12 genres: lofi (3), pop (2), and one each of rock, ambient, jazz, synthwave, indie pop, hip hop, folk, r&b, EDM and classical. It has 11 moods: chill (3), happy (2), intense (2), and one each of relaxed, moody, focused, confident, nostalgic, romantic, euphoric and sad. Lofi and chill are over-represented, and most genres and moods appear only once.

Did you add or remove data: I added 5 songs and removed none. The starter had 10 songs (ids 1 to 10), and I added ids 11 to 15: Concrete Echoes (hip hop), Porch Light Hymn (folk), Velvet Hours (r&b), Neon Pulse Festival (EDM) and Rain on Old Piano (classical). The additions fill genres and moods the starter lacked, including very low energy (0.18), very high energy (0.96) and high acousticness (0.97). I didn't change any of the original 10 rows.

Parts of musical taste missing:
    Genres: There is no country, metal, Latin, K-pop, Afrobeats, reggae, blues or world music. The list reflects mainstream Western genres.
    Moods: Every song has a single mood label, so mixed moods (e.g. bittersweet) can't be expressed. There is also no angry, playful or spiritual mood.
    Missing song attributes: Lyrics and language, vocals vs instrumental, era or decade, artist popularity and cultural context.
    Depth: With one or two songs per genre, a user who likes a genre can't get a varied list from it.
    No listening history: There is no data on skips, replays or context such as workout or commute
---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

User types it handles well: It works for users with a clear, well-represented taste, where genre, mood and energy all point the same way.

Patterns the scoring captures correctly:
    Songs that match on several features rank above partial matches. In every profile the top picks match genre, mood and energy together, and they hold their place even when the weights change.
    Related genres and moods earn partial credit. In the workout profile, EDM/euphoric correctly lands at #3, below the exact matches but above unrelated pop and indie pop songs. For the chill user, jazz/relaxed takes #5 as a reasonable adjacent pick.
    Energy and acousticness separate moods well. High-energy, low-acoustic songs go to the workout user, and quiet, acoustic ones go to the wind-down user, with no cross-over between the two.
    The explanations show why a song ranked where it did, such as "genre match (lofi); mood match (chill); energy close to target".

Cases that matched my intuition:
    Gym Hero and Storm Runner topping the workout list, and Rain on Old Piano and Porch Light Hymn topping the wind-down list.
    Spacewalk Thoughts (ambient/chill) appearing for both the chill user and the wind-down user, since it is quiet, acoustic and low energy.
    Dropping the genre weight from 0.30 to 0.15 made less relevant songs rise, such as the r&b song for the folk and classical listener. That supported keeping genre as a major signal.
---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

Genre carries the largest single weight (0.30), so a song's genre label alone can outweigh how well it matches the user on energy, mood or acousticness. A song outside the user's genres loses up to 30% of its possible score no matter how well it fits the rest of their taste. Genre is also a rough, one-label-per-song category, so this rule can bury good cross-genre matches like the jazz and ambient songs that suit a lofi listener. It also keeps recommendations inside the genres the user already named, which is the filter bubble.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

Profiles tested: Chill study (lofi/ambient, chill/focused, energy 0.4, acousticness 0.8), Intense workout (rock/pop, intense, energy 0.92, acousticness 0.1), and Rainy-day wind down (folk/classical, nostalgic/sad, energy 0.3, valence 0.4, acousticness 0.92).

Profile comparisons:

Chill study vs Intense workout: The two top 5 lists share no songs. Chill study returns lofi and ambient tracks with energy between 0.28 and 0.42 and acousticness between 0.71 and 0.92. The workout profile returns pop, rock and EDM tracks with energy between 0.76 and 0.96 and acousticness at or below 0.35. This makes sense because the profiles disagree on every feature the model scores, so a valid system should keep them completely apart.

Chill study vs Rainy-day wind down: These two overlap on Spacewalk Thoughts (ambient/chill), which makes sense because it is quiet, low energy and highly acoustic, and ambient is related to both lofi and classical. What changed is the genre and mood. Chill study ranks lofi first, while wind down moves to classical and folk with sad and nostalgic moods. Rain on Old Piano ranks first for wind down because its low valence (0.22) fits that user's lower valence target of 0.4, and it does not appear for chill study at all. The wind down list also falls off faster (0.95 for the top two, then 0.61 and 0.44), because the catalog only has one folk and one classical song, so after the exact matches the model is filling with weaker picks.

Intense workout vs Rainy-day wind down: These are opposite ends of the catalog (energy 0.92 vs 0.3, acousticness 0.1 vs 0.92), and again there is no overlap in the top 4. Workout fills with loud, danceable, electronic-sounding songs and wind down with quiet, acoustic ones, which is what the preferences ask for. The one shared song, Rooftop Lights (indie pop/happy), shows up at #5 in both with low scores (0.58 and 0.43). It is a leftover from the related-genre map (indie pop is linked to pop, rock and folk) and not a real match for either user, so it is a weakness and not a sign that the profiles are similar.

Overall, the outputs change in the directions the preferences predict, which suggests the scoring tests what it is meant to. The main caveat is that the lower ranks (4 and 5) are weak and reflect how small the catalog is.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

Next Up:
    Give tempo a real weight so a tempo target changes the score.
    Add features the catalog lacks, such as vocals vs instrumental, language and era.
    Support "avoid" preferences like disliked genres or moods.
    Allow multiple moods per song instead of one label.
    Show each feature's contribution to the score in the explanations.
    Warn the user when their genre isn't in the catalog.
    Cap songs per artist or genre in the top results to add diversity.
    Reserve one slot for an off-profile pick to counter the filter bubble.
    Support multiple taste clusters per user and sharpen the numeric scoring with a steeper falloff.
    Expand the catalog beyond 15 songs and add more test profiles, including conflicting tastes.
---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Recommender systems work with different characteristics and queues, giving each one a different weight on how much they care about that certain aspect. It is interesting how different models choose what to prioritize over others making each system unique.
This helped me understand how Spotify suggests me songs especially through things like DJ X. I will definitely be more conscious about how my queues(likes, dislikes, skips) effect my recommeneded songs.

My biggest learning moment was using the AI agent to find holes in my model and using it to fix them as well. I used AI agents to implement my functions as well as help me brain storm my algorithm and weighting logic. It surprised me how many categories songs can fall into and how they can be broken down into so many different characteristics. If I were to extend this project I would increase the dataset and fill in the gaps and holes when it comes to biases and blind spots in the recommenders logic.