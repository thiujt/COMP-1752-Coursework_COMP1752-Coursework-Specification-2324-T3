import tkinter as tk
import video_library as lib
import font_manager as fonts

fonts.configure()

class VideoRatingUpdater:
    def __init__(self, window):
        window.geometry("500x300")
        window.title("Update Video Rating")

        lbl_video_id = tk.Label(window, text="Enter Video Number")
        lbl_video_id.grid(row=0, column=0, padx=10, pady=10)

        self.entry_video_id = tk.Entry(window, width=5)
        self.entry_video_id.grid(row=0, column=1, padx=10, pady=10)

        lbl_new_rating = tk.Label(window, text="Enter New Rating")
        lbl_new_rating.grid(row=1, column=0, padx=10, pady=10)

        self.entry_new_rating = tk.Entry(window, width=5)
        self.entry_new_rating.grid(row=1, column=1, padx=10, pady=10)

        btn_update_rating = tk.Button(window, text="Update Rating", command=self.update_rating)
        btn_update_rating.grid(row=2, column=0, padx=10, pady=10)

        self.txt_video_details = tk.Text(window, width=40, height=4, wrap="none")
        self.txt_video_details.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.lbl_status = tk.Label(window, text="", font=("Helvetica", 10))
        self.lbl_status.grid(row=4, column=0, columnspan=2, sticky="W", padx=10, pady=10)

    def update_rating(self):
        video_number = self.entry_video_id.get()
        new_rating = self.entry_new_rating.get()

        if not video_number.isdigit():
            self.lbl_status.configure(text="Invalid video number. Please enter a numeric value.")
            return

        if not new_rating.isdigit() or not (1 <= int(new_rating) <= 5):
            self.lbl_status.configure(text="Invalid rating. Please enter a value between 1 and 5.")
            return

        video_name = lib.get_name(video_number)
        if video_name is not None:
            lib.set_rating(video_number, int(new_rating))
            play_count = lib.get_play_count(video_number)

            video_details = f"{video_name}\nNew Rating: {new_rating}\nPlay Count: {play_count}"
            self.txt_video_details.delete("1.0", tk.END)
            self.txt_video_details.insert(tk.END, video_details)
            self.lbl_status.configure(text=f"Rating updated for {video_name}.")
        else:
            self.lbl_status.configure(text="Video not found.")
