#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              IntelRender                                    ║
║                 Human-Readable Intelligence Report Renderer                 ║
║                                                                              ║
║  Version : 1.0                                                              ║
║  Platform: Kali Linux / Linux                                               ║
║  Mode    : Offline / Local                                                  ║
║                                                                              ║
║  Supported input:                                                           ║
║    JSON, JSONL/NDJSON, CSV, TSV, XML, YAML, INI, ENV, TXT, LOG and generic  ║
║    text-based files.                                                        ║
║                                                                              ║
║  Supported output:                                                          ║
║    TXT, HTML, Markdown, JSON, CSV, XML                                      ║
║                                                                              ║
║  No API keys. No server. No paid service.                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import csv
import re
import html
import hashlib
import configparser
import shutil
import subprocess
import textwrap
import xml.etree.ElementTree as ET

from pathlib import Path
from datetime import datetime
from collections import Counter


# =============================================================================
# APPLICATION INFORMATION
# =============================================================================

APP_NAME = "IntelRender"
VERSION = "1.0"

CONFIG_DIR = Path.home() / ".intelrender"
CONFIG_FILE = CONFIG_DIR / "config.json"

LOGIN_USERNAME = "1"
LOGIN_PASSWORD = "1"

SUPPORTED_INPUT_FORMATS = {
    "json",
    "jsonl",
    "csv",
    "tsv",
    "xml",
    "yaml",
    "ini",
    "env",
    "text",
}

OUTPUT_FORMATS = {
    "1": ("txt", "Human-readable TXT"),
    "2": ("html", "Interactive HTML"),
    "3": ("md", "Markdown"),
    "4": ("json", "Structured JSON"),
    "5": ("csv", "CSV Table"),
    "6": ("xml", "XML Document"),
}


# =============================================================================
# COLORS
# =============================================================================

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


RAINBOW = [
    Colors.BRIGHT_RED,
    Colors.BRIGHT_YELLOW,
    Colors.BRIGHT_GREEN,
    Colors.BRIGHT_CYAN,
    Colors.BRIGHT_BLUE,
    Colors.BRIGHT_MAGENTA,
]


# =============================================================================
# LOGIN ASCII ART
# =============================================================================

LOGIN_BANNER = r"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢻⣧⠹⣿⣿⢸⣿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡌⢿⣧⡘⣿⠈⣿⡇⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠋⠉⠉⠋⠉⠁⠀⠀⠀⠀⠉⠉⠈⢿⣷⣌⠃⠟⡱⢰⣿⡦⣙⣛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡽⢲⠾⢣⣿⡿⢡⣿⣿⢧⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠴⣣⢺⢲⣼⢡⣿⡿⢃⣚⣆⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⣦⡶⢃⠰⠏⢈⢻⢡⣶⣾⣿⣆⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣯⠀⣝⠸⠂⠸⢀⠘⣿⣿⣿⣿⣆⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⡁⢩⣷⣿⣄⠻⡆⣿⣿⣿⣿⣿⣆⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⣿⣿⣿⣿⣷⣅⢹⣿⣿⣿⣿⣿⣦⣦⣍⣛⡿⠿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡀⠀⠀⠀⠀⠀⠀⠈⠙⠻⣿⣿⣿⣦⡿⠿⠟⣿⣿⣿⣿⣿⣿⣿⣷⣶⣮⣭⣙⡛⠻⠿
⣿⣿⢡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⣩⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠻⢿⣦⣴⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠿⠿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣭⣙⡻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣬⠀⠀⠀⠀⠀⠀⠀⠸⢠⣶⠶⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣶⣮⣝⡛⠿⣿⣿⣿⣿⣿⣿
⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠀⠀⠀⠀⠀⠀⠀⣤⠋⠀⢀⣈⣿⡄⠳⠖⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣬⣝⡛⠿⣿
⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠼⠿⠿⠄⠀⠀⠀⠀⠀⣼⣿⣾⣁⣠⣡⣤⣦⣼⡆⠀⠀⠀⠀⠀⢠⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶
⣿⣿⡇⠠⠀⠀⠀⠀⠀⠀⠀⠀⢀⡄⢰⡆⣲⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣹⣿⣿⣿⠁⠀⠀⠀⠀⠀⠈⡄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠓⠈⣡⣴⠆⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⢸⠇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡄⡄⠀⠀⠀⠀⠀⠀⠀⢰⣶⢿⣿⣿⠀⠀⠀⣿⣿⡿⢿⣛⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠸⢀⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⢸⢻⢸⣽⣿⠀⠀⢸⣿⣿⣿⣾⡿⠿⠿⠿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠈⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣿⣿⠀⠀⣿⣿⡏⡅⠒⠈⠀⠀⠀⢸⣿⣿⣿⠄⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⢈⠻⣿⣿⠀⠀⣿⣿⡇⠀⣴⣶⣶⣿⡆⢸⣿⣿⡟⢀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠈⢤⡙⢿⣇⠀⠸⣿⣿⣄⠻⣿⣿⡿⠇⣼⣿⢋⡀⣠⠂⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿
⣿⣿⣿⣿⣿⣿⣿⡀⠠⡀⠀⠀⠀⠀⠈⠻⣦⣌⠓⠦⣙⣿⣿⣷⣤⣭⣶⣾⣿⣿⠏⣰⡏⠀⠀⠀⠀⠘⣿⡿⠟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⣋⣥⣾
⣿⣿⣿⣿⣿⣿⣿⣷⡀⢻⣆⡀⠀⠀⠀⠠⣈⡉⢀⡀⣮⣍⣛⠿⢿⣿⣿⡿⢟⣡⣾⣿⡤⠆⠀⠀⠀⢀⣀⣠⣶⣿⣿⣿⡿⠟⣋⣩⣭⣵⣶⣶⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣙⠃⢀⣷⣄⠀⢬⣳⣿⣧⠸⣿⣿⣿⣶⣶⣶⡶⠿⠛⠛⠉⠀⠀⠀⠀⠀⣤⣉⣉⣭⣿⠟⣡⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢁⣼⣿⣿⣷⣶⣾⣿⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠀⠀⠀⠻⠿⣛⠛⣥⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⡀⠀⢠⣀⣀⣀⣀⣀⣠⣤⣴⣶⣾⣿⣿⣴⡄⠘⣿⠱⠊⣾⣿⣷⣿⣿⣿⣿⣿⣿⣿⡟⣹⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠈⠀⣠⣸⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⠿⡀⠀⢶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢱⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢟⣋⣡⡤⠀⢠⣿⣿⣿⣿⣷⡹⣿⣿⣿⣿⣿⠀⠿⢟⣩⣴⣿⣿⡀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⢡⣿⣿⣿⣿⣿⣿⠿
⣿⣿⣿⠿⠟⣛⣋⣭⣭⣵⣖⣠⣜⣛⠿⠿⠁⠀⠿⠿⠿⣿⣟⠿⣷⠘⣿⣿⣿⠃⢀⣾⣿⣿⣿⣿⣿⣷⡀⠀⠻⣿⣿⣿⣿⣿⣿⣿⠣⣿⣿⣿⣿⡿⡋⣴⣿
⡿⢋⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⢀⣾⣿⣿⣿⣿⣿⣷⣦⣤⣾⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠹⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⢋⣼⢠⣿⣿
⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⡿⢓⣰⠃⣿⣿⣿
"""


# =============================================================================
# MAIN MENU ASCII ART
# =============================================================================

MAIN_BANNER = r"""
██╗███╗   ██╗████████╗███████╗██╗     ██████╗ ███████╗███╗   ██╗██████╗ ███████╗██████╗
██║████╗  ██║╚══██╔══╝██╔════╝██║     ██╔══██╗██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗
██║██╔██╗ ██║   ██║   █████╗  ██║     ██████╔╝█████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██║██║╚██╗██║   ██║   ██╔══╝  ██║     ██╔══██╗██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██║██║ ╚████║   ██║   ███████╗███████╗██║  ██║███████╗██║ ╚████║██████╔╝███████╗██║  ██║
╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝

                    INTELLIGENCE REPORT RENDERING ENGINE
