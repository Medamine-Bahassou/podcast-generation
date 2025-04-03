import base64
import os
from google import genai
from google.genai import types # type: ignore
import uuid
from pydub import AudioSegment

import tts_script 


global man_name 
global woman_name 

man_name = "Mark"
woman_name = "Laila"

history = []

def gemini(message):
    client = genai.Client(
        api_key="AIzaSyCeDXNfPaBYjxfUB1FGM-2j4k0qMO_5LAw",
    )

    model = "gemini-2.5-pro-exp-03-25"

    contents = []

    # print(history)

    if len(history) != 0 :
        for i in range(len(history)):
            contents.append(
                types.Content(
                    role=f"user",
                    parts=[
                        types.Part.from_text(text=f"""{history[i][0]}"""),
                    ],
                ),
            )
            contents.append(
                types.Content(
                    role=f"model",
                    parts=[
                        types.Part.from_text(text=f"""{history[i][1]}"""),
                    ],
                ),
            )



    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""{message}"""),
            ],
        ),
    )




    tools = [
        types.Tool(google_search=types.GoogleSearch())
    ]
    generate_content_config = types.GenerateContentConfig(
        # tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text=f"""
**Role:** Podcast Script Generator
**Personas:**
*   {man_name}
*   {woman_name}
**Topic:** [**Insert Podcast Topic Here**]

**Task:**
Write the dialogue for a podcast segment featuring {man_name} and {woman_name} discussing the specified topic.
1.  Start the script *immediately* with either {man_name} or {woman_name} speaking. No intros or scene-setting.
2.  Format the output *exactly* like this, with "<<<>>>" on its own line separating each speaker's dialogue:

    {man_name}: [{man_name}'s dialogue]
    <<<>>>
    {woman_name}: [{woman_name}'s dialogue]
    <<<>>>
    {man_name}: [{man_name}'s next line]
    <<<>>>
    {woman_name}: [{woman_name}'s next line]
    <<<>>>
    ...(continue pattern)

**Begin Script Now:**
            """),
        ],
    )

    res = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if hasattr(chunk, "text"):  # Ensure the chunk has text attribute
            res += chunk.text
    

    # History appending 
    history.append([message, res])

    return res 


if __name__ == "__main__":

    man_name = input("man name : ")
    woman_name = input("woman name : ")
    
    
    prompt = input("/PROMPT > ")
    res = gemini(prompt)
    print(res)

    dialog = res.split("<<<>>>")

    audio_files = []

    for i in range(len(dialog)): 
        if dialog[i].find(f"{man_name}:") != -1: 
            r = dialog[i].replace(f"{man_name}:","")
            tts_script.tts(r,f"sounds/{i}.mp3")
        else : 
            r = dialog[i].replace(f"{woman_name}:","")
            tts_script.tts_woman(r,f"sounds/{i}.mp3")
        audio_files.append(f"sounds/{i}.mp3")
            
    

    if not audio_files:
        print("No audio files found to merge.")
    else:
        # Load the first audio file
        combined = AudioSegment.from_file(audio_files[0])
        print(f"Loading and starting with: {audio_files[0]}")

        # Loop through the remaining audio files and append them
        for audio_file in audio_files[1:]:
            try:
                next_segment = AudioSegment.from_file(audio_file)
                combined += next_segment # Concatenate (append) the next segment
                print(f"Adding: {audio_file}")
            except Exception as e:
                print(f"Error processing file {audio_file}: {e}")
                # Decide if you want to skip the file or stop the process
                # continue # Uncomment to skip the problematic file

        # Specify the output file path and format
        output_path = "podcast.mp3"
        output_format = "mp3" # Can be 'wav', 'ogg', etc.

        # Export the combined audio
        try:
            print(f"Exporting combined audio to {output_path} in {output_format} format...")
            combined.export(output_path, format=output_format)
            print("Audio merging complete!")
        except Exception as e:
            print(f"Error exporting combined audio: {e}")

