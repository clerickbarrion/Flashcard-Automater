import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import json

class Anki:
    def __init__(self,word,deck_name):
        self.word = word
        self.deck_name = deck_name
        self.html = self.get_html()
       
    def get_html(self):
        html = requests.get(f'https://www.linguee.com/english-portuguese/search?source=auto&query={self.word}')
        return BeautifulSoup(html.text, 'html.parser')
    
    def get_translation(self):
        translation = self.html.find('a', class_='dictLink')
        return translation.text
    
    def get_sentence(self):
        sentence = self.html.find('div', class_='example_lines').find('span', class_='tag_s')
        return sentence.text

    def get_sentence_translation(self):
        translation = self.html.find('span', class_='tag_e').find('span', class_='tag_t')
        return translation.text
    
    def get_audio(self):
        audio = gTTS(text=self.word,lang='pt')
        audio.save(f'C:/Users/{username}/AppData/Roaming/Anki2/User 1/collection.media/{self.word}.mp3')
        audio = gTTS(text=self.get_sentence(),lang='pt')
        audio.save(f'C:/Users/{username}/AppData/Roaming/Anki2/User 1/collection.media/{self.get_sentence()}.mp3')

    def upload(self, model_name):
        localhost = 'http://localhost:8765'
        load = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": self.deck_name,
                    "modelName": model_name,
                    "fields": {
                        "Word": self.word,
                        "Translation": self.get_translation(),
                        "Sentence": self.get_sentence(),
                        "Sentence Translation": self.get_sentence_translation(),
                        "Word Audio": f'[sound:{self.word}.mp3]',
                        "Sentence Audio": f'[sound:{self.get_sentence()}.mp3]',
                    },
                    "options": {
                        "allowDuplicates": False
                    },
                    "tags": []
                }
            }
        }
        requests.post(localhost,json.dumps(load))

username = 'thede'
# add all translation lines
list = ['dela','só','entre','poder','qualquer','desistir','local','seco','ideal','estoque','provar','prato','chamar','regras','solução','exército','lutar']
#local 2 poder 2 provar-try/taste 
for i in list:
    try:
        card = Anki(i,'Portuguese Vocab')
        card.get_audio()
        card.upload('Tagalog English')
        card.upload('English Tagalog')
        print(f'{i} added')
    except:
        print(f'error with adding {i}')