"""


# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_CONFIG = {
    "default_output_format": "txt",
    "preview_lines": 25,
    "recursive_batch": True,
    "show_metadata": True,
    "color": True,
}


def load_config():
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        if not CONFIG_FILE.exists():
            save_config(DEFAULT_CONFIG.copy())
            return DEFAULT_CONFIG.copy()

        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        config = DEFAULT_CONFIG.copy()
        if isinstance(data, dict):
            config.update(data)

        return config

    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(config):
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        return True

    except Exception:
        return False


CONFIG = load_config()


# =============================================================================
# TERMINAL HELPERS
# =============================================================================

def clear():
    os.system("clear")


def terminal_width():
    try:
        return shutil.get_terminal_size((100, 30)).columns
    except Exception:
        return 100


def rainbow_text(text):
    if not CONFIG.get("color", True):
        return text

    output = []
    index = 0

    for char in text:
        if char == "\n":
            output.append("\n")
            continue

        if char.isspace():
            output.append(char)
            continue

        color = RAINBOW[index % len(RAINBOW)]
        output.append(color + char + Colors.RESET)
        index += 1

    return "".join(output)


def color(text, value):
    if not CONFIG.get("color", True):
        return text

    return value + str(text) + Colors.RESET


def title(text):
    print()
    print(color("╔" + "═" * 76 + "╗", Colors.BRIGHT_CYAN))
    print(color("║ ", Colors.BRIGHT_CYAN) + color(text.center(74), Colors.BRIGHT_WHITE) + color(" ║", Colors.BRIGHT_CYAN))
    print(color("╚" + "═" * 76 + "╝", Colors.BRIGHT_CYAN))
    print()


def line():
    print(color("─" * min(78, terminal_width()), Colors.BRIGHT_BLACK))


def pause(message="Press ENTER to continue..."):
    try:
        input(color(f"\n{message}", Colors.BRIGHT_YELLOW))
    except KeyboardInterrupt:
        pass


def print_banner(banner):
    clear()
    print(rainbow_text(banner))


def ask(prompt, default=None):
    if default is not None:
        prompt_text = f"{prompt} [{default}]: "
    else:
        prompt_text = f"{prompt}: "

    try:
        value = input(color(prompt_text, Colors.BRIGHT_WHITE)).strip()
    except KeyboardInterrupt:
        print()
        return ""

    if not value and default is not None:
        return str(default)

    return value


def yes_no(prompt, default=True):
    default_text = "Y/n" if default else "y/N"

    value = ask(f"{prompt} ({default_text})").lower()

    if not value:
        return default

    return value in ("y", "yes", "1", "true")


# =============================================================================
# FILE HELPERS
# =============================================================================

def human_size(size):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]

    value = float(size)

    for unit in units:
        if value < 1024:
            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} EB"


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def is_probably_binary(path):
    try:
        with path.open("rb") as f:
            sample = f.read(8192)

        return b"\x00" in sample

    except Exception:
        return True


def detect_encoding(path):
    encodings = [
        "utf-8-sig",
        "utf-8",
        "cp1252",
        "latin-1",
    ]

    for encoding in encodings:
        try:
            with path.open("r", encoding=encoding) as f:
                f.read(65536)

            return encoding

        except (UnicodeDecodeError, UnicodeError):
            continue

        except Exception:
            break

    return "utf-8"


def read_sample(path, encoding=None):
    if encoding is None:
        encoding = detect_encoding(path)

    try:
        with path.open(
            "r",
            encoding=encoding,
            errors="replace",
            newline=""
        ) as f:
            return f.read(65536)

    except Exception:
        return ""


# =============================================================================
# FORMAT DETECTION
# =============================================================================

def detect_format(path):
    suffix = path.suffix.lower()

    extension_map = {
        ".json": "json",
        ".jsonl": "jsonl",
        ".ndjson": "jsonl",
        ".csv": "csv",
        ".tsv": "tsv",
        ".xml": "xml",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".ini": "ini",
        ".conf": "ini",
        ".cfg": "ini",
        ".env": "env",
        ".txt": "text",
        ".log": "text",
        ".text": "text",
    }

    if suffix in extension_map:
        return extension_map[suffix]

    if is_probably_binary(path):
        return "binary"

    encoding = detect_encoding(path)
    sample = read_sample(path, encoding)

    stripped = sample.lstrip()

    if stripped.startswith("{") or stripped.startswith("["):
        try:
            json.loads(sample)
            return "json"
        except Exception:
            pass

    if stripped.startswith("<"):
        try:
            ET.fromstring(sample)
            return "xml"
        except Exception:
            if re.search(r"<[A-Za-z][^>]*>", sample):
                return "xml"

    lines = [
        x.strip()
        for x in sample.splitlines()
        if x.strip()
    ]

    if lines:
        json_lines = 0

        for current in lines[:50]:
            try:
                json.loads(current)
                json_lines += 1
            except Exception:
                pass

        if json_lines >= max(2, len(lines[:50]) // 2):
            return "jsonl"

    if sample:
        try:
            dialect = csv.Sniffer().sniff(sample[:8192], delimiters=",\t;|")

            if dialect.delimiter == "\t":
                return "tsv"

            if dialect.delimiter in ",;|":
                return "csv"

        except Exception:
            pass

    return "text"


# =============================================================================
# XML CONVERSION HELPERS
# =============================================================================

def xml_element_to_object(element):
    children = list(element)

    attributes = {
        f"@{key}": value
        for key, value in element.attrib.items()
    }

    text = (element.text or "").strip()

    if not children:
        if attributes:
            result = dict(attributes)

            if text:
                result["#text"] = text

            return result

        return text

    result = dict(attributes)

    if text:
        result["#text"] = text

    grouped = {}

    for child in children:
        value = xml_element_to_object(child)

        if child.tag in grouped:
            if not isinstance(grouped[child.tag], list):
                grouped[child.tag] = [grouped[child.tag]]

            grouped[child.tag].append(value)

        else:
            grouped[child.tag] = value

    result.update(grouped)

    return result


def load_xml(path):
    tree = ET.parse(path)
    return xml_element_to_object(tree.getroot())


# =============================================================================
# YAML
# =============================================================================

def load_yaml(path):
    try:
        import yaml
    except ImportError:
        raise RuntimeError(
            "YAML support requires PyYAML.\n"
            "Install it with: sudo apt install python3-yaml"
        )

    encoding = detect_encoding(path)

    with path.open("r", encoding=encoding, errors="replace") as f:
        return yaml.safe_load(f)


# =============================================================================
# JSON STREAMING
# =============================================================================

def iter_json_array(path, encoding):
    decoder = json.JSONDecoder()

    with path.open(
        "r",
        encoding=encoding,
        errors="replace"
    ) as f:

        buffer = ""
        position = 0
        started = False
        finished = False

        while not finished:
            chunk = f.read(65536)

            if chunk:
                buffer += chunk

            eof = not chunk

            while True:
                while position < len(buffer) and buffer[position].isspace():
                    position += 1

                if not started:
                    if position >= len(buffer):
                        break

                    if buffer[position] != "[":
                        raise ValueError("Expected JSON array.")

                    position += 1
                    started = True

                while position < len(buffer) and buffer[position].isspace():
                    position += 1

                if position >= len(buffer):
                    break

                if buffer[position] == "]":
                    finished = True
                    position += 1
                    break

                try:
                    value, end_position = decoder.raw_decode(
                        buffer,
                        position
                    )
                except json.JSONDecodeError:
                    if eof:
                        raise ValueError(
                            "Malformed JSON array or incomplete JSON value."
                        )

                    break

                yield value

                position = end_position

                while position < len(buffer) and buffer[position].isspace():
                    position += 1

                if position >= len(buffer):
                    break

                if buffer[position] == ",":
                    position += 1
                    continue

                if buffer[position] == "]":
                    finished = True
                    position += 1
                    break

                raise ValueError(
                    "Invalid JSON array separator."
                )

            if position:
                buffer = buffer[position:]
                position = 0

            if eof:
                break


def iter_jsonl(path, encoding):
    with path.open(
        "r",
        encoding=encoding,
        errors="replace"
    ) as f:

        for line_number, line_text in enumerate(f, 1):
            raw = line_text.strip()

            if not raw:
                continue

            try:
                yield json.loads(raw)

            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on line {line_number}: {exc}"
                )


def iter_json_records(path):
    encoding = detect_encoding(path)

    first_char = ""

    with path.open(
        "r",
        encoding=encoding,
        errors="replace"
    ) as f:
        while True:
            char = f.read(1)

            if not char:
                break

            if not char.isspace():
                first_char = char
                break

    if first_char == "[":
        yield from iter_json_array(path, encoding)
        return

    if path.suffix.lower() in (".jsonl", ".ndjson"):
        yield from iter_jsonl(path, encoding)
        return

    try:
        with path.open(
            "r",
            encoding=encoding,
            errors="replace"
        ) as f:
            data = json.load(f)

    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed JSON: {exc}")

    if isinstance(data, list):
        for item in data:
            yield item
    else:
        yield data


# =============================================================================
# CSV / TSV
# =============================================================================

def iter_csv_records(path, delimiter=None):
    encoding = detect_encoding(path)

    with path.open(
        "r",
        encoding=encoding,
        errors="replace",
        newline=""
    ) as f:

        if delimiter is None:
            try:
                sample = f.read(8192)
                f.seek(0)

                dialect = csv.Sniffer().sniff(
                    sample,
                    delimiters=",\t;|"
                )

                delimiter = dialect.delimiter

            except Exception:
                delimiter = "\t" if path.suffix.lower() == ".tsv" else ","

        reader = csv.reader(
            f,
            delimiter=delimiter
        )

        try:
            first_row = next(reader)
        except StopIteration:
            return

        if not first_row:
            return

        # Determine whether the first row appears to be a header.
        try:
            has_header = csv.Sniffer().has_header(
                "\n".join(
                    [delimiter.join(first_row)]
                )
            )
        except Exception:
            has_header = True

        if has_header:
            headers = []

            for index, value in enumerate(first_row, 1):
                header = str(value).strip()

                if not header:
                    header = f"column_{index}"

                headers.append(header)

            for row in reader:
                record = {}

                for index, header in enumerate(headers):
                    record[header] = row[index] if index < len(row) else ""

                if len(row) > len(headers):
                    for extra_index in range(len(headers), len(row)):
                        record[f"column_{extra_index + 1}"] = row[extra_index]

                yield record

        else:
            headers = [
                f"column_{index}"
                for index in range(1, len(first_row) + 1)
            ]

            yield {
                header: first_row[index]
                for index, header in enumerate(headers)
            }

            for row in reader:
                record = {}

                for index, header in enumerate(headers):
                    record[header] = (
                        row[index]
                        if index < len(row)
                        else ""
                    )

                yield record


# =============================================================================
# TEXT / LOG
# =============================================================================

def iter_text_records(path):
    encoding = detect_encoding(path)

    with path.open(
        "r",
        encoding=encoding,
        errors="replace"
    ) as f:

        for line_number, line in enumerate(f, 1):
            yield {
                "line": line_number,
                "text": line.rstrip("\r\n"),
            }


# =============================================================================
# INI
# =============================================================================

def iter_ini_records(path):
    encoding = detect_encoding(path)

    parser = configparser.ConfigParser()

    with path.open(
        "r",
        encoding=encoding,
        errors="replace"
    ) as f:
        parser.read_file(f)

    data = {}

    for section in parser.sections():
        data[section] = dict(parser.items(section))

    if not data:
        data = dict(parser.defaults())

    yield data


# =============================================================================
# ENV
# =============================================================================

def iter_env_records(path):
    encoding = detect_encoding(path)

    data = {}

    with path.open(
        "r",
        encoding=encoding,
        errors="replace"
    ) as f:

        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            key = key.strip()
            value = value.strip()

            if (
                len(value) >= 2
                and value[0] == value[-1]
                and value[0] in ("'", '"')
            ):
                value = value[1:-1]

            data[key] = value

    yield data


# =============================================================================
# UNIVERSAL RECORD ITERATOR
# =============================================================================

def iter_records(path, file_format=None):
    if file_format is None:
        file_format = detect_format(path)

    if file_format == "json":
        yield from iter_json_records(path)

    elif file_format == "jsonl":
        yield from iter_jsonl(
            path,
            detect_encoding(path)
        )

    elif file_format == "csv":
        yield from iter_csv_records(path, ",")

    elif file_format == "tsv":
        yield from iter_csv_records(path, "\t")

    elif file_format == "xml":
        yield load_xml(path)

    elif file_format == "yaml":
        yield load_yaml(path)

    elif file_format == "ini":
        yield from iter_ini_records(path)

    elif file_format == "env":
        yield from iter_env_records(path)

    elif file_format == "text":
        yield from iter_text_records(path)

    else:
        raise ValueError(
            f"Unsupported input format: {file_format}"
        )


# =============================================================================
# NORMALIZATION
# =============================================================================

def normalize_record(value):
    if isinstance(value, dict):
        return value

    if isinstance(value, list):
        return {
            "items": value
        }

    return {
        "value": value
    }


def flatten_value(value, prefix="", output=None):
    if output is None:
        output = {}

    if isinstance(value, dict):
        for key, child in value.items():
            key = str(key)

            new_prefix = (
                f"{prefix}.{key}"
                if prefix
                else key
            )

            flatten_value(
                child,
                new_prefix,
                output
            )

    elif isinstance(value, list):
        if not value:
            output[prefix] = ""

        else:
            for index, child in enumerate(value):
                new_prefix = (
                    f"{prefix}[{index}]"
                    if prefix
                    else f"[{index}]"
                )

                if isinstance(child, (dict, list)):
                    flatten_value(
                        child,
                        new_prefix,
                        output
                    )
                else:
                    output[new_prefix] = child

    else:
        output[prefix] = value

    return output


def flatten_record(record):
    record = normalize_record(record)

    flattened = flatten_value(record)

    return {
        key: stringify_value(value)
        for key, value in flattened.items()
    }


def stringify_value(value):
    if value is None:
        return ""

    if isinstance(value, (dict, list)):
        return json.dumps(
            value,
            ensure_ascii=False
        )

    if isinstance(value, bool):
        return "true" if value else "false"

    return str(value)


# =============================================================================
# HUMAN-READABLE RENDERING
# =============================================================================

def render_human(value, indent=0):
    prefix = " " * indent

    if isinstance(value, dict):
        lines = []

        for key, child in value.items():
            if isinstance(child, (dict, list)):
                lines.append(
                    f"{prefix}{key}:"
                )

                lines.extend(
                    render_human(
                        child,
                        indent + 4
                    )
                )

            else:
                lines.append(
                    f"{prefix}{key}: {stringify_value(child)}"
                )

        return lines

    if isinstance(value, list):
        lines = []

        for index, child in enumerate(value, 1):
            if isinstance(child, (dict, list)):
                lines.append(
                    f"{prefix}[{index}]"
                )

                lines.extend(
                    render_human(
                        child,
                        indent + 4
                    )
                )

            else:
                lines.append(
                    f"{prefix}- {stringify_value(child)}"
                )

        return lines

    return [
        prefix + stringify_value(value)
    ]


def render_record_text(record, record_number):
    normalized = normalize_record(record)

    lines = [
        f"RECORD {record_number}",
        "─" * 70,
    ]

    lines.extend(
        render_human(normalized)
    )

    return lines


# =============================================================================
# OUTPUT PATH
# =============================================================================

def extension_for_format(file_format):
    return {
        "txt": "txt",
        "html": "html",
        "md": "md",
        "json": "json",
        "csv": "csv",
        "xml": "xml",
    }.get(file_format, file_format)


def default_output_path(input_path, output_format):
    suffix = extension_for_format(output_format)

    return input_path.with_name(
        f"{input_path.stem}_rendered.{suffix}"
    )


def unique_output_path(path):
    if not path.exists():
        return path

    counter = 1

    while True:
        candidate = path.with_name(
            f"{path.stem}_{counter}{path.suffix}"
        )

        if not candidate.exists():
            return candidate

        counter += 1


def get_output_path(input_path, output_format):
    default = default_output_path(
        input_path,
        output_format
    )

    print()
    print(
        color(
            f"Default output: {default}",
            Colors.BRIGHT_CYAN
        )
    )

    custom = ask(
        "Output path",
        str(default)
    )

    output_path = Path(custom).expanduser()

    if output_path.resolve() == input_path.resolve():
        print(
            color(
                "Output cannot overwrite the input file.",
                Colors.BRIGHT_RED
            )
        )

        return None

    if output_path.exists():
        if not yes_no(
            f"{output_path} already exists. Overwrite?"
        ):
            output_path = unique_output_path(
                output_path
            )

            print(
                color(
                    f"Using: {output_path}",
                    Colors.BRIGHT_YELLOW
                )
            )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return output_path


# =============================================================================
# OUTPUT: TXT
# =============================================================================

def convert_to_txt(
    input_path,
    input_format,
    output_path
):
    with output_path.open(
        "w",
        encoding="utf-8"
    ) as out:

        out.write(
            f"{APP_NAME} {VERSION}\n"
        )
        out.write(
            "=" * 80 + "\n"
        )

        out.write(
            f"Source       : {input_path.name}\n"
        )
        out.write(
            f"Input format : {input_format.upper()}\n"
        )
        out.write(
            f"Generated    : {datetime.now().isoformat(sep=' ', timespec='seconds')}\n"
        )
        out.write(
            f"SHA256       : {sha256_file(input_path)}\n"
        )

        out.write(
            "=" * 80 + "\n\n"
        )

        count = 0

        for count, record in enumerate(
            iter_records(
                input_path,
                input_format
            ),
            1
        ):
            for current_line in render_record_text(
                record,
                count
            ):
                out.write(current_line + "\n")

            out.write("\n")

        return count


# =============================================================================
# OUTPUT: MARKDOWN
# =============================================================================

def convert_to_markdown(
    input_path,
    input_format,
    output_path
):
    with output_path.open(
        "w",
        encoding="utf-8"
    ) as out:

        out.write(
            f"# {APP_NAME} Report\n\n"
        )

        out.write(
            f"| Property | Value |\n"
            f"|---|---|\n"
        )

        out.write(
            f"| Source | `{input_path.name}` |\n"
        )

        out.write(
            f"| Input Format | `{input_format.upper()}` |\n"
        )

        out.write(
            f"| Generated | `{datetime.now().isoformat(sep=' ', timespec='seconds')}` |\n"
        )

        out.write(
            f"| SHA256 | `{sha256_file(input_path)}` |\n\n"
        )

        out.write(
            "---\n\n"
        )

        count = 0

        for count, record in enumerate(
            iter_records(
                input_path,
                input_format
            ),
            1
        ):
            out.write(
                f"## Record {count}\n\n"
            )

            normalized = normalize_record(record)

            lines = render_human(normalized)

            for current_line in lines:
                if current_line.strip():
                    out.write(
                        f"- {current_line.strip()}\n"
                    )

            out.write("\n")

        return count


# =============================================================================
# OUTPUT: HTML
# =============================================================================

HTML_STYLE = """
body {
    background:#0b0f14;
    color:#e8edf2;
    font-family:Arial,Helvetica,sans-serif;
    margin:0;
    padding:0;
}

