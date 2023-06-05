import requests
import numpy as np
from base64 import b64encode


def generate_android_audio_file():
    instructions = np.unique([
        "PUSH YOUR BODY WEIGHT FORWARD",
        "BRING YOUR LEFT FOOT TO THE SIDE",
        "BRING YOUR RIGHT FOOT TO THE SIDE",
        "RAISE BOTH LEGS AND HOLD"
    ])

    # instructions = [" ".join(x.split("_")) for x in instructions]

    AUTHORIZATION = f"vauser:YWlhaYTRcGl1SuNaN2VyOiQkTUYTERMDIw".encode()

    for x in instructions:
        filename = "_".join([i.lower() for i in x.split(" ")]) + ".wav"

        response = requests.post(
            url="https://devvaapi.injurycloud.com/api/voice/generate",
            json={
                "Tenant": "dev",
                "VoiceText": x
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Basic {str(b64encode(AUTHORIZATION))[2:-1]}",
            }
        )
        data = response.json()
        resp = requests.get(data["Message"]["AudioUrl"])
        with open("audio_cues/" + filename, "wb") as file:
            file.write(resp.content)

    for x in instructions:
        name = "_".join(x.split())
        print(f"const val {name} = \"{' '.join([i.lower() for i in x.split()])}\"")

    print()

    # for x in instructions:
    #     x = x.split(" ")
    #     name = x[0].lower() + "".join([i.title() for i in x[1:]])
    #     print(f"private val {name} = MediaPlayer.create(context, R.raw.{'_'.join([i.lower() for i in x])})")
    #
    # print()

    for x in instructions:
        print(x.replace(' ', "_") + " -> Instruction(text = text, player = MediaPlayer.create(context, R.raw." + x.lower().replace(' ', "_")+"))")


generate_android_audio_file()
