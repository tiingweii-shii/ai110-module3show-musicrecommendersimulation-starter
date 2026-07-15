# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias

The biggest bias I found is **genre dominance**. A genre match is worth +2.0 while a mood match
is only +1.0, so the system prefers "another song in your favorite genre" over a song that
actually matches the mood and energy you asked for. In my stress tests this created a filter
bubble: the default pop fan almost never sees a great non-pop song even when its vibe fits
better. The **adversarial profile** (wanting an *intense, high-energy, acoustic ambient* track)
exposed this clearly — the top result was a calm, low-energy ambient song that matched only on
genre and acoustic-ness, completely ignoring the "intense" and "high-energy" wishes.

Other limitations: the system does exact string matching, so "pop" and "indie pop" (or "chill"
and "relaxed") are treated as unrelated. It ignores `tempo_bpm`, `valence`, and `danceability`
even though they're in the data. And with only 18 songs, underrepresented genres like metal and
reggae rarely surface unless a user asks for them by name, so those listeners get thin results.

---

## 7. Evaluation

I tested four profiles: **High-Energy Pop** (default), **Chill Lofi**, **Deep Intense Rock**,
and an **adversarial "Intense Acoustic Ambient"** profile with conflicting wishes. For each I
ran `python -m src.main` and read the top-5 plus their reasons to check the picks made sense.

I also ran a **weight-shift experiment**: halving the genre weight and doubling the energy weight.
The top two pop songs stayed on top, but the score gap to out-of-genre songs shrank a lot, which
told me the 2.0 genre weight was the main thing creating the "pop bubble."

**Profile comparisons (why the outputs differ):**

- **Chill Lofi vs. Deep Intense Rock** — Lofi surfaces calm, acoustic tracks (*Library Rain*,
  *Midnight Coding*, energy ~0.4); Rock surfaces loud, high-energy tracks (*Storm Runner*,
  *Gym Hero*, energy ~0.9) with zero lofi songs. This is the clearest sign the energy term works:
  the two lists share nothing because the users want opposite energy levels.
- **High-Energy Pop vs. Deep Intense Rock** — Both want high energy, so *Gym Hero* and
  *Sunrise City* appear on both lists, but the genre bonus swaps who's #1 (*Sunrise City* for pop,
  *Storm Runner* for rock). Same energy, different genre loyalty.
- **Adversarial vs. Deep Intense Rock** — Both ask for "intense" and high energy, yet the
  adversarial list is topped by a *calm ambient* song purely because ambient is its favorite
  genre. Comparing these two shows how a single strong genre weight can override every other
  signal — exactly the bias described in §6.

**What surprised me:** how quickly the same handful of pop songs showed up across unrelated
profiles. It made the "filter bubble" idea concrete: a simple weighting choice, not any fancy
model, was enough to bias the results.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
