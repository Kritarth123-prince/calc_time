import os
import wave
import argparse
import pkg_resources  
from mutagen import File as MutagenFile
from moviepy.editor import VideoFileClip

def get_audio_duration(filepath):
    try:
        if filepath.lower().endswith(".wav"):
            with wave.open(filepath, "rb") as wav_file:
                frame_count = wav_file.getnframes()
                sample_rate = wav_file.getframerate()
                return frame_count / float(sample_rate)

        audio = MutagenFile(filepath)
        if audio and audio.info:
            return audio.info.length
        return 0
    except Exception:
        return 0

def get_version():
    try:
        return pkg_resources.get_distribution("calc_time").version
    except pkg_resources.DistributionNotFound:
        return "Package not installed!" 

def get_video_duration(filepath):
    try:
        with VideoFileClip(filepath) as video:
            return video.duration
    except Exception:
        return 0
    
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(seconds % 60)
    return f"{hours} hours, {minutes} minutes, {remaining_seconds} seconds"

def calculate_total_duration(directory, include_subdirs=True):
    supported_audio_formats = {".mp3", ".wav", ".m4a"}
    supported_video_formats = {".mp4", ".mkv", ".mov", ".webm"}

    total_duration = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()

            if ext in supported_audio_formats:
                total_duration += get_audio_duration(filepath)
            elif ext in supported_video_formats:
                total_duration += get_video_duration(filepath)

        if not include_subdirs:
            break

    return total_duration

def main():
    parser = argparse.ArgumentParser(description="Calculate total duration of audio and video files in a directory.")
    parser.add_argument("directory", type=str, help="Path to the directory to scan.")
    parser.add_argument("--no-subdirs", action="store_true", help="Do not include subdirectories.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {get_version()}")

    args = parser.parse_args()

    directory = args.directory
    include_subdirs = not args.no_subdirs

    if os.path.exists(directory):
        total_duration = calculate_total_duration(directory, include_subdirs=include_subdirs)
        formatted_duration = format_time(total_duration)
        print(f"Total duration: {formatted_duration}")
    else:
        print(f"Directory {directory} does not exist.")

if __name__ == "__main__":
    main()
