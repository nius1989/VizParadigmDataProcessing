from watson_developer_cloud import SpeechToTextV1
import os
import json
import datetime

speech_to_text = SpeechToTextV1(
    iam_apikey='0cnA-IKYNmFwNGd9ctzfxhKgnXjEq4kh95-ER_Zw7sQ5',
    url='https://gateway-wdc.watsonplatform.net/speech-to-text/api',
)


def process_file(path):
    audio_file = open(path, "rb")
    save_file = os.path.splitext(path)[0]
    print(path)
    result = speech_to_text.recognize(audio=audio_file, content_type="audio/mpeg",
                                      continuous=True, timestamps=True,
                                      max_alternatives=1)
    with open(save_file + ".srt", 'w') as fp:
        transcript = json.loads(str(result))
        counter = 1
        for trans in transcript["result"]["results"]:
            for sen in trans["alternatives"]:
                timestamps = sen["timestamps"]
                fp.write(str(counter) + "\n")
                fp.write(str(datetime.timedelta(seconds=timestamps[0][1])) + " --> " + str(
                    datetime.timedelta(seconds=timestamps[-1][2])) + "\n")
                fp.write(sen["transcript"] + "\n")
                fp.write("\n")
                counter += 1
    with open(save_file + ".json", 'w') as fp:
        transcript = json.loads(str(result))
        fp.write(json.dumps(transcript, sort_keys=True, indent=2))


# paths = ["G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\101\\00029.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\101\\00030.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\102\\00033.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\102\\00034.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\103\\00038.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\103\\00039.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\104\\00046.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\105\\00053.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\109\\00064.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\109\\00065.mp3"
#          ]

# paths = ["G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\202\\00031.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\202\\00032.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\203\\00040.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\203\\00041.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\205\\00049.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\205\\00050.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\206\\00054.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\206\\00055.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\207\\00056.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\207\\00057.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\209\\00062.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\209\\00063.mp3"
#          ]

# paths = ["G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\301\\00027.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\301\\00028.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\302\\00036.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\302\\00037.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\303\\00042.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\303\\00043.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\304\\00044.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\304\\00045.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\305\\00051.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\305\\00052.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\309\\00060.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\309\\00061.mp3"
#          ]

# paths = ["G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\110\\00067.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\111\\00070.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\111\\00071.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\210\\00066.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\211\\00072.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\211\\00073.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\310\\00068.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\310\\00069.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\311\\00074.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\311\\00075.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\312\\00076.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\312\\00077.mp3"
#          ]

# paths = ["G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\112\\00081.mp3",
#          "G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\112\\00082.mp3",
#          ]

paths = ["G:\\My Drive\\Technology on the Trail - Fall 2018\\DATA2\\104\\104_2.mp3",
         ]

for p in paths:
    process_file(p)
