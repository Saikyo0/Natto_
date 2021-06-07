from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from pathlib import Path
import nhentai
import requests
import os
import certifi


KV="""
Screen:
    AsyncImage:
        id: thumbnail
        source:"null"
        pos_hint:{"center_x":0.5,"center_y":0.4}
        size_hint:(0.6,0.6)
        
    MDToolbar:
        id: toolbar
        title: "Natto"
        elevation: 10
        pos_hint: {'top': 1}

    MDTextField:
        id: sauce
        hint_text:"Sauce"
        color_mode: "accent"
        pos_hint:{"center_x":0.5,"center_y":0.85}
        size_hint_y: None
        size_hint_x: .6
        
    MDIconButton:
        icon: "magnify"
        pos_hint:{"center_x":.85,"center_y":0.8}
        on_press:
            thumbnail.source = app.image()
            description.text = app.text()
            download.text = "Download"
            app.download_finished = "None"
            app.search(sauce.text)
            
    MDLabel:
        id: description
        pos_hint:{"center_x":0.5,"center_y":0.7}
        size_hint_x:(0.6)
        bold: True
        theme_text_color:"Custom"
        text_color: [1,1,1,1]
        size_hint_y: None
        height: self.texture_size[1]
        
    MDRaisedButton:
        id: download
        text:"Download"
        pos_hint:{"center_x":0.5,"center_y":0.1}
        size_hint:(0.25,0.1)
        on_press:
            app.download()
        
"""


class Natto_App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.defs = None
        self.tags = None
        self.doujin_name = "null"
        self.main_path = '/storage/emulated/0/natto'
        self.download_path = '/storage/emulated/0/natto/downloaded'
        current = Path.cwd()
        try:
            os.mkdir(self.main_path)
            os.mkdir(self.download_path)
        except:
            print("making directory error")
        return Builder.load_string(KV)
    
    def text(self):
        try:
            tags=""
            self.doujin_name = str(self.defs['english']) + "\n" +\
                               "media id :"+self.media
            for x in self.tags:
                if x[1]=='tag':
                    tags=tags + x[2] + ","
                else:
                    pass
            self.doujin_name = self.doujin_name + "\n" +\
                               "Tags: "+ tags
            return self.doujin_name
        except:
            return "  " 
    def image(self):
        try:
            return self.image_source
        except:
            return "error"
    
    def search(self, sauce):
        print(sauce)
        try:
            doujin = nhentai.get_doujin(int(sauce))
            self.image_source = doujin.cover
            self.defs = doujin.titles
            self.tags = doujin.tags
            self.media = doujin.media_id
            self.images = doujin.pages
        except:
            print("internet connection isnt acquired")
            
        cafile = certifi.where()
        with open(cafile, 'r') as infile:
            customca = infile.read()
            print(cafile)
        pass

    def download(self):
        self.loading=MDDialog(title="Download",text="Downloading",size_hint=(0.4,0.4))
        self.loading.open()
        Clock.schedule_once(self.main_download,0.1)
        
    def main_download(self,dt):
        path="/storage/emulated/0/natto/downloaded/doujins/"
        name = str(self.defs['english'])
        name=name.split(" ")
        name=name[1]
        print(path+name)
        try:
            os.makedirs(path+name)
        except:
            print("either file exist or makedir error")
            pass
        z=-1
        try:
            for x in self.images:
                z += 1
                print("downloading")
                image = requests.get(x[0])
                file = open(path+name+"/"+str(z)+".jpg","wb")
                file.write(image.content)
                print("downloaded")
                file.close()
            Clock.schedule_once(self.finished,0.1)
        except:
            print("download error")
        pass
    def finished(self, dt):
        self.loading.dismiss()
        self.ending = MDDialog(title="Download",text="Download finished",size_hint=(0.4,0.4))
        self.ending.open()
        pass
        
Natto_App().run()
