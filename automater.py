import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import json

class Anki:
    def __init__(self,word,index,deckName):
        self.word = word
        self.index = index
        self.deckName = deckName
        self.sentence, self.translation = self.getSentenceTranslation()
        self.HTML = self.getHTML()

    def getHTML(self):
        HTML = requests.get(f'https://jisho.org/search/{self.word}')
        return BeautifulSoup(HTML.text, 'html.parser')
    
    def getMeaning(self):
        meaning = self.HTML.find('span', class_='meaning-meaning')
        return meaning.text
    
    def getFurigana(self):
        furigana = self.HTML.find('span', class_='furigana')
        return furigana.text.strip()
    
    def getSentenceTranslation(self):
        sentence = ''
        HTML = BeautifulSoup(requests.get(f'https://jisho.org/search/{self.word}%20%23sentences').text, 'html.parser')
        translation = HTML.find('span', class_='english').text

        sentenceContainer = HTML.find('ul', class_='japanese_sentence japanese japanese_gothic clearfix')
    
        furiTags = sentenceContainer.findAll('span', class_='furigana')
        for i in furiTags:
            i.decompose()

        sentence = sentenceContainer.text

        # sentenceContainer = sentenceContainer.find_all('span', class_='unlinked')
        # for i in sentenceContainer:
        #     sentence += i.text
        return sentence, translation
    
    def getAudio(self):
        audio = gTTS(text=self.word,lang='ja')
        audio.save(f'/Users/{username}/Library/Application Support/Anki2/User 1/collection.media/{self.word}.mp3')
        audio = gTTS(text=self.sentence,lang='ja')
        audio.save(f'/Users/{username}/Library/Application Support/Anki2/User 1/collection.media/{self.sentence}.mp3')

    def upload(self):
        localhost = 'http://localhost:8765'
        load = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": self.deckName,
                    "modelName": "Japanese Vocabulary",
                    "fields": {
                        "Index": self.index,
                        "Word": self.word,
                        "Transliteration": self.getFurigana(),
                        "Meaning": self.getMeaning(),
                        "Example Sentence": self.sentence,
                        "Sentence Translation": self.translation,
                        "Word Audio": f'[sound:{self.word}.mp3]',
                        "Sentence Audio": f'[sound:{self.sentence}.mp3]',
                    },
                    "options": {
                        "allowDuplicates": False
                    },
                    "tags": []
                }
            }
        }
        requests.post(localhost,json.dumps(load))

# card = Anki('車',0,'Jap')
# sentence, translation = card.getSentenceTranslation()
# print(sentence)
# print(translation)

username = 'clerickbarrion'
list = ['刑務所', '自動車', '車', '運動', '飛行機']
index = 0
for i in list:
    try:
        card = Anki(i,str(index),'Jap')
        card.getAudio()
        card.upload()
        index += 1
        print(f'{i} added')
    except:
        print(f'error with adding {i}')