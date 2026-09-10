"""Entry point: argument parsing and orchestration between modules."""

import argparse
import sys

from . import logger
from . import storage
from . import yt_dlp_client


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Full backup of a YouTube channel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Metadata and thumbnails only (fast, low disk usage):
    python3 -m backup_yt --url https://www.youtube.com/@MyChannel --metadata-only

  Full videos at 1080p (recommended for a full backup):
    python3 -m backup_yt --url https://www.youtube.com/@MyChannel

  Videos at 720p (less disk space):
    python3 -m backup_yt --url https://www.youtube.com/@MyChannel --quality 720

  A single playlist:
    python3 -m backup_yt --url "https://www.youtube.com/playlist?list=PLxxxx"
        """
    )

    parser.add_argument(
        "--url",
        required=True,
        help="URL of the YouTube channel, playlist or video"
    )
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="Only download metadata and thumbnails, not the video"
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=1080,
        choices=[480, 720, 1080, 1440, 2160],
        help="Max video quality in pixels (default: 1080)"
    )

    return parser.parse_args()


def main():
    args = _parse_args()

    logger.title("=" * 60)
    logger.title("  YOUTUBE CHANNEL BACKUP")
    logger.title("=" * 60)
    logger.info(f"Channel: {args.url}")
    logger.info(f"Mode: {'Metadata only' if args.metadata_only else f'Full videos ({args.quality}p)'}")
    logger.title("=" * 60)

    if not yt_dlp_client.check_installed():
        sys.exit(1)

    folder = storage.create_folders(args.url)

    if args.metadata_only:
        yt_dlp_client.download_metadata_only(args.url, folder)
    else:
        yt_dlp_client.download_full_channel(args.url, folder, args.quality)

    storage.generate_summary(folder, args.url)

    logger.title("=" * 60)
    logger.success("BACKUP COMPLETE")
    logger.info(f"Saved to: {folder.resolve()}")
    logger.title("=" * 60)


if __name__ == "__main__":
    main()
