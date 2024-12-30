# subtitle_adder.py

import cv2
from moviepy.editor import VideoFileClip, AudioFileClip
import os 
# Let the user select subtitle position
def select_position(video_file):
    def get_position(event, x, y, flags, param):
        nonlocal position
        if event == cv2.EVENT_LBUTTONDOWN:  # Left mouse button click
            position = (x, y)
            cv2.destroyAllWindows()

    cap = cv2.VideoCapture(video_file)
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Unable to read video")
    cap.release()

    position = None

    # Resize frame to fit screen dimensions
    screen_width = 800  # Adjust based on your screen size
    screen_height = 600  # Adjust based on your screen size
    frame_height, frame_width = frame.shape[:2]

    # Calculate scaling factor to fit frame in the window
    scale = min(screen_width / frame_width, screen_height / frame_height)
    resized_frame = cv2.resize(frame, (int(frame_width * scale), int(frame_height * scale)))

    # Add a message to the frame asking the user to click
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "Click on the area where you want subtitles"
    font_scale = 1
    thickness = 2
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = int((resized_frame.shape[1] - text_size[0]) / 2)
    text_y = 30  # Positioning the text a bit above the center

    cv2.putText(resized_frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

    # Display resized frame and capture click position
    cv2.imshow("Click to Select Subtitle Position (Resized)", resized_frame)
    cv2.setMouseCallback("Click to Select Subtitle Position (Resized)", get_position)
    cv2.waitKey(0)

    # Adjust position back to original scale
    if position is not None:
        position = (int(position[0] / scale), int(position[1] / scale))
    return position

# Parse SRT file
def parse_srt(srt_file):
    subtitles = []
    with open(srt_file, "r") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):
            start_time = parse_srt_time(lines[i + 1].split(" --> ")[0])
            end_time = parse_srt_time(lines[i + 1].split(" --> ")[1])
            text = lines[i + 2].strip()
            subtitles.append({"start": start_time, "end": end_time, "text": text})
    return subtitles

# Convert SRT time to seconds
def parse_srt_time(time_str):
    hours, minutes, seconds = map(float, time_str.replace(",", ".").split(":"))
    return hours * 3600 + minutes * 60 + seconds

# Add subtitles and save video
def add_subtitles(video_file, srt_file, output_file, position):
    subtitles = parse_srt(srt_file)
    video = cv2.VideoCapture(video_file)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    temp_video = "temp_video.mp4"
    output_video = cv2.VideoWriter(temp_video, fourcc, fps, (frame_width, frame_height))

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break

        current_frame = int(video.get(cv2.CAP_PROP_POS_FRAMES))
        current_time = current_frame / fps

        # Draw subtitles
        for subtitle in subtitles:
            start_time = subtitle["start"]
            end_time = subtitle["end"]
            text = subtitle["text"]

            if start_time <= current_time <= end_time:
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 2
                color = (255, 255, 255)
                thickness = 4

                text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                text_x = position[0] - (text_size[0] // 2)
                text_y = position[1]

                cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness, lineType=cv2.LINE_AA)

        output_video.write(frame)

    video.release()
    output_video.release()

    # Combine the original audio with the processed video
    original_audio = AudioFileClip(video_file)
    processed_video = VideoFileClip(temp_video).set_audio(original_audio)
    processed_video.write_videofile(output_file, codec="libx264", audio_codec="aac")

    # Delete temporary video file
    os.remove(temp_video)
