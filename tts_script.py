import asyncio
import edge_tts  # Ensure this module is installed and not shadowed by your script name

async def text_to_speech(text, filename="output.mp3", voice="en-US-BrianNeural"):
    tts = edge_tts.Communicate(text, voice)
    await tts.save(filename)
    print(f"Saved as {filename}")






def tts_woman(text, dir):
    asyncio.run(text_to_speech(text, dir,"en-US-EmmaNeural"))


def tts(text, dir="male_voice.mp3"): 
    asyncio.run(text_to_speech(text, dir))
    

if __name__ == "__main__":
    text = f"""
Alright, you want a fucking true story? Here's one that'll blow your mind.

Picture this: Christmas Eve, 1971. A 17-year-old girl, Juliane Koepcke, is on a plane over the goddamn Amazon jungle. Shit hits the fan, lightning blasts the plane, and it rips apart mid-air. She falls. Not like, tripping over your feet falls. She falls *two fucking miles*, strapped into her airplane seat, down into the thickest jungle on Earth.

And the insane part? She lives. Wakes up alone, busted collarbone, gashed up, concussed, one eye swollen shut, probably thinking "what the actual fuck just happened?" She's the *only* one out of 92 people who survived the initial crash. But surviving the fall was just the start. Now she's gotta survive the jungle.

For 11 days, this badass teenager walks through hell. Got nothing to eat but some candy she found. Bugs are eating her alive – literally, she gets maggots festering in a wound on her arm. But she remembers survival shit her zoologist parents taught her, finds a creek, and follows the water downstream. Knows it's her only shot. Finally, half-dead, she stumbles into a logging camp. Can you imagine the look on those loggers' faces? This girl literally fell from the sky and walked out of the jungle. Fucking legend. She didn't just survive; she went on to become a biologist, like her folks. How's that for a true fucking story?
    """
    asyncio.run(text_to_speech(text, "male_voice.mp3"))

    
