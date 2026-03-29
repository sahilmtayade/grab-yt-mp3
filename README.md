# grab-yt-mp3

A beautiful interactive command-line tool to search and download high-quality MP3s from YouTube Music directly to your local machine.

## Features

- **Interactive Search**: Search for songs on YouTube Music and choose from top results.
- **High-Quality Audio**: Automatically extracts and converts the best available audio to MP3.
- **Rich Metadata & Cover Art**: Embeds artist, album, and thumbnail cover art directly into the downloaded MP3.
- **Cross-Platform**: Works on Windows, macOS, and Linux.
- **Direct Query**: Pass search queries directly via command-line arguments.

_(Note: Requires `ffmpeg` to be installed and available in your system's PATH.)_

## Installation

### Prerequisites

1. **Python 3.14+**
2. **FFmpeg** (Required for audio extraction and metadata embedding)
   - Windows: `winget install ffmpeg` or via [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

### Using `uv` (Recommended)

**To install from PyPI (Once published):**

```bash
uv tool install grab-yt-mp3
```

**To install locally from source (After cloning the repo):**

```bash
uv tool install .
```

### Using `pip`

```bash
pip install -e .
```

## Usage

You can launch the tool simply by typing:

```bash
ytdl
```

Or you can pass a search query directly:

```bash
ytdl "Never Gonna Give You Up"
```

You can also pass a direct YouTube link as a positional argument to skip the interactive search:

```bash
ytdl "https://music.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Help

```bash
ytdl --help
```

## Development

To setup the development environment:

```bash
uv sync --all-groups
# run the project with:
uv run ytdl
```

## License

MIT License
