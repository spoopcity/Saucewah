import json
import requests
import time
import io
import urllib
from PIL import Image as image
from selenium import webdriver
import random

import os

#driver = webdriver.Chrome("C:/Users/Some Idiot/source/repos/Saucewah/Saucewah/chromedriver.exe")  # Optional argument, if not specified will search path.
driver = webdriver.Chrome()  # Optional argument, if not specified will search path.

# Build bitmask
index_hmags='0'
index_reserved='0'
index_hcg='0'
index_ddbobjects='0'
index_ddbsamples='0'
index_pixiv='0'
index_pixivhistorical='0'
index_reserved='0'
index_seigaillust='0'
index_danbooru='0'
index_drawr='0'
index_nijie='0'
index_yandere='0'
index_animeop='0'
index_reserved='0'
index_shutterstock='0'
index_fakku='0'
index_hmisc='0'
index_2dmarket='0'
index_medibang='0'
index_anime='0'
index_hanime='0'
index_movies='0'
index_shows='0'
index_gelbooru='0'
index_konachan='0'
index_sankaku='0'
index_animepictures='0'
index_e621='1'
index_idolcomplex='0'
index_bcyillust='0'
index_bcycosplay='0'
index_portalgraphics='0'
index_da='1'
index_pawoo='0'
index_madokami='0'
index_mangadex='0'
#generate appropriate bitmask
db_bitmask = int(index_mangadex+index_madokami+index_pawoo+index_da+index_portalgraphics+index_bcycosplay+index_bcyillust+index_idolcomplex+index_e621+index_animepictures+index_sankaku+index_konachan+index_gelbooru+index_shows+index_movies+index_hanime+index_anime+index_medibang+index_2dmarket+index_hmisc+index_fakku+index_shutterstock+index_reserved+index_animeop+index_yandere+index_nijie+index_drawr+index_danbooru+index_seigaillust+index_anime+index_pixivhistorical+index_pixiv+index_ddbsamples+index_ddbobjects+index_hcg+index_hanime+index_hmags,2)


with open("Bot_token.txt") as file:
    botToken = file.read().strip()

with open("Sauce_token.txt") as file:
    sauceToken = file.read().strip()

