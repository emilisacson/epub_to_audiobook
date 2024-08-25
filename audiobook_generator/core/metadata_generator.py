import os
from audiobook_generator.core.utils import sanitize_filename, get_duration, convert_milliseconds

"""
Based on and thanks to: https://github.com/aedocw/epub2tts-edge
"""

def generate_metadata(files, author, title, chapter_titles, logger):
    chap = 1
    start_time = 0
    processed_chap = 0
    logger.info(
        f"Starting metadata generation for {title}"
    )

    sanitized_filename = sanitize_filename(title)

    if os.path.exists(sanitized_filename + "_latest_metadata_chapter.ini"):
        with open(sanitized_filename + "_latest_metadata_chapter.ini", "r") as f:
            content = f.read()

            # Split the content into lines
            lines = content.splitlines()

            # Extract values assuming that:
            # lines[0] contains the value of chap
            # lines[1] contains the value of start_time + duration
            processed_chap = int(lines[0])  # Convert to int, assuming chap was an integer
            start_time = int(lines[1])  # Convert to int, assuming it was integer

            logger.info(
                f"Resuming metadata generation from chapter {processed_chap}/{len(chapter_titles)} with the start time {convert_milliseconds(start_time)}: {chapter_titles[processed_chap-1]}"
            )

    open_file_type = "w"
    if os.path.exists(sanitized_filename + "_FFMETADATAFILE"):
        open_file_type = "a"

    with open(sanitized_filename + "_FFMETADATAFILE", open_file_type) as file:
        file.write(";FFMETADATA1\n")
        file.write(f"ARTIST={author}\n")
        file.write(f"ALBUM={title}\n")
        file.write("DESCRIPTION=Made with https://github.com/emilisacson/epub_to_audiobook\n")
        for file_name in files:
            if chap <= processed_chap:
                chap += 1
                continue
            duration = get_duration(file_name)
            chapter_name = chapter_titles[chap-1]
            file.write("[CHAPTER]\n")
            file.write("TIMEBASE=1/1000\n")
            file.write(f"START={start_time}\n")
            file.write(f"END={start_time + duration}\n")
            file.write(f"title={chapter_name}\n")
            logger.info(
                f"Generated metadata for chapter {chap}/{len(chapter_titles)}: \"{chapter_name}\" with the start time {convert_milliseconds(start_time)} and duration {convert_milliseconds(duration)}"
            )
            # Create a txt file containing the latest chapter number that was processed in order to continue in case of an error
            # Add duration as well to calculate the start time for the next chapter
            with open(sanitized_filename + "_latest_metadata_chapter.ini", "w") as f:
                f.write(str(chap) + "\n" + str(start_time + duration))

            chap += 1
            start_time += duration
        
        logger.info(
            f"Metadata generation for {title} is complete"
        )
