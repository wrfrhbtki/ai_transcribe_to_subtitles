# main.py

from ai_subtitle_generator import generate_srt
from srt_editor import edit_srt
from subtitle_adder import select_position, add_subtitles
import os

def main():
    video_file = "input.mp4"  # Replace with your video file
    srt_file = "subtitles.srt"
    output_file = "output_with_subtitles.mp4"

    # Step 1: Generate subtitles
    generate_srt(video_file, srt_file)
    print(f"Generated subtitles saved to {srt_file}")

    # Step 2: Edit subtitles
    edit_srt(srt_file)
    print("Subtitles edited successfully.")

    # Step 3: Select subtitle position
    position = select_position(video_file)
    print(f"Selected subtitle position: {position}")

    # Step 4: Add subtitles to the video
    add_subtitles(video_file, srt_file, output_file, position)
    print(f"Final video saved to {output_file}")

    # Clean up
    if os.path.exists(srt_file):
        os.remove(srt_file)

if __name__ == "__main__":
    main()
