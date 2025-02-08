import os
import shutil
import argparse
from datetime import datetime, timedelta, date
from PIL import Image
import subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to get the date based on the option provided
def get_target_date(option, date_input=None):
    now = datetime.now()
    
    if option == "onehour":
        return now - timedelta(hours=1), now.strftime("%d-%m-%Y")
    
    elif option == "today":
        today = date.today()
        return today, today.strftime("%d-%m-%Y")
    
    elif option == "date":
        if not date_input:
            raise ValueError("Date input required in format: dd,mm,yyyy")
        day, month, year = map(int, date_input.split(','))
        target_date = date(year, month, day)
        return target_date, target_date.strftime("%d-%m-%Y")
    
    else:
        raise ValueError("Invalid option! Use onehour, today, or date.")

# Function to check if a file is a voice note
def is_voice_note(file_path):
    try:
        # Use ffmpeg to check if it's an audio file with duration <= 180s
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
                                 '-of', 'default=noprint_wrappers=1:nokey=1', file_path], 
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        duration_str = result.stdout.decode().strip()
        duration = float(duration_str)
        
        result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', 
                                 '-show_entries', 'stream=codec_type', 
                                 '-of', 'default=noprint_wrappers=1:nokey=1', file_path], 
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        codec_type = result.stdout.decode().strip()

        return codec_type == 'audio' and duration <= 180
    except:
        return False

# Function to check if a file was created within the last hour
def file_within_timeframe(file_path, time_threshold):
    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
    return file_time >= time_threshold

# Function to check if a file was created on a specific date
def file_created_on_date(file_path, target_date):
    file_date = datetime.fromtimestamp(os.path.getctime(file_path)).date()
    return file_date == target_date

# Function to handle duplicate file names
def handle_file_overwrite(file_path):
    base, ext = os.path.splitext(file_path)
    counter = 1
    new_file_path = file_path
    while os.path.exists(new_file_path):
        new_file_path = f"{base}_{counter}{ext}"
        counter += 1
    return new_file_path

# Function to process a file
def process_file(file_path, option, time_threshold, image_dir, video_dir, audio_dir):
    try:
        # Determine if file should be processed based on option
        if option == "onehour" and not file_within_timeframe(file_path, time_threshold):
            return
        elif option in ["today", "date"] and not file_created_on_date(file_path, time_threshold):
            return

        # Check if file is an image
        try:
            with Image.open(file_path) as img:
                if img.width < 641 or img.height < 641:
                    return
                new_image_path = os.path.join(image_dir, f"{os.path.basename(file_path)}.png")
                new_image_path = handle_file_overwrite(new_image_path)
                img.save(new_image_path)
                return
        except:
            pass

        # Check if file is a video
        result = subprocess.run(['ffmpeg', '-i', file_path], stderr=subprocess.PIPE)
        output = result.stderr.decode()
        if 'Video' in output:
            new_file_name = os.path.splitext(os.path.basename(file_path))[0] + ".mp4"
            new_file_path = os.path.join(video_dir, new_file_name)
            new_file_path = handle_file_overwrite(new_file_path)
            shutil.copy(file_path, new_file_path)
        elif is_voice_note(file_path):
            new_file_name = os.path.basename(file_path) + ".mp3"
            new_file_path = os.path.join(audio_dir, new_file_name)
            new_file_path = handle_file_overwrite(new_file_path)
            shutil.copy(file_path, new_file_path)

    except:
        pass

# Main script execution
def main():
    parser = argparse.ArgumentParser(description="Copy Snapchat media files based on time criteria.")
    parser.add_argument("option", choices=["onehour", "today", "date"], help="Select mode: onehour, today, or date")
    parser.add_argument("--date", type=str, help="Specify date in format: dd,mm,yyyy (Required for date option)")

    args = parser.parse_args()

    try:
        time_threshold, today_str = get_target_date(args.option, args.date)
    except ValueError as e:
        print(e)
        return

    # Define source and destination directories
    source_dir = "/data/data/com.snapchat.android/files/native_content_manager/"
    destination_dir = f"/storage/emulated/0/snap/.{today_str}"
    image_dir = os.path.join(destination_dir, "images")
    video_dir = os.path.join(destination_dir, "videos")
    audio_dir = os.path.join(destination_dir, "audios")

    # Create necessary directories
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(os.path.join(destination_dir, "empty"), exist_ok=True)

    # Collect all files
    all_files = [os.path.join(root, file) for root, _, files in os.walk(source_dir) for file in files]

    # Process files using ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, file_path, args.option, time_threshold, image_dir, video_dir, audio_dir) for file_path in all_files]
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Processing files", unit="file"):
            pass

if __name__ == "__main__":
    main()