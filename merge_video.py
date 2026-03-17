import os
import subprocess

# --- Configuration ---
START_INDEX = 718  # 508  # 599
END_INDEX = 739  # 512  # 616
FILE_PATTERN = "./LastRideDaisy2025/DVR00{:03d}.MP4"
OUTPUT_FILENAME = "LastRideDaisy2025.mp4"
TEMP_LIST_FILE = "file_list_to_merge.txt"
# ---------------------


def merge_videos_ffmpeg(start, end, pattern, output_name, list_file):
    """
    Generates a list of files and uses FFmpeg concat demuxer to merge them.
    Requires FFmpeg to be installed on the system.
    """
    # 1. Generate the ordered list of file names
    file_list = []
    for i in range(start, end + 1):
        filename = pattern.format(i)
        file_list.append(filename)

    # 2. Check if all files exist
    missing_files = [f for f in file_list if not os.path.exists(f)]
    if missing_files:
        print(
            f"⚠️ Error: The following files are missing and will be skipped: {missing_files}"
        )
        # Filter out missing files for the merge list
        file_list = [f for f in file_list if os.path.exists(f)]
        if not file_list:
            print("No files left to merge. Exiting.")
            return

    # 3. Create the temporary list file for FFmpeg
    try:
        with open(list_file, "w") as f:
            for filename in file_list:
                # FFmpeg concat demuxer format requires 'file ' followed by the path
                # Use single quotes for compatibility with potential spaces in filenames
                f.write(f"file '{filename}'\n")
        print(f"Created list file: {list_file}")

        # 4. Construct the FFmpeg command
        # -f concat: specifies the concat demuxer
        # -safe 0: allows for relative or complex file paths (important for this method)
        # -i {list_file}: specifies the input file list
        # -c copy: copies the streams without re-encoding (FAST and LOSSLESS, but requires matching stream properties)
        # {output_name}: specifies the final output file
        ffmpeg_command = [
            "ffmpeg",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            list_file,
            "-c",
            "copy",
            output_name,
        ]

        # 5. Execute the FFmpeg command
        print("Starting video merge...")
        subprocess.run(ffmpeg_command, check=True)
        print(f"✅ Successfully merged videos into {output_name}")

    except FileNotFoundError:
        print("❌ Error: FFmpeg is not installed or not in your system's PATH.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during FFmpeg execution: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    finally:
        # 6. Clean up the temporary list file
        if os.path.exists(list_file):
            os.remove(list_file)
            print(f"Cleaned up temporary list file: {list_file}")


# --- Run the function ---
if __name__ == "__main__":
    merge_videos_ffmpeg(
        START_INDEX, END_INDEX, FILE_PATTERN, OUTPUT_FILENAME, TEMP_LIST_FILE
    )
