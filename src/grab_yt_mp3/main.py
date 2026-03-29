import sys
import os
import platform
import subprocess
import argparse
from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()

def search_song(query: str) -> list:
    """Searches YouTube Music for songs and returns a list of results."""
    ytm = YTMusic()
    console.print(f"[cyan]Searching for '{query}'...[/cyan]")
    
    # filter="songs" ensures we get Official Audio, not Music Videos
    results = ytm.search(query, filter="songs", limit=5)
    return results

def display_results(results: list) -> dict:
    """Displays results in a rich table and prompts user for selection."""
    if not results:
        console.print("[red]No results found.[/red]")
        return None

    table = Table(title="Search Results")
    table.add_column("Index", justify="center", style="magenta")
    table.add_column("Title", style="white")
    table.add_column("Artist", style="green")
    table.add_column("Album", style="yellow")
    table.add_column("Duration", justify="right", style="blue")

    for i, res in enumerate(results):
        artists = ", ".join([a['name'] for a in res['artists']])
        album = res.get('album', {}).get('name', 'N/A') if res.get('album') else 'N/A'
        table.add_row(str(i+1), res['title'], artists, album, res.get('duration', 'N/A'))

    console.print(table)
    
    choices =[str(i+1) for i in range(len(results))]
    choice = Prompt.ask("Select a song to download", choices=choices)
    
    return results[int(choice) - 1]

def download_song(url_or_id: str, output_dir: str, title: str = None):
    """Downloads best audio, converts to mp3, embeds metadata, and saves to output folder."""
    if url_or_id.startswith("http://") or url_or_id.startswith("https://"):
        url = url_or_id
    else:
        url = f"https://music.youtube.com/watch?v={url_or_id}"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        # Save output into the designated directory
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'writethumbnail': True,  
        'postprocessors':[
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0', 
            },
            {
                'key': 'FFmpegMetadata',
                'add_metadata': True,
            },
            {
                'key': 'EmbedThumbnail',
            },
        ],
        'quiet': False,
    }

    display_title = title if title else url
    console.print(f"\n[bold green]Downloading:[/bold green] {display_title}...")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        console.print("\n[bold green]✓ Download and conversion complete![/bold green]")
        return True
    except Exception as e:
        console.print(f"\n[bold red]Download Failed:[/bold red] {e}")
        console.print("[yellow]Hint: Ensure 'ffmpeg' is installed and added to your system PATH![/yellow]")
        return False

def open_folder(path: str):
    """Opens the directory in the default system file explorer (cross-platform)."""
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", path])
        else:  # Linux
            subprocess.Popen(["xdg-open", path])
    except Exception as e:
        console.print(f"[red]Could not open folder: {e}[/red]")

def run():
    parser = argparse.ArgumentParser(
        description="A beautiful, interactive command-line tool to search and download high-quality MP3s from YouTube Music."
    )
    parser.add_argument(
        "query", 
        nargs="*", 
        help="The search query, song name, or a direct YouTube URL"
    )
    parser.add_argument(
        "-o", "--output",
        default="yt-mp3-downloads",
        help="Output directory for downloaded MP3s (default: ./yt-mp3-downloads)"
    )
    
    args = parser.parse_args()

    # Setup Output Directory
    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Get query
    if args.query:
        query = " ".join(args.query)
    else:
        query = Prompt.ask("\n[bold cyan]Enter song name, search query, or YouTube URL[/bold cyan]")
    
    # Check if URL directly provided
    if query.startswith("http://") or query.startswith("https://"):
        success = download_song(query, output_dir)
        if success:
            console.input("\n[bold cyan]Press Enter to open the output folder...[/bold cyan]")
            open_folder(output_dir)
        return

    # 2. Search
    results = search_song(query)
    
    # 3. Select
    selected = display_results(results)
    
    # 4. Download
    if selected:
        success = download_song(selected['videoId'], output_dir, title=selected['title'])
        
        # 5. Open Explorer Prompt
        if success:
            console.input("\n[bold cyan]Press Enter to open the output folder...[/bold cyan]")
            open_folder(output_dir)

def main():
    try:
        run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Exiting cleanly...[/yellow]")

if __name__ == "__main__":
    main()