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
        self.other_matches = [] #list of names of people where this person ended up on someone else's list
        self.freq_dic = {}
        self.matches = []
        
        for i in range(len(interests)+1):
            self.freq_dic[i] = []
            
    def add_freq(self, name, common_interests):
        x = len(common_interests)
        self.freq_dic[x].append(name, common_interests)
    
    def add_match(self, match):
        self.matches.append(match)
    
    def get_matches(self):
        return self.matches
    
    def add_other(self, name):
        self.other_matches.append(name)
        
    def __str__(self):
        gender = "Female" if self.gender else "Male"
        result = self.name + "  " + self.email + "  " + gender + "\n"
        result += "Interests : " 
        for i in self.interests:
            result += i + ", "
        result = result[:-2] + "\n Number of matches: " + len(self.matches) + "\n"
        for i in range(len(self.matches)):
            result += str(i+1)+". " + self.matches[i][0] + str(self.matches[i][1]) + "\n"
        result += "Other Matches : " + str(len(self.other_matches)) + "  " + str(self.other_matches) + "\n"
        