class sauceWah:
    def __init__(self, botToken, sauceToken, chat_id, minsim='80!', sauceurl='', pipe_timeout=5, pipe_offset=-1, pipe_limit=1, curSearches=0, searchLimit_half=6, searchLimit_full=200):
        # Enable when we reach our hard limit
        self.stopSearch = False
        # Manage potential commands
        self.management = []
        # TG Endpoints
        self.url = "https://api.telegram.org/bot{}/".format(botToken)
        self.getFile = "https://api.telegram.org/bot{}/getfile?file_id=".format(botToken)
        self.dlFile = "https://api.telegram.org/file/bot{}/".format(botToken)
        # Saucenao Endpoint
        self.minsim = minsim
        self.sauceurl = 'http://saucenao.com/search.php?output_type=2&numres=1&minsim={}&dbmask={}&api_key={}'.format(minsim,db_bitmask,sauceToken)
        # Everything Else
        self.botToken = botToken
        self.sauceToken = sauceToken
        self.chat_id = chat_id
        self.pipe_timeout = pipe_timeout
        self.pipe_offset = pipe_offset
        self.pipe_limit = pipe_limit
        self.curSearches = curSearches
        self.searchLimit_half = searchLimit_half
        self.searchLimit_full = searchLimit_full
               

    ## TG Parsing and Handling Body ##
    def scan(self):
        chat = self.get_Updates_return_json()
        id_list = []

        # Check for command
        for message in chat:
            id_list.append(message["update_id"])
            if message["update_id"] not in self.management:
                print("Parsing message: '{}'".format(message["update_id"]))
                # Take message id and store it in a list
                self.management.append(message["update_id"])
                try:
                    key = list(message)[1]
                    message_chat_id = message[key]["chat"]["id"]

                except:
                    print("Fail with message: {}".format(message))

                else:
                    if self.chat_id == message_chat_id:
                        try:
                            if message["message"]["reply_to_message"]["photo"]:
                                print("possible photo")

                                rand = random.randint(0,20)
                                if rand == 20:
                                    self.send_plain_text(self.chat_id, "gay", message["message"]["message_id"])

                                else:
                                    # If we have our photo
                                    tgPhoto = message["message"]["reply_to_message"]["photo"][0]["file_id"]
                                    result = self.process_file(tgPhoto, message["message"]["message_id"])
                                    if result:
                                        print("Done posting.")
                                    else:
                                        print("This file could not be processed.")

                        except:
                            print("Either no photo was found or no reply_to_message and photo")                


    def process_file(self, fileObj, reply_id):
        url_string = self.getFile + "{}".format(fileObj)

        try:
            responce = self.request_url(url_string)
            json_responce_data = json.loads(responce.content)
            if "result" in json_responce_data:
                fPath = json_responce_data["result"]["file_path"]
                print(fPath)
                
        except:
            print("Could not process file. Filepath was not found.")

        else:
            try:
                url_string = self.dlFile + "/{}".format(fPath)
                responce = requests.get(url_string)

                with open('file.jpg', 'wb') as f:
                    data = f.write(responce.content)
                f.closed
                #tempim = open('file.jpg', 'wb').write(responce.content)

                extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
                thumbSize = (250,250)

                for root, _, files in os.walk(u'.',topdown=False):
                    for f in files:
                        fname = os.path.join(root, f)
                        for ext in extensions:
                            if fname.lower().endswith(ext):

                                # Now to send to saucenao
                                im = image.open(fname)
                                im.thumbnail(thumbSize)
                                imageData = io.BytesIO()
                                im.save(imageData,format='PNG')

                                files = {'file': ("file.png", imageData.getvalue())}
                                imageData.close()

                                try:
                                    r = requests.post(self.sauceurl, files=files)
                                    results = json.loads(r.content)# Use json lib return parsed responce
                                    print(results)
                                    if float(results['results'][0]['header']['similarity']) > float(results['header']['minimum_similarity']):

                                        #tgPhoto = message["message"]["reply_to_message"]["photo"][0]["file_id"]
                                        for result in results["results"]:
                                            for data in result["data"]["ext_urls"]:
                                                #print(data)
                                                self.send_plain_text(self.chat_id, data, reply_id)
                                    else:
                                        headerurl = "https://saucenao.com/{}".format(results['header']['query_image_display'])
                                        print(headerurl)
                                        driver.get('https://kheina.com/')
                                        time.sleep(1)
                                        url_box = driver.find_element_by_name('url')
                                        url_box.send_keys(headerurl)
                                        time.sleep(1)
                                        submit_box = driver.find_element_by_xpath('//*[@id="content"]/div[1]/form/input[3]')
                                        submit_box.click()
                                        time.sleep(5)
                                        result_box = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/a')
                                        result_rating = driver.find_element_by_id("percent").text

                                        if float(result_rating[:-1]) > 80.0:
                                            #print(result_box.get_attribute("href"))
                                            self.send_plain_text(self.chat_id, result_box.get_attribute("href"), reply_id)
                                        else:
                                            self.send_plain_text(self.chat_id, "Uhm, I couldnt find anything...", reply_id)


                                        #self.send_plain_text(self.chat_id, ("I did not find anything. However, it is possible that it may be found on https://kheina.com/ \nInput saucenao.com/{} in the URL field.").format(headerurl), reply_id)
                                        
                                except Exception as e:
                                    print(str(e))
                                    

                                return True

            except:
                    print("Failed to download processed file.")

        return False

    ## Helper Functs ##
    def send_plain_text(self, chat_id, plain_text, reply_id):
        notice_url = self.url + "sendMessage?chat_id={}&text={}&reply_to_message_id={}".format(chat_id, urllib.parse.quote_plus(plain_text), reply_id)
        #responce = requests.get(notice_url)
        self.request_url(notice_url)

    # Checks for required data needed for a function
    def required_data_check(self, message, *args):
        for arg in args:
            if isinstance(arg, list):
                _message = message
                try:
                    for key in arg:
                        _message = _message[key]
                except KeyError:
                    return False
            else:
                if arg not in message:
                    return False
        return True

    # Simply fetch the json update list
    # https://core.telegram.org/bots/api#getupdates
    def get_Updates_return_json(self):
        url_string = self.url + "getUpdates"
        if self.pipe_timeout != 0: # If pipe_timeout is not None or False, add it to the update url
            url_string += "?timeout={}".format(self.pipe_timeout)
            if self.pipe_offset != 0: # If pipe_offset is not None or False, add it to the update url
                url_string += "&offset={}".format(self.pipe_offset)
            if self.pipe_limit != 0: # If pipe_limit is not None or False, add it to the update url
                url_string += "&limit={}".format(self.pipe_limit)
        # https://api.telegram.org/bot#####/getUpdates?timeout=10&offset=-50&limit=50
        while True:
            responce = self.request_url(url_string)
            json_responce_data = json.loads(responce.content)# Use json lib return parsed responce
            if "result" in json_responce_data:
                return json_responce_data["result"]
            time.sleep(1)
    
    # Request to url, be it saucenao's endpoint or telegram
    def request_url(self, url):
        start_time = time.time()
        while True:
            try:
                responce = requests.get(url)
                responce.raise_for_status()
                if responce.json():
                    return responce
                else:
                    print("Request returned a responce that is not JSON.")
            except requests.exceptions.HTTPError as errHTTP:
                print ("Http Error:",errHTTP)
            except requests.exceptions.ConnectionError as errConnection:
                print ("Error Connecting:",errConnection)
            except requests.exceptions.Timeout as errTimeout:
                print ("Timeout Error:",errTimeout)
            except requests.exceptions.RequestException as err:
                print ("OOps: Something Else",err)
            print("Retrying in 10 seconds... (Exception for {} seconds)".format(int(time.time()) - int(start_time)))
            time.sleep(10)
            print("Retrying now")
            


# -1001065317964 echobase
# -1001439347866 fake
def main():
    runSauce = sauceWah(botToken, sauceToken, chat_id = -1001065317964)

    while True:
        runSauce.scan()
        time.sleep(1)

if __name__ == '__main__':
    main()