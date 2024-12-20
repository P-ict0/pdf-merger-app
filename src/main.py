import sys
import tkinter as tk
import webbrowser
from tkinter import messagebox
from tkinter import ttk
import requests

from tools.compressor import Compressor
from tools.encryptor import Encryptor
from tools.merger import Merger

import styles
from config import (
    APP_NAME,
    APP_AUTHOR,
    APP_URL,
    AUTHOR_GITHUB,
    APP_VERSION,
)


def check_for_updates(current_version: str) -> None:
    """
    Check for updates by comparing the current version with the latest version on GitHub.
    """
    try:
        response = requests.get(
            "https://raw.githubusercontent.com/P-ict0/pdf-tools-app/refs/heads/main/VERSION"
        )
        latest_version = response.text.strip()

        if latest_version > current_version:
            prompt_update(latest_version)
        else:
            print("You are using the latest version.")

    except Exception:
        pass  # Silently ignore any errors


def prompt_update(latest_version: str) -> None:
    """
    Prompt the user to download the latest version of the application.
    """
    if messagebox.askyesno(
        "Update Available",
        f"A new version ({latest_version}) is available. Do you want to download it?",
    ):
        webbrowser.open(f"{APP_URL}/releases/latest")
        sys.exit(0)


def main() -> None:
    """
    Main function to create the application window and run the main event loop.
    """
    print(f"{APP_NAME} version {APP_VERSION}")
    check_for_updates(APP_VERSION)

    # Create the main window
    root = tk.Tk()
    root.title(APP_NAME)
    root.geometry("900x600")
    root.resizable(False, False)

    # Set up styles
    style = ttk.Style()
    styles.set_theme(style)

    # Create a frame
    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True, fill=tk.BOTH)

    # Title Label
    label = ttk.Label(frame, text="Select a PDF Tool:", font=styles.FONT_LARGE_BOLD)
    label.pack(pady=20)

    # Available tools mapped to their classes
    tools = {
        "PDF Merger": Merger,
        "PDF Encrypt/Decrypt": Encryptor,
        "PDF Compressor": Compressor,
    }

    # Function to open selected tool
    def open_tool(tool_class) -> None:
        root.withdraw()
        tool_class(root_window=root)

    # Function to dynamically create tool buttons
    def create_tool_buttons() -> None:
        tool_frame = ttk.Frame(frame)
        tool_frame.pack(pady=10)

        max_cols = 3
        row = 0
        col = 0

        for tool_name, tool_class in tools.items():
            btn = ttk.Button(
                tool_frame,
                text=tool_name,
                command=lambda c=tool_class: open_tool(c),
                width=20,
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    create_tool_buttons()

    # Credits and version at the bottom
    bottom_frame = ttk.Frame(frame)
    bottom_frame.pack(side="bottom", fill=tk.X)

    # Credits label
    def open_author_github(event: tk.Event) -> None:
        webbrowser.open(AUTHOR_GITHUB)

    credits_label = ttk.Label(
        bottom_frame,
        text=f"Created by {APP_AUTHOR}",
        foreground=styles.HIGHLIGHT_COLOR,
        cursor="hand2",
        font=styles.FONT_DEFAULT,
        background=styles.BG_COLOR,
    )
    credits_label.pack(side="left", padx=10, pady=10)
    credits_label.bind("<Button-1>", open_author_github)

    # Version label
    version_label = ttk.Label(
        bottom_frame,
        text=f"Version {APP_VERSION}",
        foreground=styles.FG_COLOR,
        font=styles.FONT_DEFAULT,
        background=styles.BG_COLOR,
    )
    version_label.pack(side="right", padx=10, pady=10)

    # Handle the close event
    def on_root_close() -> None:
        root.destroy()
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_root_close)

    root.mainloop()


if __name__ == "__main__":
    main()
