# backup-yt

Full backup tool for YouTube channels: videos, thumbnails, titles, descriptions, tags and subtitles — powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Features

- Download every video from a channel, playlist, or a single video URL.
- Two modes: full video backup, or metadata-only (fast, low disk usage).
- Embeds thumbnail, subtitles and metadata directly into the video file.
- Saves per-video metadata as `.info.json` and `.description` files.
- Skips videos you already downloaded (resumable, safe to interrupt).
- Generates a `summary.json` and a `summary.csv` with every video's title, description, tags, URL and thumbnail.
- Colored console output (info / success / warning / error), no emojis.

## Requirements

- Python 3.9 or higher.
- [ffmpeg](https://ffmpeg.org/download.html) installed and available on your `PATH` (needed by yt-dlp to merge video/audio and embed thumbnails/subtitles).
- `yt-dlp` is installed automatically as a dependency of this package.

## Installation

From PyPI:

```bash
pip install backup-yt
```

From source (for development):

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/backup-yt.git
cd backup-yt
pip install -e .
```

## Usage

Once installed, the `backup-yt` command is available, or you can run the package directly with `python3 -m backup_yt`.

```bash
# Metadata and thumbnails only (fast, low disk usage)
backup-yt --url https://www.youtube.com/@MyChannel --metadata-only

# Full video backup at 1080p (default)
backup-yt --url https://www.youtube.com/@MyChannel

# Full video backup at 720p (less disk space)
backup-yt --url https://www.youtube.com/@MyChannel --quality 720

# A single playlist
backup-yt --url "https://www.youtube.com/playlist?list=PLxxxx"
```

### Options

| Flag | Description | Default |
|---|---|---|
| `--url` | URL of the channel, playlist or video (required) | — |
| `--metadata-only` | Only download metadata and thumbnails, skip the video file | off |
| `--quality` | Max video quality in pixels: `480`, `720`, `1080`, `1440`, `2160` | `1080` |

## Output structure

Each run creates a timestamped folder under `youtube_backup/`:

```
youtube_backup/
└── MyChannel_20260910/
    ├── summary.json
    ├── summary.csv
    ├── downloaded_history.txt
    └── MyChannel/
        └── 20240315 - Video title [videoId]/
            ├── Video title.mp4
            ├── Video title.info.json
            ├── Video title.description
            └── Video title.jpg
```

## Project structure

```
backup_yt/
├── __main__.py       # entry point (python3 -m backup_yt)
├── cli.py            # argument parsing and orchestration
├── config.py         # shared constants
├── logger.py         # colored console output
├── storage.py        # folders, summary.json, summary.csv
└── yt_dlp_client.py  # yt-dlp invocation
```

## License

MIT — see [LICENSE](LICENSE).
