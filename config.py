# MAIN EVENT

DATA_SOURCE = 'Collaboratory Cohort 1 Spreadsheet'
DATA_SOURCE_FILE = '/root/collab/collab.json'

MATCH_CSV_FILE = '/root/collab/collab.csv'
MATCH_SOURCE_FILE = '/root/collab/match.json'

#SCORED CATEGORIES

EVAL = [
        "Artist:Experimental",
        "Sched:AvailMon",
        "Sched:AvailTues",
        "Sched:AvailWeds",
        "Sched:AvailThurs",
        "Sched:AvailFri",
        "Sched:AvailSat",
        "Sched:AvailSun",
        "Topic:CurrentEvents",
        "Topic:Health",
        "Topic:History",
        "Topic:Nature",
        "Topic:Politics",
        "Topic:Relationships",
        "Topic:Religion",
        "Topic:SocialJustice",
        "Topic:Sports",
        "Topic:Technology",
        "Project:Contributions",
        "Project:Correspond"
       ]

#POINTS PER MATCH IN CATEGORY

CATS = {
        "Artist":49.0,
        "Sched":5.0,
        "Topic":4.2,
        "Project":7.0
       }