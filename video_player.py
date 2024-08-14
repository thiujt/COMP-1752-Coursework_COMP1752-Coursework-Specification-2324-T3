import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pygame
import video_library as lib
import os

class VideoPlayerGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Video Player")
        self.library = lib.library
        self.playlist = []
        self.current_media_path = None
        self.is_playing = False
        self.is_audio = False

        pygame.mixer.init()  # Initialize pygame mixer for audio playback

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.tab_control = ttk.Notebook(window)
        self.check_videos_tab = ttk.Frame(self.tab_control)
        self.create_playlist_tab = ttk.Frame(self.tab_control)
        self.update_ratings_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.check_videos_tab, text="Check Videos")
        self.tab_control.add(self.create_playlist_tab, text="Create Playlist")
        self.tab_control.add(self.update_ratings_tab, text="Update Ratings")
        self.tab_control.pack(expand=1, fill="both")

        self.init_check_videos_tab()
        self.init_create_playlist_tab()
        self.init_update_ratings_tab()

    def init_check_videos_tab(self):
        tk.Button(self.check_videos_tab, text="List All Videos", command=self.list_videos_clicked).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.check_videos_tab, text="Enter Video Number").grid(row=0, column=1, padx=10, pady=10)
        self.input_txt_check = tk.Entry(self.check_videos_tab, width=5)
        self.input_txt_check.grid(row=0, column=2, padx=10, pady=10)
        tk.Button(self.check_videos_tab, text="Check Video", command=self.check_video_clicked).grid(row=0, column=3, padx=10, pady=10)
        tk.Button(self.check_videos_tab, text="Play", command=self.play_media).grid(row=1, column=0, padx=10, pady=10)
        tk.Button(self.check_videos_tab, text="Stop", command=self.stop_media).grid(row=1, column=1, padx=10, pady=10)
        self.list_txt = tk.Text(self.check_videos_tab, width=60, height=20)
        self.list_txt.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
        self.image_label = tk.Label(self.check_videos_tab)
        self.image_label.grid(row=2, column=4, padx=10, pady=10)

    def init_create_playlist_tab(self):
        tk.Label(self.create_playlist_tab, text="Enter Video Number").grid(row=0, column=0, padx=10, pady=10)
        self.entry_video_id = tk.Entry(self.create_playlist_tab, width=5)
        self.entry_video_id.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.create_playlist_tab, text="Add to Playlist", command=self.add_video_to_playlist).grid(row=0, column=2, padx=10, pady=10)
        self.playlist_txt = tk.Text(self.create_playlist_tab, width=60, height=20)
        self.playlist_txt.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    def init_update_ratings_tab(self):
        tk.Label(self.update_ratings_tab, text="Enter Video Number").grid(row=0, column=0, padx=10, pady=10)
        self.entry_video_id_update = tk.Entry(self.update_ratings_tab, width=5)
        self.entry_video_id_update.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(self.update_ratings_tab, text="Enter New Rating").grid(row=1, column=0, padx=10, pady=10)
        self.entry_new_rating = tk.Entry(self.update_ratings_tab, width=5)
        self.entry_new_rating.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self.update_ratings_tab, text="Update Rating", command=self.update_rating).grid(row=2, column=0, padx=10, pady=10)
        self.txt_video_details = tk.Text(self.update_ratings_tab, width=40, height=4)
        self.txt_video_details.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.lbl_status = tk.Label(self.update_ratings_tab, text="", font=("Helvetica", 10))
        self.lbl_status.grid(row=4, column=0, columnspan=2, sticky="W", padx=10, pady=10)

    def list_videos_clicked(self):
        video_list = lib.list_all()
        self.list_txt.delete("1.0", tk.END)
        self.list_txt.insert(tk.END, video_list)

    def check_video_clicked(self):
        video_number = self.input_txt_check.get()
        if video_number in self.library:
            media_path = self.library[video_number].get_media_path()
            image_path = self.library[video_number].get_image_path()
            self.is_audio = media_path.lower().endswith('.mp3')
            self.current_media_path = media_path
            self.display_image(image_path)
        else:
            self.show_message("Video number not found.")

    def play_media(self):
        if self.current_media_path:
            if self.is_audio:
                self.play_audio(self.current_media_path)
            else:
                self.play_video(self.current_media_path)
        else:
            self.show_message("No media selected.")

    def stop_media(self):
        if self.is_audio:
            pygame.mixer.music.stop()
        self.is_playing = False

    def add_video_to_playlist(self):
        video_number = self.entry_video_id.get()
        video_name = lib.get_name(video_number)
        if video_name:
            self.playlist.append(video_name)
            self.update_playlist_text()

    def update_playlist_text(self):
        self.playlist_txt.delete("1.0", tk.END)
        for video in self.playlist:
            self.playlist_txt.insert(tk.END, f"{video}\n")

    def update_rating(self):
        video_number = self.entry_video_id_update.get()
        new_rating = self.entry_new_rating.get()

        if not video_number.isdigit() or not (new_rating.isdigit() and 1 <= int(new_rating) <= 5):
            self.lbl_status.configure(text="Invalid input. Ensure video number is numeric and rating is between 1 and 5.")
            return

        if lib.get_name(video_number):
            lib.set_rating(video_number, int(new_rating))
            play_count = lib.get_play_count(video_number)
            self.txt_video_details.delete("1.0", tk.END)
            self.txt_video_details.insert(tk.END, f"{lib.get_name(video_number)}\nNew Rating: {new_rating}\nPlay Count: {play_count}")
            self.lbl_status.configure(text=f"Rating updated for {lib.get_name(video_number)}.")
        else:
            self.lbl_status.configure(text="Video not found.")

    def play_video(self, video_path):
        self.current_media_path = video_path
        self.is_playing = True
        print(f"Playing video: {video_path}")

    def stop_video(self):
        print("Stopping video playback")
        self.is_playing = False

    def play_audio(self, audio_path):
        if os.path.isfile(audio_path):
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            self.is_playing = True
        else:
            self.show_message("Audio file not found.")

    def display_image(self, image_path):
        if os.path.isfile(image_path):
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
        else:
            self.show_message(f"Image file not found: {image_path}")

    def show_message(self, message):
        messagebox.showinfo("Information", message)

    def on_close(self):
        if self.is_audio and self.is_playing:
            pygame.mixer.music.stop()
        self.window.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerGUI(root)
    root.mainloop()
