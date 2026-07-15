# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0** — a small, explainable, content-based music recommender.

---

## 2. Intended Use

VibeFinder takes a short "taste profile" (favorite genre, favorite mood, target energy, and
whether you like acoustic music) and returns a ranked list of songs from a small catalog, each
with a plain-English reason for why it was picked. It assumes the user can describe their taste
in those few fields and that a good recommendation is one whose attributes match that description.

This is a **classroom/learning simulation**, not a product. It's meant to show how data turns
into a ranked prediction and where bias creeps in — not to serve real listeners at scale.

---

## 3. How the Model Works

Think of it as a points game. Every song starts with zero points. If the song's genre is your
favorite, it earns 2 points. If its mood matches yours, it earns 1 more. Then it earns up to
1.5 points for how *close* its energy level is to the energy you're in the mood for — a perfect
match gets the full 1.5, a big mismatch gets almost nothing. Finally, if you said you like
acoustic music and the song is acoustic (or you don't and it isn't), it gets a small half-point
nudge. Once every song has its points, we sort them from most to fewest and show you the top few.

Compared to the starter code (which just returned the first few songs unchanged), I added real
weighted scoring, an energy "closeness" rule instead of a raw high/low comparison, and a reasons
list so each recommendation explains itself.

---

## 4. Data

The catalog has **18 songs**, each with genre, mood, energy, tempo, valence, danceability, and
acousticness. I expanded the starter set of 10 by adding 8 songs to widen the range of genres
(edm, hip hop, folk, classical, r&b, country, metal, reggae) and moods (euphoric, aggressive,
nostalgic, romantic, angry). It's still tiny and English-pop-leaning, so whole styles of music
(world, jazz standards, spoken word) and the way taste shifts by context (workout vs. sleep) are
missing. Numeric fields are on a 0.0–1.0 scale except tempo, which is in BPM.

---

## 5. Strengths

The system works well for users with a **clear, consistent** taste — the Chill Lofi and Deep
Intense Rock profiles both returned lists that genuinely felt right, with the acoustic/energy
signals lining up with what a human would expect. The energy-closeness rule is the standout: it
correctly separates low-energy and high-energy listeners into non-overlapping lists. And because
every pick comes with reasons, it's easy to trust or challenge — you can always see exactly which
rule earned the points.

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

1. **Soften genre matching** — give partial credit for related genres ("pop" ↔ "indie pop") and
   moods ("chill" ↔ "relaxed") instead of exact string matches.
2. **Score more features** — bring `valence` and `danceability` into the formula, and let users
   weight what matters to them (a "diversity mode" that penalizes repeating the same genre/artist
   in the top results would directly attack the filter bubble).
3. **Add a collaborative signal** — even a simple "people who liked X also liked Y" layer on a
   bigger catalog would let it surprise users with songs outside their stated taste.

---

## 9. Personal Reflection

The biggest thing I learned is that a "recommendation" doesn't need machine learning — a handful
of if-statements and a sort already *feel* like a smart suggestion once the reasons are shown.
What surprised me most was watching the same pop songs surface across unrelated profiles; it made
the idea of a filter bubble concrete, because I could point to the exact +2.0 genre weight that
caused it. AI tools helped me move fast on the CSV parsing and the Pythonic sorting, but I had to
double-check the scoring math myself — especially the energy "closeness" formula, where it's easy
to accidentally reward high energy instead of *matching* energy. This changed how I think about
apps like Spotify: behind the magic there are weighting choices someone made, and those choices
quietly decide what you do and don't get to hear.
