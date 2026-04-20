"""
YouTube Transcript Fetcher for B2B SaaS Research
=================================================
Fetches transcripts for 10 experts on YouTube content strategy for B2B SaaS.
Organizes files into /research/youtube-transcripts/{expert-name}/ structure.

Setup:
    pip install youtube-transcript-api

Usage:
    python fetch_transcripts.py

Optional (Supadata fallback for videos without captions):
    pip install supadata
    Set SUPADATA_API_KEY environment variable
"""

import os
import time
import json
from pathlib import Path

# Try importing the primary library
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    PRIMARY_AVAILABLE = True
except ImportError:
    print("ERROR: youtube-transcript-api not installed.")
    print("Run: pip install youtube-transcript-api")
    PRIMARY_AVAILABLE = False

# Try importing Supadata as fallback
try:
    from supadata import Supadata
    SUPADATA_API_KEY = os.getenv("SUPADATA_API_KEY", "")
    SUPADATA_AVAILABLE = bool(SUPADATA_API_KEY)
except ImportError:
    SUPADATA_AVAILABLE = False

# ─────────────────────────────────────────────
# EXPERT + VIDEO DATABASE
# Each expert has a slug (used as folder name),
# display name, and a list of video IDs to fetch.
#
# HOW TO GET VIDEO IDs:
# From URL https://youtube.com/watch?v=ABC123XYZ
# the video ID is: ABC123XYZ
# ─────────────────────────────────────────────

EXPERTS = [
    {
        "slug": "rob-walling",
        "name": "Rob Walling",
        "channel": "https://www.youtube.com/@MicroConf",
        "videos": [
            "Sxn1ji7vYzU",  # If I Started SaaS in 2024, Here's My B2B Content Strategy for $1M ARR
            "Sv1IO5mmTKY",  # Break Through the 7 SaaS Plateaus - MicroConf US 2025
            "BgC-yiNYsR4",  # Early Stage SaaS Marketing Overview - MicroConf Remote 2021
        ],
    },
    {
        "slug": "jason-lemkin",
        "name": "Jason Lemkin",
        "channel": "https://www.youtube.com/@SaaStr",
        "videos": [
            "vc0nITbOlos",  # 10 Things That Always Work in SaaS Marketing
            "RqgjBMlQ6ik",  # How To 10X Your SaaS with Jason Lemkin
            "f0L_l4pc4rU",  # What Really Matters in SaaS in 2025
        ],
    },
    {
        "slug": "ross-simmonds",
        "name": "Ross Simmonds",
        "channel": "https://www.youtube.com/@RossSimmondsTV",
        "videos": [
            "7_bFP2iVVN0",  # B2B Content Marketing & Distribution - Exit Five Drive 2024
            "HqKjnlBfcg0",  # B2B Content Distribution Masterclass: Live with Ross Simmonds
            "8lQfWBFF45U",  # B2B Content & Social Media Strategy with Ross Simmonds
        ],
    },
    {
        "slug": "rand-fishkin",
        "name": "Rand Fishkin",
        "channel": "https://www.youtube.com/@randfish",
        "videos": [
            "C9k5ygsCPvo",  # A Content Marketing Masterclass for B2B Tech Marketers
            "xO_V-7IjkOE",  # Zero-Click Marketing with Rand Fishkin
            "5JQvdLYvGZI",  # Rand Fishkin on SEO, AI Overviews, and the Future of Content Marketing
        ],
    },
    {
        "slug": "wes-bush",
        "name": "Wes Bush",
        "channel": "https://www.youtube.com/@Wes_Bush",
        "videos": [
            "sMaOzX7qmvE",  # Wes Bush on Scaling SaaS and Mastering Content Marketing
            "s7QLEp6hkwM",  # How to Create a Winning B2B Product Strategy
            "w4lyPixues8",  # How to build a SaaS product that sells itself
        ],
    },
    {
        "slug": "nathan-barry",
        "name": "Nathan Barry",
        "channel": "https://www.youtube.com/@nathanbarry",
        "videos": [
            "FRkOW2KWqnc",  # The Billion Dollar Creator Strategy (From Kit's Founder)
            "uctaJFXgNLo",  # Inside the $360K Rebrand That ACTUALLY Worked
            "sZGbQvX9AXY",  # How To Make Money As A Creator | Nathan Barry (ConvertKit)
        ],
    },
    {
        "slug": "denis-shatalin",
        "name": "Denis Shatalin",
        "channel": "https://www.youtube.com/@denisshatalin",
        "videos": [
            "sB9m15rt0SY",  # The best B2B SaaS content strategy in 2025
        ],
    },
    {
        "slug": "dave-gerhardt",
        "name": "Dave Gerhardt",
        "channel": "https://www.youtube.com/@ExitFiveCommunity",
        "videos": [
            "-7drPzHJDPQ",  # Behind the Scenes of Our Content Strategy at Exit Five
            "UB8ZJ01N3bk",  # B2B Marketing Masterclass with Dave Gerhardt
            "N5aoOGfkRVM",  # What's the Right Content Cadence for B2B Brands?
        ],
    },
    {
        "slug": "chima-mmeje",
        "name": "Chima Mmeje",
        "channel": "https://www.youtube.com/@ChimaMmeje",
        "videos": [
            "6ku6KnhlRcU",  # Building Personal Brand Authority in the AI Era
            "iTttoPGAJoY",  # Top SEO Tips For 2026 | Whiteboard Friday
            "5fxd21bpBY4",  # Topic Clusters: How To Own A Subject In The SERPs
        ],
    },
    {
        "slug": "noah-kagan",
        "name": "Noah Kagan",
        "channel": "https://www.youtube.com/@noahkagan",
        "videos": [
            "atyrVhUz8eY",  # YouTube Marketing, best marketing channels with Noah Kagan
            "MolxsU1csKc",  # Noah Kagan's Startup Survival Guide
            "Qyb3R0vYgbo",  # How To Grow a Million Dollar Business w/ AppSumo CEO
        ],
    },
]

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

