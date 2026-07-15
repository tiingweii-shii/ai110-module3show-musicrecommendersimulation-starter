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

<!-- Algorithm Recipe added in Phase 2 -->

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
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
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



