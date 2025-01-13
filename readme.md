# README: YouTube Music Playlist Maker

## Why You Need This

You know what’s annoying? Copy-pasting song titles into a playlist manually. Maybe you’ve got a list of 50+ songs from "Gerard's radio show" on Mixcloud (seriously, what *is* Mixcloud?), and you’re stuck turning it into something usable. Enter this script: your new playlist-making best friend. It takes your plain old text file and turns it into a YouTube Music playlist, no sweat.

It’s like having a DJ who never hogs the aux cable.

---

## Features

- **Easy Input**: Reads a text file with your favorite songs.
- **Automagic Matching**: Uses fuzzy logic to find the best matches on YouTube Music.
- **Playlist Creation**: Makes a fresh playlist, ready to rock.
- **Logging**: Tracks mismatches so you can fix the stragglers.

---

## What You’ll Need

1. **Python** (3.8+).
2. A virtual environment (optional, but recommended).
3. These Python packages:
   - `ytmusicapi`
   - `fuzzywuzzy`
   - `python-Levenshtein` (optional but faster).
4. A `headers.json` file from the YouTube Music API. Grab one using [this setup guide](https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html). Heads up: this step can get tricky because headers formatting can be "lumpy." Be patient—you’ve got this!

---

## How to Use

### The Command

```bash
python3 create_playlist.py <text_file> <playlist_name> [--fuzziness N]
```

### What Do These Mean?

- **`<text_file>`**: Path to your song list file (1 song per line).
- **`<playlist_name>`**: Name of your shiny new playlist.
- **`--fuzziness N`**: Optional. Sets how forgiving the matching should be (default: 50). Lower = more matches.

### Example

```bash
python3 create_playlist.py songs.txt "Party Playlist" --fuzziness 45
```

---

## Text File Format

- Each line should look like this:
  ```
  Artist - Song Title
  ```
- Example:
  ```
  Black Randy & The Metrosquad - I Wanna Be A Narc
  DJ Zenobia - Dance Da Ma Ju
  Posthuman - Acid Cranker
  ```

---

## How It Works

1. **Playlist Creation**: Names your playlist and logs its ID.
2. **Song Matching**: Searches YouTube Music for each song in your file.
3. **Fuzzy Logic**: Adds songs to your playlist if the title or artist is "close enough."
4. **Logging**: Saves unmatched songs to `unmatched_songs.txt` for review.

---

## Pro Tips

- **Start with Default Fuzziness**: If it’s skipping songs, lower the threshold (e.g., 45).
- **Check Unmatched Songs**: Open `unmatched_songs.txt` to see what didn’t make it.
- **Rate Limits**: The script waits 1 second between searches to keep YouTube happy. You can adjust this if you’re feeling brave.

---

## Example Output

```
Created playlist 'Party Playlist' with ID: PL12345...
Searching for: Black Randy & The Metrosquad - I Wanna Be A Narc
Matched: I Wanna Be a Nark by Black Randy And The Metrosquad
...
Playlist creation complete! Added 17/20 songs successfully.
```

---

## Troubleshooting

### It’s Slow

Install `python-Levenshtein` for faster fuzzy matching:

```bash
pip install python-Levenshtein
```

### It Missed a Good Match

Try lowering the fuzziness threshold:

```bash
--fuzziness 45
```

### Nothing Happened

Check your `headers.json` file and song list format. Make sure everything is in the right place.

---

## Extras

- Want to create multiple playlists at once? Add a loop.
- Need to recheck unmatched songs? Rerun with a lower fuzziness.

---

## License

Use it, share it, tweak it. Just don’t blame us if your playlist ends up full of "Baby Shark" remixes.
