"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top-k recommendations for one profile in a readable layout."""
    print("=" * 60)
    print(f"Profile: {label}")
    print(f"  prefs: {user_prefs}")
    print("=" * 60)
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} — {song['artist']} "
              f"[{song['genre']}/{song['mood']}]  Score: {score:.2f}")
        print(f"     Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # A set of diverse profiles to stress-test the scoring logic.
    profiles = {
        "High-Energy Pop (default)":
            {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
        "Chill Lofi":
            {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
        "Deep Intense Rock":
            {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
        # Adversarial: wants an acoustic, high-energy, "intense" ambient track — but ambient
        # in the catalog is calm and low-energy, so these preferences conflict on purpose.
        "Adversarial: Intense Acoustic Ambient":
            {"genre": "ambient", "mood": "intense", "energy": 0.95, "likes_acoustic": True},
    }

    for label, user_prefs in profiles.items():
        print_recommendations(label, user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
