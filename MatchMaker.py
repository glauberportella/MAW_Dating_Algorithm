# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 07:38:44 2018

@author: hoped
"""
from Person import *
import random

NUM_MATCHES = 4
### create a function- to read in from response.txt and create a list of instances of person
def read_that_text_file():
    f = open("response.txt", "r")
    # Make an array for each line
    lines = [line for line in f]
    people = []

    for i in lines:
      person = i.replace("\t", ",")
      person = person.split(",")
      people.append(Person(person[0], person[1], person[2], person[3:]))
      
    # lines = [x.strip() for x in lines.split(',')]
    # Deliminate that array into seperate items
    # for i in lines:
    #   lines[i].replace("\t", ","
    f.close()

    return people

    # first_three_words = text_file.read().split(' ')
    # attributes = text_file.read().split(',')
### create a function- take the ward members and make match frequency dictionary
### for each member of the opposite sex
def make_frequencies(people):
    for p1 in people:
        for p2 in people:
            if p1.gender != p2.gender and p2.name not in p1.in_freq_dic:
                common = []
                for interest in p1.interests:
                    if interest in p2.interests:
                        common.append(interest)
                p1.add_freq(p2.name, common)
                p2.add_freq(p1.name, common)
                
### function to make all the "natural" matches in the form of a list of tuples (matched_person, [list of common interests])
def make_matches(people):
    for p in people:
        for i in range(len(p.interests), -1, -1):
            if len(p.freq_dic[i]) <= NUM_MATCHES-len(p.matches):
                for z in p.freq_dic[i]:
                    p.matches.append(z)
            else:
                break
### function to make "tiebreaker" matches
def tiebreaker(people):
    dic = {}
    for p in people:
        dic[p.name]= p
    
    for p in people:
        for match in p.matches:
            dic[match[0]].add_other(p.name)
    
    for p in people:
        needed = (NUM_MATCHES-len(p.matches))
        for k in range(needed):
            level = len(p.interests)+1
            end = False
            while not end and level > 0:
                level -= 1
                for person in p.freq_dic[level]:
                    if person not in p.matches:
                        end = True
                        break
            lowest = None
            for potential in p.freq_dic[level]:
                name = potential[0]
                if potential not in p.matches:
                    lowest = len(dic[name].other_matches) if lowest == None or len(dic[name].other_matches) < lowest else lowest
            contenders = []
            for potential in p.freq_dic[level]:
                name = potential[0]
                if len(dic[name].other_matches) == lowest:
                    contenders.append(potential)
            winner = random.randint(0,len(contenders)-1)
            p.matches.append(contenders[winner])
            name = contenders[winner][0]
            dic[name].other_matches.append(p.name)

### function to write the results for each individual to a text file containing
### 1- their email address
### 2- Name - listed interests
### 3- Matches and interests that they share in common


### main method calls all these functions in sequence
if __name__ == "__main__":
    people = read_that_text_file()
    make_frequencies(people)
    make_matches(people)
    tiebreaker(people)
    for p in people:
        print(p)