import argparse
from ytmusicapi import YTMusic
import unicodedata
from fuzzywuzzy import fuzz
import time


def normalize_text(text):
    """Normalize text to remove special characters and accents."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()


def create_playlist_from_file(file_path, playlist_name, fuzziness, playlist_description="Created by script"):
    # Initialize YTMusic with your headers
    ytmusic = YTMusic("headers.json")
    
    # Read song names from the text file
    try:
        with open(file_path, "r") as file:
            songs = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

    # Create a new playlist
    playlist_id = ytmusic.create_playlist(playlist_name, playlist_description)
    print(f"Created playlist '{playlist_name}' with ID: {playlist_id}")

    unmatched_songs = []  # To log songs that weren't confidently matched
    added_songs = 0       # Track successful additions

    # Search and add songs
    for song in songs:
        print(f"\nSearching for: {song}")
        normalized_query = normalize_text(song)
        search_results = ytmusic.search(normalized_query, filter="songs")
        
        if search_results:
            result = search_results[0]
            title = normalize_text(result['title'])
            artist = normalize_text(result['artists'][0]['name']) if result['artists'] else "unknown artist"

            # Compute fuzzy match scores
            title_score = fuzz.ratio(normalized_query, title)
            artist_score = fuzz.ratio(normalized_query, artist)

            # Debugging: Log normalized values and scores
            print(f"Normalized Query: '{normalized_query}', Title: '{title}', Artist: '{artist}'")
            print(f"Fuzzy Match Scores -> Title: {title_score}, Artist: {artist_score}")

            # Match threshold is set by the `fuzziness` argument
            if title_score >= fuzziness or artist_score >= fuzziness:
                print(f"Adding: {result['title']} by {result['artists'][0]['name']}")
                ytmusic.add_playlist_items(playlist_id, [result['videoId']])
                added_songs += 1
            else:
                print(f"No strong match for: {song}. Found: {result['title']} by {result['artists'][0]['name']}. Logging for review.")
                unmatched_songs.append(f"{song} -> {result['title']} by {result['artists'][0]['name']}")
        else:
            print(f"No results found for: {song}")
            unmatched_songs.append(f"{song} -> No results found")

        # Optional: Delay between requests to avoid rate-limiting
        time.sleep(1)

    print(f"\nPlaylist creation complete! Added {added_songs}/{len(songs)} songs successfully.")

    return unmatched_songs


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Create a YouTube Music playlist from a text file.")
    parser.add_argument("file", help="Path to the text file containing song titles.")
    parser.add_argument("playlist_name", help="Name of the playlist to create.")
    parser.add_argument("--fuzziness", type=int, default=40, help="Fuzziness threshold for matching (default: 50).")
    parser.add_argument("--description", default="Created by script", help="Playlist description (optional).")

    args = parser.parse_args()

    # Call the function with arguments
    unmatched_songs = create_playlist_from_file(args.file, args.playlist_name, args.fuzziness, args.description)

    # Analyze unmatched songs
    if unmatched_songs:
        match_scores = []
        for entry in unmatched_songs:
            parts = entry.split("->")
            if len(parts) == 2:
                song = parts[0].strip()
                result = parts[1].strip()

                normalized_query = normalize_text(song)
                if " by " in result:
                    title = normalize_text(result.split(" by ")[0])
                    artist = normalize_text(result.split(" by ")[1])
                else:
                    title = normalize_text(result)
                    artist = "unknown artist"

                title_score = fuzz.ratio(normalized_query, title)
                artist_score = fuzz.ratio(normalized_query, artist)
                match_scores.append((song, title_score, artist_score))

        avg_title_score = sum(score[1] for score in match_scores) / len(match_scores) if match_scores else 0
        avg_artist_score = sum(score[2] for score in match_scores) / len(match_scores) if match_scores else 0
        print(f"\nAverage Fuzzy Scores for Unmatched Songs -> Title: {avg_title_score:.2f}, Artist: {avg_artist_score:.2f}")
    else:
        print("\nNo unmatched songs to analyze.")
