import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# --- Scoring weights (the "Algorithm Recipe") ---
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.5
ACOUSTIC_WEIGHT = 0.5


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _score_features(
    genre: str,
    mood: str,
    energy: float,
    acousticness: float,
    pref_genre: Optional[str],
    pref_mood: Optional[str],
    target_energy: Optional[float],
    likes_acoustic: Optional[bool],
) -> Tuple[float, List[str]]:
    """Core weighted scoring shared by the dict and OOP APIs; returns (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    if pref_genre is not None and genre == pref_genre:
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT})")

    if pref_mood is not None and mood == pref_mood:
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT})")

    if target_energy is not None:
        closeness = 1.0 - abs(energy - target_energy)  # 1.0 = perfect, ~0 = far
        points = ENERGY_WEIGHT * closeness
        score += points
        reasons.append(f"energy close to {target_energy:.2f} (+{points:.2f})")

    if likes_acoustic is not None:
        if likes_acoustic and acousticness >= 0.6:
            score += ACOUSTIC_WEIGHT
            reasons.append(f"acoustic song for acoustic fan (+{ACOUSTIC_WEIGHT})")
        elif not likes_acoustic and acousticness <= 0.3:
            score += ACOUSTIC_WEIGHT
            reasons.append(f"non-acoustic song as preferred (+{ACOUSTIC_WEIGHT})")

    return score, reasons


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score one Song against a UserProfile, returning (score, reasons)."""
        return _score_features(
            song.genre, song.mood, song.energy, song.acousticness,
            user.favorite_genre, user.favorite_mood,
            user.target_energy, user.likes_acoustic,
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked from highest to lowest score."""
        ranked = sorted(self.songs, key=lambda s: self._score(user, s)[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song scored as it did."""
        score, reasons = self._score(user, song)
        if not reasons:
            return f"No strong matches (score {score:.2f})."
        return f"Score {score:.2f}: " + ", ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts with numeric fields cast to numbers."""
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in int_fields:
                row[key] = int(row[key])
            for key in float_fields:
                row[key] = float(row[key])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song dict against a user_prefs dict; returns (score, reasons)."""
    target_energy = user_prefs.get("energy", user_prefs.get("target_energy"))
    return _score_features(
        song["genre"], song["mood"], song["energy"], song["acousticness"],
        user_prefs.get("genre"), user_prefs.get("mood"),
        target_energy, user_prefs.get("likes_acoustic"),
    )


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score and rank all songs, returning the top-k as (song, score, explanation) tuples."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
