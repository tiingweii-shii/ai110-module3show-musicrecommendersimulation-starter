# 🎵 Music Recommender Simulation

## Project Summary

In this project I built **VibeFinder 1.0**, a small, explainable, content-based music
recommender. It reads a catalog of songs (with attributes like genre, mood, and energy),
compares each song to a user's "taste profile," and returns a ranked list of suggestions.
Crucially, every recommendation comes with **reasons** (e.g. `genre match (+2.0)`) so you can
see *why* a song was picked instead of trusting a black box.

The goals of the project were to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what my system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

---

## How The System Works

### How real platforms do it (research summary)

Big platforms like Spotify, YouTube, and TikTok mostly blend **two** families of techniques:

- **Collaborative filtering** — predicts what you'll like based on *other people's behavior*.
  If thousands of users who liked songs A and B also liked C, the system suggests C to anyone
  who liked A and B. It uses signals like plays, likes, skips, saves, playlist adds, and
  watch/listen time. Its strength is discovering non-obvious hits; its weakness is the
  "cold-start" problem — a brand-new song or user has no behavior history yet.
- **Content-based filtering** — predicts what you'll like based on the *attributes of the items*
  themselves (a song's genre, tempo, energy, "valence"/positivity, acousticness, etc.) matched
  against your past preferences. It handles new songs well and is easy to explain, but it tends
  to keep recommending "more of the same," creating a **filter bubble**.

Real systems combine both (a *hybrid* approach) and layer on deep-learning models trained on
huge interaction logs. **My simulation is purely content-based** — it's the simplest thing that
still shows the core idea of turning data into a ranked prediction, and it's fully explainable.

### What my version prioritizes

VibeFinder scores each song by how well its attributes match a user's stated taste, and ranks
the whole catalog from best match to worst. I prioritize **transparency** (every score is
broken down into human-readable reasons) and **"vibe" matching** — I lean on genre, mood, and
energy because in my own listening those three define a song's feel more than tempo alone.

### Features used

**`Song`** uses: `genre`, `mood`, `energy` (0.0–1.0), `tempo_bpm`, `valence` (positivity 0.0–1.0),
`danceability` (0.0–1.0), and `acousticness` (0.0–1.0).

**`UserProfile`** stores: `favorite_genre`, `favorite_mood`, `target_energy` (the energy level
they're in the mood for), and `likes_acoustic` (a boolean nudge toward/away from acoustic songs).

The **`Recommender`** computes a numeric score per song from these (see the Algorithm Recipe
below), then chooses the top *k* songs by score.

### Algorithm Recipe

Each song starts at a score of **0.0**. Then:

| Rule | Points | Why |
|------|--------|-----|
| **Genre match** (song genre == favorite genre) | **+2.0** | Genre is the strongest signal of taste, so it's worth the most. |
| **Mood match** (song mood == favorite mood) | **+1.0** | Mood matters, but a happy pop song and a happy country song can both fit. |
| **Energy closeness** | **+1.5 × (1 − \|song.energy − target_energy\|)** | Rewards songs whose energy is *close* to the target — not just high energy. A perfect energy match adds 1.5; a total mismatch adds ~0. |
| **Acoustic preference** | **+0.5** | If `likes_acoustic` is true and the song's acousticness ≥ 0.6 (or the user dislikes acoustic and the song is ≤ 0.3), nudge the score. |

**Ranking Rule:** score *every* song in the catalog with the rule above, then sort from highest
to lowest score and return the top *k*. Scoring judges one song; ranking orders the whole list —
you need both.

**Example user profile** (the default): `favorite_genre="pop"`, `favorite_mood="happy"`,
`target_energy=0.8`, `likes_acoustic=False`. This should surface upbeat, high-energy pop like
*Sunrise City* while pushing calm acoustic tracks like *Moonlit Adagio* to the bottom.

### Expected biases (before testing)

- **Genre dominance:** because a genre match is worth twice a mood match, I expect songs in the
  user's favorite genre to crowd the top even when an out-of-genre song fits the mood/energy
  better. This is a built-in filter bubble.
- **Small-catalog skew:** with only ~18 songs and several `lofi`/`pop` entries, popular genres
  have more chances to appear; rare genres (metal, reggae) may almost never surface unless
  requested directly.
- **Middle-energy blind spot:** the energy term rewards closeness, so users wanting extreme
  energy (0.0 or 1.0) get sharper separation than users targeting 0.5, where many songs cluster.

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

Running `python -m src.main` with the default "High-Energy Pop" profile produces:

```
Loaded songs: 18

============================================================
Profile: High-Energy Pop (default)
  prefs: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}
============================================================
1. Sunrise City — Neon Echo [pop/happy]  Score: 4.97
     Because: genre match (+2.0), mood match (+1.0), energy close to 0.80 (+1.47), non-acoustic song as preferred (+0.5)
2. Gym Hero — Max Pulse [pop/intense]  Score: 3.80
     Because: genre match (+2.0), energy close to 0.80 (+1.30), non-acoustic song as preferred (+0.5)
3. Rooftop Lights — Indigo Parade [indie pop/happy]  Score: 2.44
     Because: mood match (+1.0), energy close to 0.80 (+1.44)
4. Dust and Diesel — Cody Rains [country/happy]  Score: 2.26
     Because: mood match (+1.0), energy close to 0.80 (+1.26)
5. Concrete Verses — MC Grid [hip hop/aggressive]  Score: 1.98
     Because: energy close to 0.80 (+1.48), non-acoustic song as preferred (+0.5)
```

---

## Experiments You Tried

**Weight-shift experiment.** I halved the genre weight (2.0 → 1.0) and doubled the energy weight
(1.5 → 3.0), then re-ran the default `pop/happy/0.8` profile:

```
1. Sunrise City       [pop/happy]        energy=0.82  score=5.44
2. Gym Hero           [pop/intense]      energy=0.93  score=4.11
3. Rooftop Lights     [indie pop/happy]  energy=0.76  score=3.88
4. Dust and Diesel    [country/happy]    energy=0.64  score=3.52
5. Concrete Verses    [hip hop/aggressive] energy=0.79 score=3.47
```

The two pop songs still lead, but the *gap* between them and the out-of-genre songs collapses
(4.97 → 5.44 vs. 2.44 → 3.88). Lesson: the original 2.0 genre weight was the main force creating
a "pop bubble." When energy dominates, songs from country, indie pop, and hip hop with the right
energy climb into contention — the results become **more diverse but less genre-loyal**.

**Profile diversity.** Swapping profiles (Chill Lofi vs. Deep Intense Rock) cleanly flips the
rankings: lofi/acoustic tracks top one list and none appear in the other. This confirms the
scoring actually responds to preferences rather than always returning the same "popular" songs.

---

## Limitations and Risks

- **Tiny catalog (18 songs).** Rankings are fragile — one song can dominate a whole category.
- **Genre bubble.** A genre match (+2.0) outweighs a mood match (+1.0), so it favors "more of
  the same genre" over songs that fit the user's actual vibe. This is a classic filter bubble.
- **Exact-match only.** Genre/mood must match *exactly* ("pop" ≠ "indie pop", "chill" ≠
  "relaxed"), so near-misses get zero credit even when they'd fit.
- **Ignores most features.** `tempo_bpm`, `valence`, and `danceability` are in the data but not
  yet scored, and it has no idea about lyrics, language, or the user's listening history.
- **No collaborative signal.** It can't learn from other listeners, so it never surprises you
  with something outside your stated taste.

I go deeper on these in the [model card](model_card.md).

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