OUTPUT_BASE = Path("research/youtube-transcripts")
LOG_FILE = Path("research/fetch_log.json")
DELAY_BETWEEN_REQUESTS = 1.5  # seconds, to avoid rate limiting


# ─────────────────────────────────────────────
# FUNCTIONS
# ─────────────────────────────────────────────

def fetch_with_primary(video_id: str) -> str | None:
    """Fetch transcript using youtube-transcript-api (free, no key needed)."""
    try:
        ytt = YouTubeTranscriptApi()
        fetched = ytt.fetch(video_id)
        return " ".join([entry.text for entry in fetched])
    except Exception as e:
        print(f"    [ERROR] {video_id}: {e}")
        return None


def fetch_with_supadata(video_id: str) -> str | None:
    """Fallback: fetch using Supadata API (needs API key, 100 free credits/month)."""
    if not SUPADATA_AVAILABLE:
        return None
    try:
        supadata = Supadata(api_key=SUPADATA_API_KEY)
        result = supadata.youtube.transcript(video_id=video_id, text=True)
        return result.content
    except Exception as e:
        print(f"    [SUPADATA ERROR] {video_id}: {e}")
        return None


def save_transcript(expert_slug: str, video_id: str, text: str):
    """Save transcript text to the correct folder."""
    folder = OUTPUT_BASE / expert_slug
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / f"transcript_{video_id}.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Video ID: {video_id}\n")
        f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
        f.write("=" * 60 + "\n\n")
        f.write(text)
    print(f"    [SAVED] {filepath}")
    return filepath


def run():
    if not PRIMARY_AVAILABLE:
        return

    # Create base directory
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

    log = {
        "fetched": [],
        "skipped": [],
        "errors": [],
    }

    total_videos = sum(len(e["videos"]) for e in EXPERTS)
    print(f"\nFetching transcripts for {len(EXPERTS)} experts, {total_videos} videos total.\n")

    for expert in EXPERTS:
        print(f"\n[{expert['name']}]")

        if not expert["videos"]:
            print("  No video IDs listed. Add IDs to the EXPERTS list above.")
            continue

        for video_id in expert["videos"]:
            print(f"  Fetching: {video_id}")

            # Try primary method first
            text = fetch_with_primary(video_id)

            # Fallback to Supadata if primary fails
            if text is None and SUPADATA_AVAILABLE:
                print(f"    Trying Supadata fallback...")
                text = fetch_with_supadata(video_id)

            if text:
                save_transcript(expert["slug"], video_id, text)
                log["fetched"].append({"expert": expert["slug"], "video_id": video_id})
            else:
                log["skipped"].append({"expert": expert["slug"], "video_id": video_id})

            time.sleep(DELAY_BETWEEN_REQUESTS)

    # Save log
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

    # Summary
    print("\n" + "=" * 60)
    print(f"Done! Fetched: {len(log['fetched'])} | Skipped: {len(log['skipped'])}")
    print(f"Log saved to: {LOG_FILE}")
    print(f"Transcripts saved to: {OUTPUT_BASE}/")


if __name__ == "__main__":
    run()
