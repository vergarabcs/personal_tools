import os
import srt
import datetime
import csv
import shutil

class Config:
    AnkiCollectionPath = '/Users/billcarlo.vergara/Library/Application Support/Anki2/Bill/collection.media'
    AnimeNoVid = ['ID', 'Japanese', 'Reading', 'Context', 'English', 'Explanation', 'Screenshot', 'Audio_Sentence', 'Audio_English', 'Video', 'Tags']
    EPISODE_NAME = "Frieren_02"
    FRAME_HEIGHT = "240"
    INPUT_VIDEO = "./input/mySub2srs/frieren_02.mkv"
    INPUT_SRT_EN = './input/mySub2srs/frieren_02_en.srt'
    INPUT_SRT_JAP = './input/mySub2srs/frieren_02.srt'
    MEDIA_FOLDER = "./input/mySub2srs/media"
    OFFSET = -1
    OUTPUT_TSV = "./input/mySub2srs/output.tsv"
    PADDING = 0.250

class SubLine:
    def __init__(self, start, end, text, index):
        self.start = start
        self.end = end
        self.text = text
        self.index = index

    def parse(line: str):
        [index, timing, *texts] = line.split('\n')
        text = ' '.join(texts)
        print(index)
        print(timing)
        print(text)

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        pass


def extractAudio(filename, start, end):
    start = start + Config.OFFSET - Config.PADDING
    end = end + Config.OFFSET + Config.PADDING
    duration = end - start
    file_path = f'{Config.MEDIA_FOLDER}/{filename}'
    silentremove(file_path)

    command = f'''ffmpeg -ss {start} -t {duration} -i {Config.INPUT_VIDEO} -filter_complex "[0:a:1]channelsplit=channel_layout=stereo:channels=FR[right]" -map "[right]" {file_path}'''
    os.system(command)
    # os.system(f"afplay {file_path}")

def extractImage(filename, time):
    fullPath = f"{Config.MEDIA_FOLDER}/{filename}"
    withOffset = time + Config.OFFSET
    command = f'''ffmpeg -ss {withOffset} -i {Config.INPUT_VIDEO} -frames:v 1 -q:v 2 -vf "scale=-1:{Config.FRAME_HEIGHT}" {fullPath}'''
    os.system(command)

unique_id = datetime.datetime.now().isoformat()
def getNoteId(index):
    return f"{Config.EPISODE_NAME}_{str(index).zfill(4)}"

def moveFilesToAnki(image, audio):
    shutil.move(
        f"{Config.MEDIA_FOLDER}/{image}",
        f"{Config.AnkiCollectionPath}/{image}"
    )
    shutil.move(
        f"{Config.MEDIA_FOLDER}/{audio}",
        f"{Config.AnkiCollectionPath}/{audio}"
    )
    
def main():
    with open(Config.INPUT_SRT_JAP, "r") as file_jap, open(Config.INPUT_SRT_EN, 'r') as file_en, open(Config.OUTPUT_TSV, "w") as fileTsv:
        writer = csv.writer(fileTsv, delimiter='\t', lineterminator='\n')
        subs_jap = list(srt.parse(file_jap.read()))
        subs_en = list(srt.parse(file_en.read()))
        context = ''
        for i in range(0, len(subs_jap)):
            sub_jap = subs_jap[i]
            sub_en = subs_en[i]
            if(sub_jap.index != sub_en.index):
                raise Exception('Line Mismatch', sub_jap, sub_en)
            noteId = getNoteId(sub_jap.index)
            audioFileName = f"{noteId}.mp3"
            imageFileName = f"{noteId}.jpg"
            print(audioFileName, imageFileName)
            extractAudio(
                audioFileName, 
                sub_jap.start.total_seconds(), 
                sub_jap.end.total_seconds()
            )            
            extractImage(imageFileName, sub_jap.start.total_seconds())

            writer.writerow([
                noteId,
                sub_jap.content,
                '',
                f"Context: {context}",
                sub_en.content,
                '',
                f'<img src="{imageFileName}">',
                f'[sound:{audioFileName}]',
                '',
                '',
                ''
            ])
            moveFilesToAnki(imageFileName, audioFileName)
            context = sub_en.content

main()