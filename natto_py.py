from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.clock import Clock
from pathlib import Path
import nhentai
import requests
import os
import certifi
import sys

KV="""
Screen:
    MDToolbar:
        id: toolbar
        title: "Natto"
        elevation: 10
        pos_hint: {'top': 1}

    MDTextField:
        id: sauce
        hint_text:"Sauce"
        pos_hint:{"center_x":0.25,"center_y":0.8}
        size_hint_y: None
        size_hint_x: .3
        
    MDIconButton:
        icon: "magnify"
        pos_hint:{"center_x":.35,"center_y":0.8}
        on_press:
            thumbnail.source = app.image()
            description.text = app.text()
            download.text = "Download"
            app.download_finished = "None"
            app.search(sauce.text)
        
    MDLabel:
        id: description
        pos_hint:{"center_x":0.3,"center_y":0.45}
        size_hint:(0.4,0.4)
        font_style:"Button"
        
        
    MDRaisedButton:
        id: download
        text:"Download"
        pos_hint:{"center_x":0.3,"center_y":0.1}
        size_hint:(0.25,0.1)
        on_press:
            app.download()
        
    AsyncImage:
        id: thumbnail
        pos_hint:{"center_x":0.7,"center_y":0.5}
        size_hint:(0.4,0.6)
        
"""
class Natto_App(MDApp):
    def build(self):
        self.defs = None
        self.tags = None
        self.doujin_name = "null"
        self.download_path = "./downloaded"
        current = Path.cwd()
        try:
            os.chdir(self.download_path)
        except:
            os.mkdir(self.download_path)
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
            pass
    
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
            cafile = certifi.where()
            with open('certificate.pem','rb') as infile:
                customca = infile.read()
            with open(cafile,'rb') as outfile:
                outfile.write()
        pass

    def download(self):
        self.loading=MDDialog(title="Download",text="Downloading",size_hint=(0.4,0.4))
        self.loading.open()
        Clock.schedule_once(self.main_download,0.1)
        
    def main_download(self,dt):
        try:
            path="./doujins/"+str(self.doujin_name)
            try:
            	os.makedirs(path)
            except:
            	pass
            print("cc")
            z=-1
            for x in self.images:
                z += 1
                print("downloading")
                image = requests.get(x[0])
                file = open(path+"/"+str(z),"wb")
                file.write(image.content)
                file.close()
            time=0.01*float(z)
            if time>0:
               Clock.schedule_once(self.finished,time)
            
        except:
            pass
        
        pass
    def finished(self, dt):
        self.loading.dismiss()
        self.ending = MDDialog(title="Download",text="Downloading",size_hint=(0.4,0.4))
        self.ending.open()
        pass
        
Natto_App().run()
