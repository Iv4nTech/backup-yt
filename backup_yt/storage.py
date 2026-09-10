"""Single responsibility: local persistence (folders, summary.json, CSV).

Knows nothing about yt-dlp; it only reads the .info.json files left on
disk and organizes/saves the results.
"""

import csv
import json
from datetime import datetime
from pathlib import Path

from . import logger
from .config import BACKUP_FOLDER


def create_folders(channel_url: str) -> Path:
    """Creates the backup folder structure."""
    name = channel_url.rstrip("/").split("/")[-1].replace("@", "")
    timestamp = datetime.now().strftime("%Y%m%d")
    folder = Path(BACKUP_FOLDER) / f"{name}_{timestamp}"
    folder.mkdir(parents=True, exist_ok=True)
    logger.info(f"Backup folder: {folder.resolve()}")
    return folder


def read_summary(folder: Path) -> dict:
    """Reads the summary of downloaded videos if it already exists."""
    file = folder / "summary.json"
    if file.exists():
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"channel": "", "date": "", "total_videos": 0, "videos": []}


def save_summary(folder: Path, summary: dict):
    """Saves the summary as JSON."""
    file = folder / "summary.json"
    with open(file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


def generate_summary(folder: Path, channel_url: str) -> dict:
    """
    Walks the folders and builds a JSON summary of every video,
    with its title, description, tags, URL and thumbnail.
    """
    logger.info("Generating video summary...")

    videos = []

    for info_file in sorted(folder.rglob("*.info.json")):
        try:
            with open(info_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            video = {
                "id": data.get("id", ""),
                "title": data.get("title", "Untitled"),
                "description": data.get("description", ""),
                "tags": data.get("tags", []),
                "categories": data.get("categories", []),
                "upload_date": data.get("upload_date", ""),
                "duration_seconds": data.get("duration", 0),
                "url": f"https://www.youtube.com/watch?v={data.get('id', '')}",
                "thumbnail_url": data.get("thumbnail", ""),
                "folder": str(info_file.parent.relative_to(folder)),
            }
            videos.append(video)

        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Error reading {info_file.name}: {e}")

    summary = {
        "channel": channel_url,
        "backup_date": datetime.now().isoformat(),
        "total_videos": len(videos),
        "videos": videos,
    }

    save_summary(folder, summary)
    generate_csv(folder, videos)

    logger.success(f"Summary saved: {len(videos)} videos found.")
    logger.info("summary.json - all the data in JSON format")
    logger.info("summary.csv  - table you can open in Excel")

    return summary


def generate_csv(folder: Path, videos: list):
    """Generates a CSV with the main data for each video."""
    csv_file = folder / "summary.csv"
    fields = ["id", "title", "upload_date", "duration_seconds", "url", "tags", "folder"]

    with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for v in videos:
            row = {k: v.get(k, "") for k in fields}
            row["tags"] = ", ".join(v.get("tags", []))
            writer.writerow(row)
