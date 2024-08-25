import os
import subprocess
from audiobook_generator.core.utils import sanitize_filename

"""
Based on and thanks to: https://github.com/aedocw/epub2tts-edge
"""

def make_m4b(files, book_name, logger):
    filelist = "filelist.txt"
    sanitized_book_name = sanitize_filename(book_name)
    outputm4a = f"{sanitized_book_name}.m4a"
    outputm4b = f"{sanitized_book_name}.m4b"
    with open(filelist, "w") as f:
        for filename in files:
            filename = filename.replace("'", "'\\''")
            f.write(f"file '{filename}'\n")

    if os.path.exists(outputm4a) and os.path.exists(outputm4a + ".successfull"):
        logger.info(f"Skipping m4a conversion. Output file already exists.")
    else:
        ffmpeg_command = [
            "ffmpeg",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            filelist,
            "-codec:a",
            "flac",
            "-f",
            "mp4",
            "-strict",
            "-2",
            outputm4a,
        ]
        subprocess.run(ffmpeg_command)

        # Create a file representing the successful conversion
        with open(outputm4a + ".successfull", "w") as f:
            f.write("")

    if os.path.exists(outputm4b) and os.path.exists(outputm4b + ".successfull"):
        logger.info(f"Skipping m4b conversion. Output file already exists.")
    else:
        ffmpeg_command = [
            "ffmpeg",
            "-i",
            outputm4a,
            "-i",
            sanitized_book_name + "_FFMETADATAFILE",
            "-map_metadata",
            "1",
            "-codec",
            "aac",
            outputm4b,
        ]
        subprocess.run(ffmpeg_command)

        # Create a file representing the successful conversion
        with open(outputm4b + ".successfull", "w") as f:
            f.write("")
    
    os.remove(filelist)
    os.remove(sanitized_book_name + "_FFMETADATAFILE")
    # os.remove(outputm4a)
    # for f in files:
    #     os.remove(f)
    return outputm4b