.container {
    max-width:1200px;
    margin:auto;
    padding:30px;
}

.header {
    border:1px solid #34404d;
    border-radius:12px;
    padding:25px;
    margin-bottom:25px;
    background:#111820;
}

.header h1 {
    margin-top:0;
}

.meta {
    color:#9aa8b5;
    font-size:14px;
    line-height:1.8;
}

.record {
    border:1px solid #303b46;
    border-radius:10px;
    margin-bottom:20px;
    overflow:hidden;
    background:#10161d;
}

.record-title {
    padding:12px 16px;
    background:#18222c;
    font-weight:bold;
}

pre {
    white-space:pre-wrap;
    word-break:break-word;
    padding:18px;
    margin:0;
    line-height:1.55;
}

.badge {
    display:inline-block;
    padding:4px 8px;
    border-radius:5px;
    background:#273646;
    margin-right:5px;
}
"""


def convert_to_html(
    input_path,
    input_format,
    output_path
):
    generated = datetime.now().isoformat(
        sep=" ",
        timespec="seconds"
    )

    digest = sha256_file(input_path)

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as out:

        out.write(
            "<!DOCTYPE html>\n"
        )
        out.write(
            '<html lang="en">\n<head>\n'
        )
        out.write(
            '<meta charset="utf-8">\n'
        )
        out.write(
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        )
        out.write(
            f"<title>{html.escape(APP_NAME)} Report</title>\n"
        )
        out.write(
            f"<style>{HTML_STYLE}</style>\n"
        )
        out.write(
            "</head>\n<body>\n<div class=\"container\">\n"
        )

        out.write(
            '<div class="header">\n'
        )

        out.write(
            f"<h1>{html.escape(APP_NAME)} Report</h1>\n"
        )

        out.write(
            '<div class="meta">\n'
        )

        out.write(
            f"<b>Source:</b> {html.escape(input_path.name)}<br>\n"
        )

        out.write(
            f"<b>Input format:</b> "
            f"<span class=\"badge\">{html.escape(input_format.upper())}</span><br>\n"
        )

        out.write(
            f"<b>Generated:</b> {html.escape(generated)}<br>\n"
        )

        out.write(
            f"<b>SHA256:</b> {html.escape(digest)}\n"
        )

        out.write(
            "</div>\n</div>\n"
        )

        count = 0

        for count, record in enumerate(
            iter_records(
                input_path,
                input_format
            ),
            1
        ):
            rendered = "\n".join(
                render_human(
                    normalize_record(record)
                )
            )

            out.write(
                '<div class="record">\n'
            )

            out.write(
                f'<div class="record-title">Record {count}</div>\n'
            )

            out.write(
                "<pre>"
                + html.escape(rendered)
                + "</pre>\n"
            )

            out.write(
                "</div>\n"
            )

        out.write(
            "</div>\n</body>\n</html>\n"
        )

        return count


# =============================================================================
# OUTPUT: JSON
# =============================================================================

def convert_to_json(
    input_path,
    input_format,
    output_path
):
    metadata = {
        "tool": APP_NAME,
        "version": VERSION,
        "source": input_path.name,
        "input_format": input_format,
        "generated": datetime.now().isoformat(
            sep=" ",
            timespec="seconds"
        ),
        "sha256": sha256_file(input_path),
    }

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as out:

        out.write("{\n")

        out.write(
            '  "intelrender": '
            + json.dumps(
                metadata,
                ensure_ascii=False,
                indent=4
            ).replace(
                "\n",
                "\n  "
            )
            + ",\n"
        )

        out.write(
            '  "records": [\n'
        )

        first = True
        count = 0

        for count, record in enumerate(
            iter_records(
                input_path,
                input_format
            ),
            1
        ):
            if not first:
                out.write(",\n")

            serialized = json.dumps(
                record,
                ensure_ascii=False,
                indent=4
            )

            out.write(
                textwrap.indent(
                    serialized,
                    "    "
                )
            )

            first = False

        out.write(
            "\n  ]\n"
        )

        out.write(
            "}\n"
        )

        return count


# =============================================================================
# OUTPUT: CSV
# =============================================================================

def collect_csv_fields(
    input_path,
    input_format
):
    fields = []

    seen = set()

    for record in iter_records(
        input_path,
        input_format
    ):
        flattened = flatten_record(record)

        for key in flattened:
            if key not in seen:
                seen.add(key)
                fields.append(key)

    return fields


def convert_to_csv(
    input_path,
    input_format,
    output_path
):
    fields = collect_csv_fields(
        input_path,
        input_format
    )

    with output_path.open(
        "w",
        encoding="utf-8",
        newline=""
    ) as out:

        writer = csv.DictWriter(
            out,
            fieldnames=fields,
            extrasaction="ignore"
        )

        writer.writeheader()

        count = 0

        for count, record in enumerate(
            iter_records(
                input_path,
                input_format
            ),
            1
        ):
            flattened = flatten_record(record)

            writer.writerow(
                {
                    field: flattened.get(
                        field,
                        ""
                    )
                    for field in fields
                }
            )

        return count


# =============================================================================
# OUTPUT: XML
# =============================================================================

def safe_xml_tag(value):
    value = str(value)

    value = re.sub(
        r"[^A-Za-z0-9_.-]",
        "_",
        value
    )

    if not value:
        value = "item"

    if value[0].isdigit():
        value = "_" + value

    return value


def object_to_xml(parent, value, key_name="item"):
    if isinstance(value, dict):
        for key, child in value.items():
            child_element = ET.SubElement(
                parent,
                safe_xml_tag(key)
            )

            object_to_xml(
                child_element,
                child,
                key
            )

    elif isinstance(value, list):
        for child in value:
            child_element = ET.SubElement(
                parent,
                safe_xml_tag(key_name)
            )

            object_to_xml(
                child_element,
                child,
                key_name
            )

    else:
        parent.text = stringify_value(value)


def convert_to_xml(
    input_path,
    input_format,
    output_path
):
    root = ET.Element(
        "intelrender"
    )

    metadata = ET.SubElement(
        root,
        "metadata"
    )

    ET.SubElement(
        metadata,
        "tool"
    ).text = APP_NAME

    ET.SubElement(
        metadata,
        "version"
    ).text = VERSION

    ET.SubElement(
        metadata,
        "source"
    ).text = input_path.name

    ET.SubElement(
        metadata,
        "input_format"
    ).text = input_format

    ET.SubElement(
        metadata,
        "generated"
    ).text = datetime.now().isoformat(
        sep=" ",
        timespec="seconds"
    )

    ET.SubElement(
        metadata,
        "sha256"
    ).text = sha256_file(
        input_path
    )

    records_element = ET.SubElement(
        root,
        "records"
    )

    count = 0

    for count, record in enumerate(
        iter_records(
            input_path,
            input_format
        ),
        1
    ):
        record_element = ET.SubElement(
            records_element,
            "record"
        )

        record_element.set(
            "number",
            str(count)
        )

        object_to_xml(
            record_element,
            normalize_record(record)
        )

    tree = ET.ElementTree(root)

    try:
        ET.indent(
            tree,
            space="  "
        )
    except AttributeError:
        pass

    tree.write(
        output_path,
        encoding="utf-8",
        xml_declaration=True
    )

    return count


# =============================================================================
# CONVERSION DISPATCHER
# =============================================================================

def convert_file(
    input_path,
    output_format,
    output_path=None
):
    input_path = Path(input_path).expanduser()

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file does not exist: {input_path}"
        )

    if not input_path.is_file():
        raise ValueError(
            f"Not a regular file: {input_path}"
        )

    input_format = detect_format(
        input_path
    )

    if input_format == "binary":
        raise ValueError(
            "The selected file appears to be binary."
        )

    if output_path is None:
        output_path = default_output_path(
            input_path,
            output_format
        )

        if output_path.exists():
            output_path = unique_output_path(
                output_path
            )

    output_path = Path(
        output_path
    ).expanduser()

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if output_path.resolve() == input_path.resolve():
        raise ValueError(
            "Input and output paths cannot be the same."
        )

    if output_format == "txt":
        count = convert_to_txt(
            input_path,
            input_format,
            output_path
        )

    elif output_format == "html":
        count = convert_to_html(
            input_path,
            input_format,
            output_path
        )

    elif output_format == "md":
        count = convert_to_markdown(
            input_path,
            input_format,
            output_path
        )

    elif output_format == "json":
        count = convert_to_json(
            input_path,
            input_format,
            output_path
        )

    elif output_format == "csv":
        count = convert_to_csv(
            input_path,
            input_format,
            output_path
        )

    elif output_format == "xml":
        count = convert_to_xml(
            input_path,
            input_format,
            output_path
        )

    else:
        raise ValueError(
            f"Unsupported output format: {output_format}"
        )

    return {
        "input": input_path,
        "input_format": input_format,
        "output": output_path,
        "output_format": output_format,
        "records": count,
    }


# =============================================================================
# OUTPUT FORMAT MENU
# =============================================================================

def choose_output_format():
    print()

    title("SELECT FINAL DOCUMENT FORMAT")

    for number, (extension, description) in OUTPUT_FORMATS.items():
        print(
            f"  {color(number, Colors.BRIGHT_YELLOW)}"
            f"  {color(description, Colors.BRIGHT_WHITE)}"
            f"  [{extension.upper()}]"
        )

    print()
    print(
        color("  0  Cancel", Colors.BRIGHT_RED)
    )

    while True:
        choice = ask(
            "Select output format",
            CONFIG.get(
                "default_output_format",
                "txt"
            )
        )

        if choice == "0":
            return None

        if choice in OUTPUT_FORMATS:
            return OUTPUT_FORMATS[choice][0]

        # Allow typing the extension directly.
        normalized = choice.lower().lstrip(".")

        if normalized in {
            "txt",
            "html",
            "md",
            "json",
            "csv",
            "xml",
        }:
            return normalized

        print(
            color(
                "Invalid output format.",
                Colors.BRIGHT_RED
            )
        )


# =============================================================================
# CONVERT SINGLE FILE
# =============================================================================

def single_conversion():
    clear()

    title("CONVERT REPORT")

    input_value = ask(
        "Enter input file path"
    )

    if not input_value:
        return

    input_path = Path(
        input_value
    ).expanduser()

    if not input_path.exists():
        print(
            color(
                "File not found.",
                Colors.BRIGHT_RED
            )
        )

        pause()
        return

    try:
        detected = detect_format(
            input_path
        )

        print()
        print(
            color(
                f"Detected input format : {detected.upper()}",
                Colors.BRIGHT_CYAN
            )
        )

        print(
            color(
                f"File size             : {human_size(input_path.stat().st_size)}",
                Colors.BRIGHT_CYAN
            )
        )

    except Exception as exc:
        print(
            color(
                f"Detection error: {exc}",
                Colors.BRIGHT_RED
            )
        )

        pause()
        return

    output_format = choose_output_format()

    if output_format is None:
        return

    output_path = get_output_path(
        input_path,
        output_format
    )

    if output_path is None:
        pause()
        return

    print()
    print(
        color(
            "Rendering report...",
            Colors.BRIGHT_YELLOW
        )
    )

    try:
        result = convert_file(
            input_path,
            output_format,
            output_path
        )

        print()
        print(
            color(
                "╔════════════════════════════════════════════════════╗",
                Colors.BRIGHT_GREEN
            )
        )

        print(
            color(
                "║                 CONVERSION COMPLETE              ║",
                Colors.BRIGHT_GREEN
            )
        )

        print(
            color(
                "╚════════════════════════════════════════════════════╝",
                Colors.BRIGHT_GREEN
            )
        )

        print()
        print(
            f"Input      : {result['input']}"
        )

        print(
            f"Detected   : {result['input_format'].upper()}"
        )

        print(
            f"Output     : {result['output']}"
        )

        print(
            f"Format     : {result['output_format'].upper()}"
        )

        print(
            f"Records    : {result['records']:,}"
        )

    except Exception as exc:
        print()
        print(
            color(
                f"Conversion failed: {exc}",
                Colors.BRIGHT_RED
            )
        )

    pause()


# =============================================================================
# BATCH CONVERSION
# =============================================================================

def discover_files(directory, recursive=True):
    directory = Path(directory)

    if recursive:
        candidates = directory.rglob("*")
    else:
        candidates = directory.glob("*")

    files = []

    for path in candidates:
        if not path.is_file():
            continue

        if path.name.startswith("."):
            continue

        if "_rendered" in path.stem:
            continue

        try:
            if is_probably_binary(path):
                continue
        except Exception:
            continue

        files.append(path)

    return sorted(
        files,
        key=lambda p: str(p).lower()
    )


def batch_conversion():
    clear()

    title("BATCH REPORT CONVERSION")

    directory_value = ask(
        "Enter directory path"
    )

    if not directory_value:
        return

    directory = Path(
        directory_value
    ).expanduser()

    if not directory.exists():
        print(
            color(
                "Directory does not exist.",
                Colors.BRIGHT_RED
            )
        )

        pause()
        return

    if not directory.is_dir():
        print(
            color(
                "Selected path is not a directory.",
                Colors.BRIGHT_RED
            )
        )

        pause()
        return

    recursive = yes_no(
        "Search subdirectories recursively?",
        CONFIG.get(
            "recursive_batch",
            True
        )
    )

    files = discover_files(
        directory,
        recursive
    )

    if not files:
        print(
            color(
                "No text-based files found.",
                Colors.BRIGHT_YELLOW
            )
        )

        pause()
        return

    print()
    print(
        color(
            f"Discovered {len(files):,} file(s).",
            Colors.BRIGHT_CYAN
        )
    )

    output_format = choose_output_format()

    if output_format is None:
        return

    print()
    overwrite = yes_no(
        "Overwrite existing rendered files?",
        False
    )

    success_count = 0
    failure_count = 0

    print()

    for index, path in enumerate(files, 1):
        print(
            color(
                f"[{index}/{len(files)}] ",
                Colors.BRIGHT_YELLOW
            )
            + str(path)
        )

        try:
            output_path = default_output_path(
                path,
                output_format
            )

            if output_path.exists():
                if overwrite:
                    pass
                else:
                    output_path = unique_output_path(
                        output_path
                    )

            result = convert_file(
                path,
                output_format,
                output_path
            )

            success_count += 1

            print(
                color(
                    f"    ✓ {result['records']:,} records → {output_path.name}",
                    Colors.BRIGHT_GREEN
                )
            )

        except Exception as exc:
            failure_count += 1

            print(
                color(
                    f"    ✗ {exc}",
                    Colors.BRIGHT_RED
                )
            )

    print()
    line()

    print(
        color(
            f"Completed : {success_count:,}",
            Colors.BRIGHT_GREEN
        )
    )

    print(
        color(
            f"Failed    : {failure_count:,}",
            Colors.BRIGHT_RED if failure_count else Colors.BRIGHT_GREEN
        )
    )

    pause()


# =============================================================================
# PREVIEW
# =============================================================================

def preview_file():
    clear()

    title("REPORT PREVIEW")

    input_value = ask(
        "Enter input file path"
    )

    if not input_value:
        return

    path = Path(
        input_value
    ).expanduser()

    if not path.exists():
        print(
            color(
                "File not found.",
                Colors.BRIGHT_RED
            )
        )

        pause()
        return

    try:
        file_format = detect_format(path)

        if file_format == "binary":
            raise ValueError(
                "Binary file cannot be previewed."
            )

        amount = ask(
            "Number of records/lines to preview",
            CONFIG.get(
                "preview_lines",
                25
            )
        )

        try:
            amount = max(
                1,
                int(amount)
            )
        except ValueError:
            amount = 25

        print()

        for number, record in enumerate(
            iter_records(
                path,
                file_format
            ),
            1
        ):
            if number > amount:
                break

            print(
                color(
                    f"── Record {number} ──",
                    Colors.BRIGHT_CYAN
                )
            )

            for current_line in render_human(
                normalize_record(record)
            ):
                print(current_line)

            print()

        print(
            color(
                f"Input format: {file_format.upper()}",
                Colors.BRIGHT_YELLOW
            )
        )

    except Exception as exc:
        print(
            color(
                f"Preview failed: {exc}",
                Colors.BRIGHT_RED
            )
        )

    pause()


# =============================================================================
# FILE ANALYSIS
# =============================================================================

def count_lines(path):
    encoding = detect_encoding(path)

    count = 0

    with path.open(
        "r",
        encoding=encoding,
        errors="replace"
    ) as f:
        for _ in f:
            count += 1

    return count


def analyze_file():
    clear()

    title("REPORT ANALYSIS")

    input_value = ask(
        "Enter input file path"
    )

    if not input_value:
        return

    path = Path(
        input_value
    ).expanduser()

    if not path.exists():
        print(
            color(
                "File not found.",
                Colors.BRIGHT_RED
            )
        )

        pause()
        return

    try:
        stat = path.stat()

        file_format = detect_format(path)
        encoding = detect_encoding(path)

        print(
            color(
                "FILE INFORMATION",
                Colors.BRIGHT_CYAN
            )
        )

        line()

        information = [
            ("Name", path.name),
            ("Path", str(path.resolve())),
            ("Size", human_size(stat.st_size)),
            ("Format", file_format.upper()),
            ("Encoding", encoding),
            (
                "Modified",
                datetime.fromtimestamp(
                    stat.st_mtime
                ).isoformat(
                    sep=" ",
                    timespec="seconds"
                )
            ),
        ]

        for key, value in information:
            print(
                f"{color(key.ljust(14), Colors.BRIGHT_YELLOW)} : {value}"
            )

        print()

        print(
            color(
                "SHA256",
                Colors.BRIGHT_CYAN
            )
        )

        line()

        print(
            sha256_file(path)
        )

        if file_format == "text":
            print()

            print(
                color(
                    "TEXT STATISTICS",
                    Colors.BRIGHT_CYAN
                )
            )

            line()

            lines = count_lines(path)

            print(
                f"Lines : {lines:,}"
            )

        else:
            print()

            print(
                color(
                    "RECORD STATISTICS",
                    Colors.BRIGHT_CYAN
                )
            )

            line()

            count = 0

            for count, _ in enumerate(
                iter_records(
                    path,
                    file_format
                ),
                1
            ):
                pass

            print(
                f"Records : {count:,}"
            )

    except Exception as exc:
        print(
            color(
                f"Analysis failed: {exc}",
                Colors.BRIGHT_RED
            )
        )

    pause()


# =============================================================================
# SEARCH
# =============================================================================

def search_report():
    clear()

    title("SEARCH REPORT")

    input_value = ask(
        "Enter input file path"
    )

    if not input_value:
        return

    path = Path(
        input_value
    ).expanduser()

    if not path.exists():
        print(
            color(
                "File not found.",
                Colors.BRIGHT_RED
            )
        )

        pause()
        return

    query = ask(
        "Search term"
    )

    if not query:
        return

    regex_mode = yes_no(
        "Use regular expression?",
        False
    )

    case_sensitive = yes_no(
        "Case-sensitive search?",
        False
    )

    try:
        if regex_mode:
            flags = 0 if case_sensitive else re.IGNORECASE
            pattern = re.compile(
                query,
                flags
            )

        else:
            pattern = None

        encoding = detect_encoding(path)

        matches = 0

        with path.open(
            "r",
            encoding=encoding,
            errors="replace"
        ) as f:

            for line_number, line_text in enumerate(
                f,
                1
            ):
                text = line_text.rstrip("\r\n")

                if pattern is not None:
                    matched = bool(
                        pattern.search(text)
                    )

                else:
                    if case_sensitive:
                        matched = query in text
                    else:
                        matched = (
                            query.lower()
                            in text.lower()
                        )

                if matched:
                    matches += 1

                    print(
                        color(
                            f"[{line_number}] ",
                            Colors.BRIGHT_YELLOW
                        )
                        + text
                    )

        print()

        print(
            color(
                f"Matches found: {matches:,}",
                Colors.BRIGHT_GREEN
                if matches
                else Colors.BRIGHT_RED
            )
        )

    except re.error as exc:
        print(
            color(
                f"Invalid regular expression: {exc}",
                Colors.BRIGHT_RED
            )
        )

    except Exception as exc:
        print(
            color(
                f"Search failed: {exc}",
                Colors.BRIGHT_RED
            )
        )

    pause()


# =============================================================================
# SETTINGS
# =============================================================================

def settings_menu():
    while True:
        clear()

        title("INTELRENDER SETTINGS")

        print(
            f"  {color('1', Colors.BRIGHT_YELLOW)}  "
            f"Default output format : "
            f"{color(CONFIG.get('default_output_format'), Colors.BRIGHT_CYAN)}"
        )

        print(
            f"  {color('2', Colors.BRIGHT_YELLOW)}  "
            f"Preview records       : "
            f"{color(CONFIG.get('preview_lines'), Colors.BRIGHT_CYAN)}"
        )

        print(
            f"  {color('3', Colors.BRIGHT_YELLOW)}  "
            f"Recursive batch       : "
            f"{color(CONFIG.get('recursive_batch'), Colors.BRIGHT_CYAN)}"
        )

        print(
            f"  {color('4', Colors.BRIGHT_YELLOW)}  "
            f"Color interface       : "
            f"{color(CONFIG.get('color'), Colors.BRIGHT_CYAN)}"
        )

        print(
            f"  {color('5', Colors.BRIGHT_YELLOW)}  "
            f"Reset settings"
        )

        print(
            f"  {color('0', Colors.BRIGHT_RED)}  "
            f"Back"
        )

        choice = ask(
            "Select option"
        )

        if choice == "0":
            return

        elif choice == "1":
            selected = choose_output_format()

            if selected:
                CONFIG["default_output_format"] = selected
                save_config(CONFIG)

        elif choice == "2":
            value = ask(
                "Preview record count",
                CONFIG.get(
                    "preview_lines",
                    25
                )
            )

            try:
                value = max(
                    1,
                    int(value)
                )

                CONFIG["preview_lines"] = value
                save_config(CONFIG)

            except ValueError:
                print(
                    color(
                        "Invalid number.",
                        Colors.BRIGHT_RED
                    )
                )

                pause()

        elif choice == "3":
            CONFIG["recursive_batch"] = not CONFIG.get(
                "recursive_batch",
                True
            )

            save_config(CONFIG)

        elif choice == "4":
            CONFIG["color"] = not CONFIG.get(
                "color",
                True
            )

            save_config(CONFIG)

        elif choice == "5":
            CONFIG.clear()
            CONFIG.update(
                DEFAULT_CONFIG.copy()
            )

            save_config(CONFIG)

            print(
                color(
                    "Settings reset.",
                    Colors.BRIGHT_GREEN
                )
            )

            pause()

        else:
            print(
                color(
                    "Invalid option.",
                    Colors.BRIGHT_RED
                )
            )

            pause()


# =============================================================================
# HELP
# =============================================================================

def help_menu():
    clear()

    title("INTELRENDER HELP")

    print(
        color(
            "WHAT IS INTELRENDER?",
            Colors.BRIGHT_CYAN
        )
    )

    line()

    print(
        "IntelRender converts raw report/data files into structured,"
    )

    print(
        "human-readable documents."
    )

    print()

    print(
        color(
            "INPUT FORMATS",
            Colors.BRIGHT_CYAN
        )
    )

    line()

    inputs = [
        "JSON",
        "JSON Lines / NDJSON",
        "CSV",
        "TSV",
        "XML",
        "YAML",
        "INI / CFG / CONF",
        "ENV",
        "TXT",
        "LOG",
        "Generic text files",
    ]

    for item in inputs:
        print(
            f"  {color('•', Colors.BRIGHT_GREEN)} {item}"
        )

    print()

    print(
        color(
            "OUTPUT FORMATS",
            Colors.BRIGHT_CYAN
        )
    )

    line()

    outputs = [
        "TXT      - human-readable report",
        "HTML     - browser-friendly report",
        "Markdown - GitHub/documentation friendly",
        "JSON     - structured machine-readable data",
        "CSV      - spreadsheet/table format",
        "XML      - structured XML document",
    ]

    for item in outputs:
        print(
            f"  {color('•', Colors.BRIGHT_GREEN)} {item}"
        )

    print()

    print(
        color(
            "LARGE FILE HANDLING",
            Colors.BRIGHT_CYAN
        )
    )

    line()

    print(
        "Line-based formats are processed progressively rather than"
    )

    print(
        "requiring the entire file to be loaded into memory."
    )

    print(
        "JSON arrays and JSONL files also support streaming-style"
    )

    print(
        "record processing where applicable."
    )

    print()

    print(
        color(
            "IMPORTANT",
            Colors.BRIGHT_YELLOW
        )
    )

    print(
        "There is no practical 'infinite' file size."
    )

    print(
        "The tool avoids arbitrary record limits and processes"
    )

    print(
        "large reports progressively wherever possible."
    )

    pause()


# =============================================================================
# LOGIN
# =============================================================================

def login():
    attempts = 0
    maximum_attempts = 5

    while attempts < maximum_attempts:
        print_banner(
            LOGIN_BANNER
        )

        print()
        print(
            rainbow_text(
                "                         INTELRENDER"
            )
        )

        print(
            color(
                "                 Intelligence Report Renderer",
                Colors.BRIGHT_CYAN
            )
        )

        print()
        line()

        print(
            color(
                "                     AUTHENTICATION",
                Colors.BRIGHT_WHITE
            )
        )

        line()

        username = ask(
            "Username"
        )

        try:
            import getpass

            password = getpass.getpass(
                color(
                    "Password: ",
                    Colors.BRIGHT_WHITE
                )
            )

        except Exception:
            password = ask(
                "Password"
            )

        if (
            username == LOGIN_USERNAME
            and password == LOGIN_PASSWORD
        ):
            print()

            print(
                color(
                    "✓ Authentication successful.",
                    Colors.BRIGHT_GREEN
                )
            )

            pause(
                "Press ENTER to enter IntelRender..."
            )

            return True

        attempts += 1

        print()

        print(
            color(
                "✗ Invalid credentials.",
                Colors.BRIGHT_RED
            )
        )

        print(
            color(
                f"Attempts remaining: {maximum_attempts - attempts}",
                Colors.BRIGHT_YELLOW
            )
        )

        pause()

    print()

    print(
        color(
            "Maximum authentication attempts exceeded.",
            Colors.BRIGHT_RED
        )
    )

    return False


# =============================================================================
# MAIN MENU
# =============================================================================

def main_menu():
    while True:
        print_banner(
            MAIN_BANNER
        )

        print(
            color(
                f"  IntelRender v{VERSION}",
                Colors.BRIGHT_CYAN
            )
        )

        print(
            color(
                "  Offline Intelligence Report Rendering Engine",
                Colors.BRIGHT_BLACK
            )
        )

        print()

        line()

        menu_items = [
            ("1", "Convert a report"),
            ("2", "Batch convert directory"),
            ("3", "Preview report"),
            ("4", "Analyze report"),
            ("5", "Search report"),
            ("6", "Settings"),
            ("7", "Help"),
            ("0", "Exit"),
        ]

        for number, description in menu_items:
            if number == "0":
                number_color = Colors.BRIGHT_RED
            else:
                number_color = Colors.BRIGHT_YELLOW

            print(
                f"  {color(f'[{number}]', number_color)} "
                f"{color(description, Colors.BRIGHT_WHITE)}"
            )

        line()

        choice = ask(
            "Select option"
        )

        if choice == "1":
            single_conversion()

        elif choice == "2":
            batch_conversion()

        elif choice == "3":
            preview_file()

        elif choice == "4":
            analyze_file()

        elif choice == "5":
            search_report()

        elif choice == "6":
            settings_menu()

        elif choice == "7":
            help_menu()

        elif choice == "0":
            clear()

            print(
                rainbow_text(
                    "\n        IntelRender shutting down..."
                )
            )

            print(
                color(
                    "        Thank you for using IntelRender.",
                    Colors.BRIGHT_CYAN
                )
            )

            print()

            break

        else:
            print(
                color(
                    "Invalid option.",
                    Colors.BRIGHT_RED
                )
            )

            pause()


# =============================================================================
# EXCEPTION HANDLING
# =============================================================================

def main():
    try:
        if not sys.version_info >= (3, 9):
            print(
                "IntelRender requires Python 3.9 or newer."
            )

            sys.exit(1)

        if not login():
            sys.exit(1)

        main_menu()

    except KeyboardInterrupt:
        clear()

        print(
            color(
                "\nIntelRender interrupted by user.",
                Colors.BRIGHT_YELLOW
            )
        )

        print()

    except Exception as exc:
        print()

        print(
            color(
                "Fatal error:",
                Colors.BRIGHT_RED
            )
        )

        print(
            str(exc)
        )

        print()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
