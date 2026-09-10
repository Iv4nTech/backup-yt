"""Single responsibility: call yt-dlp."""

import subprocess
from pathlib import Path

from . import logger
from .config import HISTORY_FILE


def check_installed() -> bool:
    """Checks that yt-dlp is installed."""
    try:
        result = subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True, text=True
        )
        logger.success(f"yt-dlp found (version {result.stdout.strip()})")
        return True
    except FileNotFoundError:
        logger.error("yt-dlp is not installed.")
        logger.info("Install it with: pip install yt-dlp")
        return False


def download_metadata_only(channel_url: str, folder: Path) -> int:
    """
    Downloads only metadata and thumbnails for every video.
    Returns the yt-dlp exit code.
    """
    logger.info("Downloading metadata and thumbnails (no videos)...")
    logger.info("This can take a few minutes depending on the channel size.")

    history_file = folder / HISTORY_FILE

    cmd = [
        "yt-dlp",
        "--ignore-errors",                        # Keep going if a single video fails
        "--no-warnings",
        "--write-info-json",                      # Save full metadata in .info.json
        "--write-thumbnail",                      # Download the thumbnail
        "--convert-thumbnails", "jpg",            # Convert thumbnails to JPG
        "--skip-download",                        # Do NOT download the video
        "--download-archive", str(history_file),  # Track what's already downloaded
        "-o", str(folder / "%(uploader)s" / "%(upload_date)s - %(title)s [%(id)s]" / "%(title)s.%(ext)s"),
        channel_url
    ]

    process = subprocess.run(cmd, text=True)

    if process.returncode == 0:
        logger.success("Metadata downloaded successfully.")
    else:
        logger.warning(f"Process finished with exit code {process.returncode}. Check the messages above.")

    return process.returncode


def download_full_channel(channel_url: str, folder: Path, quality: int = 1080) -> int:
    """
    Downloads every video in the channel with its thumbnail, metadata,
    description and tags embedded. Returns the yt-dlp exit code.
    """
    logger.info(f"Downloading full videos at max quality {quality}p...")
    logger.info("This can take a LONG time. You can stop and resume later.")

    history_file = folder / HISTORY_FILE

    # Quality format: try the requested quality, fall back to the best available
    video_format = f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best"

    cmd = [
        "yt-dlp",
        "--ignore-errors",                        # Keep going on errors
        "--no-warnings",

        # -- Quality --
        "-f", video_format,
        "--merge-output-format", "mp4",           # Always save as MP4

        # -- Metadata embedded in the video --
        "--add-metadata",                         # Embed title, description, etc. in the file
        "--embed-thumbnail",                      # Embed the thumbnail inside the MP4
        "--embed-subs",                           # Embed subtitles if available
        "--all-subs",                             # Download subtitles in every language

        # -- Separate metadata files --
        "--write-info-json",                      # .info.json file with EVERYTHING (tags, description, etc.)
        "--write-thumbnail",                      # Separate thumbnail image
        "--write-description",                    # .description file with the text
        "--convert-thumbnails", "jpg",

        # -- History control --
        "--download-archive", str(history_file),  # Skip what you already have

        # -- Folder/file naming --
        "-o", str(folder / "%(uploader)s" / "%(upload_date)s - %(title)s [%(id)s]" / "%(title)s.%(ext)s"),

        channel_url
    ]

    process = subprocess.run(cmd, text=True)

    if process.returncode == 0:
        logger.success("Channel downloaded successfully.")
    else:
        logger.warning(f"Process finished with exit code {process.returncode}.")
        logger.info("Videos already downloaded are safe. You can retry and it will resume where it left off.")

    return process.returncode
