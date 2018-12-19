# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 07:38:11 2018

@author: hoped
"""

class Person():
    def __init__(self, name, email, gender, interests):
        self.name = name
        self.email = email
        self.gender = gender == "Female" # Female == True, Male == False
        self.interests = interests
        
        self.freq_dic = {}
        self.matches = []
        
        for i in range(len(interests)+1):
            self.freq_dic[i] = []
    