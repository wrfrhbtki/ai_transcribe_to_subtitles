# subtitle_generator.py

import whisper

# Generate subtitles and save to SRT
def generate_srt(video_file, srt_file):
    model = whisper.load_model("base")
    result = model.transcribe(video_file, word_timestamps=True)

    with open(srt_file, "w") as f:
        idx = 1
        for segment in result["segments"]:
            words = segment.get("words", [])
            for word in words:
                if "start" in word and "end" in word and "word" in word:
                    start_time = word["start"]
                    end_time = word["end"]
                    text = word["word"]

                    f.write(f"{idx}\n")
                    f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
                    f.write(f"{text}\n\n")
                    idx += 1

# Convert seconds to SRT time format
def format_time(seconds):
    millis = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"
