# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 07:38:44 2018
Main match making algorithm, aka where the magic happens
@author: hoped
"""
from Person import *
import EmailAutomation
import random

NUM_MATCHES = 5
def read_that_text_file():
    '''
    @author: byoung
    read in survey results from response.txt (must be in same folder as this file)
    return: list of instances of Person created from survey data
    '''
    f = open("result1.txt", "r")
    # Make an array for each line
    lines = [line for line in f]
    f.close()
    people = []
    for i in lines:
      i = i.replace("\n", "")
      person = i.split("\t")
      people.append(Person(person[0], person[1], person[2], person[3:])) #make people
    return people

def make_frequencies(people):
    """
    input: people - a list of persons
    generates a frequency dictionary for each person's common interests with 
    members of the opposite sex to make matching easier
    """
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
    """
    input: people - a list of persons
    make all natural matches, that is for each person match them with the person that
    has the highest number of common interests as long as their are less than NUM_MATCHES total
    matches
    if we reach a level with more candidates than matches left to make, stop. The tiebreaker method
    will take care of those cases
    """
    matches_made = 0
    for p in people:
        for i in range(len(p.interests), -1, -1):
            if len(p.freq_dic[i]) <= NUM_MATCHES-len(p.matches):
                for z in p.freq_dic[i]:
                    p.matches.append(z)
                    matches_made += 1
            else:
                break
    return matches_made
def tiebreaker(people):
    """
    input: people - a list of persons
    After all natural matches have been made, it is quite possible that more matches need to be made.
    Say the NUM_MATCHES is 5, you match 5 interests with one person, 4 interests with 
    another and 3 interests with 10 people. This method "breaks the tie" between
    the 10 people to fill the remaining slots.
    
    1) Identify the "level" (the number of common interests we are looking at)
    2) Take the people that have the least number of matches with other people and
    then randomly select between them.
    
    This ensures fairness (an even distribution of people across lists is ideal)
    and still randomly breaks the tie. 
    """
    dic = {}
    #create a quick lookup system to match names with person objects
    for p in people:
        p.num_random_matches = NUM_MATCHES-len(p.matches)
        dic[p.name]= p
    
    #for each person, keep track of the other people that have them on their lists
    for p in people:
        for match in p.matches:
            dic[match[0]].add_other(p.name)
    people = sorted(people, key = lambda x: x.num_random_matches) 
    result = []
    for p in people:
        result.append((p.name, p.num_random_matches))
    for p in people:
        for k in range(p.num_random_matches):
            level = len(p.interests)+1
            end = False
            while not end and level > 0: #find what level we need to split ties between
                level -= 1
                for person in p.freq_dic[level]:
                    if person not in p.matches:
                        end = True
                        break
            lowest = None
            #find person with lowest number of matches
            for potential in p.freq_dic[level]:
                name = potential[0]
                if potential not in p.matches:
                    if lowest == None:
                        lowest = len(dic[name].other_matches) 
                    elif len(dic[name].other_matches) < lowest:
                        lowest = len(dic[name].other_matches)
            contenders = []
            if p.name == "Hope Dargan":
                print(p.freq_dic[level])
            #if there are multiple people with lowest number of other matches, create a list of "contenders"
            for potential in p.freq_dic[level]:
                name = potential[0]
                if len(dic[name].other_matches) == lowest and potential not in p.matches:
                    contenders.append(potential)
            winner = 0 if len(contenders) == 1 else random.randint(0,len(contenders)-1) #randomly selects index
            p.matches.append(contenders[winner])
            name = contenders[winner][0]
            dic[name].other_matches.append(p.name)


    
### main method calls all these functions in sequence
if __name__ == "__main__":
    run_again = True
    num_tries = 0
    MAX_NUM_TRIES = 20
    #Because there is a bit of a random element in this program, the algorithm runs
    #up to 20 times and tries to ensure that everyone ends up on at least one list
    #of the person of the opposite gender if they can do to randomness with the tiebreaker algorithm
    
    while run_again and num_tries < MAX_NUM_TRIES:
        people = read_that_text_file()
        make_frequencies(people)
        matches_made = make_matches(people)
        tiebreaker(people)
        run_again = False
        for p in people:
            if len(p.other_matches) == 0:
                run_again = True
                break
        num_tries += 1
    if run_again:
        print("Warning: someone has ended up on no lists of the opposite gender")
    #Calculate overall stats for the algorithm
    male_total = [0,0, 0, len(people)] 
    #[number of males, number of times they appeared on the opposite gender's list, max, min]
    female_total = [0,0, 0, len(people)]
    for p in people:
        num = len(p.other_matches)
        #print(p)
        if p.gender == True: #female
            female_total[0] += 1
            female_total[1] += num
            female_total[2] = num if female_total[2] < num else female_total[2]
            female_total[3] = num if female_total[3] > num else female_total[3]
        else:
            male_total[0] += 1
            male_total[1] += num
            male_total[2] = num if male_total[2] < num else male_total[2]
            male_total[3] = num if male_total[2] > num else male_total[3]

    #email peeps - requires adding your username and password
    #EmailAutomation.main(people)
    print("Final Stats")
    print("Number of natural matches: ", matches_made, " / ", len(people)*NUM_MATCHES, " aka ", int(100*matches_made/(len(people)*NUM_MATCHES)), "%")
    print("# Females:", female_total[0], "Average # matches:", female_total[1]/female_total[0])
    print("Min:", female_total[3], "Max:", female_total[2])
    print("# Males:", male_total[0], "Average # matches:", male_total[1]/male_total[0])
    print("Min:", male_total[3], "Max:", male_total[2])