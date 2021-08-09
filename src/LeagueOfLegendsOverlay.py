from tkinter import *
from HTTPRequests import *
from functools import partial
import os

dirname = os.path.dirname(__file__)

current_champion_index = 0
new_champion_index = 0

class Overlay(Frame):

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.initial_frame = Frame(parent)
        self.initial_frame.pack()
        self.champion_portrait_frame = Frame(parent)
        self.champion_portrait_frame.pack()
        self.champion_ability_icon_frame = Frame(parent)
        self.champion_ability_icon_frame.pack()
        self.champion_ability_frame = Frame(parent)
        self.champion_ability_frame.pack()

        self.champion_images = [] 
        self.champion_ability_images = []

        self.champions = []
        self.champion_abilities = {}

        self.summoner_name = StringVar()
        self.create_initial_frame()

    def create_initial_frame(self):
        Label(
            self.initial_frame,
            text = "Summoner Name",
            font = ('calibre', 14, 'bold')
        ).pack(side = LEFT)
        Entry(
            self.initial_frame,
            textvariable = self.summoner_name,
            font = ('calibre', 14)
        ).pack(side = LEFT)
        Button(
            self.initial_frame,
            text = "Find current game",
            font = ('calibre', 14),
            command = lambda: self.create_champion_overlay()
        ).pack(side = LEFT)

    def create_champion_overlay(self):
        self.champions = get_current_game_champions(get_encrypted_summoner_id_by_name(self.summoner_name.get()))
        for champion in self.champions:
            abilities = get_champion_abilities(champion)
            self.champion_abilities[champion] = abilities

        self.create_champion_buttons(self.champions)
    
    def create_champion_ability_tooltip(self, ability):
        for child in list(self.champion_ability_frame.children.values()):
            child.destroy()

        Label(
            self.champion_ability_frame,
            text = "{}".format(ability['description']),
            wraplength = self.parent.winfo_width()
        ).pack(side = BOTTOM)
        
    def create_champion_abilities(self, champion):
        #destroy the old ability icons
        for child in list(self.champion_ability_icon_frame.children.values()):
            child.destroy()
        
        abilities = self.champion_abilities[champion]
        for ability in abilities:
            filename = os.path.join(dirname, '..\\resources\\ability\\{}').format(ability['image']['full'])
            img = PhotoImage(file = filename)
            self.champion_ability_images.append(img)
            Button(
                self.champion_ability_icon_frame,
                image = img,
                command = partial(self.create_champion_ability_tooltip, ability)
            ).pack(side = LEFT, fill = BOTH, expand = True)
        

    def create_champion_buttons(self, champions):
        for champion in champions:
            #TODO change the way images are gotten
            filename = os.path.join(dirname, '..\\resources\\champion\\{}.png').format(champion)
            img = PhotoImage(file = filename)
            img = img.subsample(2)
            self.champion_images.append(img)
            Button(
                self.champion_portrait_frame,
                image = img,
                command = partial(self.create_champion_abilities, champion)
            ).pack(side = LEFT)
            

root = Tk()
overlay = Overlay(root)

root.attributes('-topmost', True)

root.mainloop()