import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import video_library as lib
import font_manager as fonts

fonts.configure()

class VideoPlaylistCreator:
    def __init__(self, window):
        window.geometry("600x450")
        window.title("Create Video Playlist")

        lbl_video_id = tk.Label(window, text="Enter Video Number")
        lbl_video_id.grid(row=0, column=0, padx=10, pady=10)

        self.entry_video_id = tk.Entry(window, width=5)
        self.entry_video_id.grid(row=0, column=1, padx=10, pady=10)

        btn_add_video = tk.Button(window, text="Add to Playlist", command=self.add_video)
        btn_add_video.grid(row=0, column=2, padx=10, pady=10)

        lbl_search = tk.Label(window, text="Search (by Title or Director)")
        lbl_search.grid(row=1, column=0, padx=10, pady=10)

        self.entry_search = tk.Entry(window, width=20)
        self.entry_search.grid(row=1, column=1, padx=10, pady=10)

        btn_search = tk.Button(window, text="Search", command=self.search_videos)
        btn_search.grid(row=1, column=2, padx=10, pady=10)

        self.txt_playlist = scrolledtext.ScrolledText(window, width=50, height=15, wrap="none")
        self.txt_playlist.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        btn_play_playlist = tk.Button(window, text="Play Playlist", command=self.play_playlist)
        btn_play_playlist.grid(row=3, column=0, padx=10, pady=10)

        btn_reset_playlist = tk.Button(window, text="Reset Playlist", command=self.reset_playlist)
        btn_reset_playlist.grid(row=3, column=1, padx=10, pady=10)

        self.lbl_status = tk.Label(window, text="", font=("Helvetica", 10))
        self.lbl_status.grid(row=4, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        self.playlist = []

    def add_video(self):
        video_number = self.entry_video_id.get()

        if not video_number.isdigit():
            self.lbl_status.configure(text="Invalid ID. Please enter a numeric value.")
            return

        video_name = lib.get_name(video_number)
        if video_name:
            self.playlist.append(video_name)
            self.lbl_status.configure(text=f"Added {video_name} to playlist.")
            self.update_playlist_text()
        else:
            self.lbl_status.configure(text="Video not found.")

    def search_videos(self):
        search_query = self.entry_search.get().lower()
        search_results = [video_name for video_number, video_name in lib.library.items()
                          if search_query in video_name.get_name().lower() or search_query in video_name.get_director().lower()]
        self.update_playlist_text(search_results)

    def update_playlist_text(self, search_results=None):
        if search_results is None:
            search_results = self.playlist
        self.txt_playlist.delete("1.0", tk.END)
        for video_name in search_results:
            self.txt_playlist.insert(tk.END, f"{video_name}\n")

    def play_playlist(self):
        # Implement playlist playback logic
        pass

    def reset_playlist(self):
        self.playlist = []
        self.txt_playlist.delete("1.0", tk.END)
        self.lbl_status.configure(text="Playlist reset.")
