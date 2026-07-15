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

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    print_recommendations("High-Energy Pop (default)", user_prefs, songs, k=5)


if __name__ == "__main__":
    main()
