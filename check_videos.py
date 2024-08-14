import tkinter as tk
import tkinter.scrolledtext as tkst
import video_library as lib
import font_manager as fonts

# Configure the font settings using the external font_manager module.
fonts.configure()


def set_text(text_area, content):
  """
  A helper function to update the content of a Text or ScrolledText widget.
  :param text_area: The widget to update (either Text or ScrolledText)
  :param content: The content to insert into the widget
  """
  text_area.delete("1.0", tk.END)  # Clear existing content in the widget
  text_area.insert("1.0", content)  # Insert new content starting from the top (1.0) of the widget


class CheckVideos:
  def __init__(self, window):
    """
    Initialize the CheckVideos window with various widgets for interacting with the video library.
    :param window: The main application window
    """
    # Set the size of the window
    window.geometry("750x350")

    # Set the title of the window
    window.title("Check Videos")

    # Create a button that lists all videos when clicked
    list_videos_btn = tk.Button(window, text="List All Videos", command=self.list_videos_clicked)
    list_videos_btn.grid(row=0, column=0, padx=10, pady=10)  # Place the button at row 0, column 0

    # Create a label instructing the user to enter a video number
    enter_lbl = tk.Label(window, text="Enter Video Number")
    enter_lbl.grid(row=0, column=1, padx=10, pady=10)  # Place the label next to the button

    # Create an entry widget for the user to input the video number
    self.input_txt = tk.Entry(window, width=3)
    self.input_txt.grid(row=0, column=2, padx=10, pady=10)  # Place the entry box next to the label

    # Create a button to check the details of the entered video number
    check_video_btn = tk.Button(window, text="Check Video", command=self.check_video_clicked)
    check_video_btn.grid(row=0, column=3, padx=10, pady=10)  # Place the button next to the entry box

    # Create a ScrolledText widget to display the list of all videos in the library
    self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")
    self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)  # Span the widget across 3 columns

    # Create a Text widget to display the details of the selected video
    self.video_txt = tk.Text(window, width=40, height=4, wrap="none")
    self.video_txt.grid(row=2, column=0, columnspan=3, padx=10, pady=10)  # Span the widget across 3 columns

  def list_videos_clicked(self):
    """
    Event handler for the "List All Videos" button.
    When clicked, it retrieves and displays the list of all videos from the library.
    """
    video_list = lib.list_all()  # Retrieve the list of all videos from the video library
    set_text(self.list_txt, video_list)  # Display the video list in the ScrolledText widget

  def check_video_clicked(self):
    """
    Event handler for the "Check Video" button.
    When clicked, it checks the entered video number and displays the corresponding video details.
    """
    video_number = self.input_txt.get()  # Get the video number entered by the user
    if video_number in lib.library:  # Check if the video number exists in the library
      # Retrieve and format the video details
      video_details = f"Name: {lib.get_name(video_number)}\n" \
                      f"Director: {lib.get_director(video_number)}\n" \
                      f"Rating: {lib.get_rating(video_number)}\n" \
                      f"Play Count: {lib.get_play_count(video_number)}"
      set_text(self.video_txt, video_details)  # Display the video details in the Text widget
    else:
      # If the video number is not found, display an error message
      set_text(self.video_txt, "Video not found.")


# To run the CheckVideos window, create an instance of Tk and pass it to the CheckVideos class.
if __name__ == "__main__":
  root = tk.Tk()  # Create the main window instance
  CheckVideos(root)  # Instantiate the CheckVideos class with the main window
  root.mainloop()  # Start the Tkinter event loop
