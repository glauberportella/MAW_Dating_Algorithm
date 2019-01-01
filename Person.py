# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 07:38:11 2018

@author: hoped
"""

MAX_NUM_INTERESTS = 6
class Person():
    def __init__(self, name, email, gender, interests):
        self.name = name
        self.email = email
        self.gender = gender == "Female" # Female == True, Male == False
        self.other_matches = [] #list of names of people where this person ended up on someone else's list
        self.in_freq_dic = set()
        self.freq_dic = {}
        self.matches = []
        self.num_random_matches = 0
        self.interests = interests[0].split(", ") #note in the interest survey there should be no options that contain this character combo!!!
        #if people selected too many interests it messes up the algorithm
        if len(self.interests) >= MAX_NUM_INTERESTS:
            self.interests = self.interests[0:MAX_NUM_INTERESTS] 
        for i in range(len(self.interests)+1):
            self.freq_dic[i] = []
            
    def add_freq(self, name, common_interests):
        x = len(common_interests)
        self.freq_dic[x].append((name, common_interests))
        self.in_freq_dic.add(name)
    
    def add_match(self, match):
        self.matches.append(match)
    
    def get_matches(self):
        return self.matches
    
    def add_other(self, name):
        self.other_matches.append(name)
        
    def __str__(self):
        result = "Happy New Year " + self.name + "!\n\n"
        result += "Here are the interests you listed: " 
        for i in self.interests:
            result += i + ", "
        result = result[:-2] + "\n\n"
        result += "And here are the results from the algorithm! (Rank, Name, Common Interests):\n"
        for i in range(len(self.matches)):
            result += str(i+1)+". " + self.matches[i][0] + " - "
            for interest in self.matches[i][1]:
                result += interest + ", " 
            result = result[:-2] + "\n"
        result += "\nA few things to note about the algorithm:\n"
        result += "- The purpose of this algorithm is to simply help people in the ward initiate interaction with other people they don't know as well. My hypothesis is that starting out with knowing some "
        result += "common interests can cut out some of the small talk and help people plan a date or have a meaningful conversation at church.\n"
        result += "- How the algorithm works:\n"
        result += "Each person was assigned 5 matches based on how many common interests they shared with the respondents of the opposite gender. If you listed more than 6 interests, the extras were removed because this interfered with matching.\n"
        result += "A very common scenario that occurred was someone would match 5 interests with one person, 4 interests with another and 3 interests "
        result += "with 10 people. Thus in order for everyone to get only five matches, a tie-breaking method was developed to fill the remaining three "
        result += "slots randomly in such a way that everyone ended up on more or less the same number of lists in the end. \n\n"
        result += "!!! Because of this and other factors, it is unlikely that all the people on your list have you on theirs !!! \n "
        result += "Use this fact to your advantage! Be brave! Talk to the other person first.\n\n"
        result += "-Disclaimer: This is not a perfect algorithm. Your list is not exhaustive and does not include all of your potential matches because I didn't want to overwhelm people. Aka if you "
        result += "want to talk to someone and they aren't on your list, it could mean they didn't participate or that they weren't randomly selected during tie breakers or that this algorithm sucks- talk to them anyway. I would love to hear feedback for how it goes and if this helps (or hurts) at all. I'll be sending out a survey to "
        result += "gauge how effective it was in a couple of months and to see if there is an interest in a version 2.0 next year. If not, hey it was worth a shot and it was a fun side project.\n\n"
        result += "If you have any questions, please feel free to respond to this email or talk to me [I'll be back in Boston in February]. \nThe source code for those interested can be found here: "
        result += "https://github.com/h0p3d/MAW_Dating_Algorithm\n\nThanks for your participation,\n MAW Dating Algorithm 1.0"
        return result