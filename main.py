import codecs, config, json, sys
sys.path.insert(0,'/root/bots')

import sheetstation

STRUCT = {"Artist:Email":"2",
       	  "Artist:FirstName":"3",
       	  "Artist:LastName":"4",
          "Artist:Role":"10",
	  "Artist:Experimental":"12",
	  "Artist:DifferentStyle":"13",
	  "Artist:DifferentSubjects":"24",
	  "Artist:Timezone":"27",
	  "Artist:TimezoneAlt":"28",
	  "Sched:AvailMon":"29",
	  "Sched:AvailTues":"30",
	  "Sched:AvailWeds":"31",
	  "Sched:AvailThurs":"32",
	  "Sched:AvailFri":"33",
	  "Sched:AvailSat":"34",
	  "Sched:AvailSun":"35",
	  "Artist:Age":"36",
	  "Artist:Gender":"37",
	  "Topic:CurrentEvents":"14",
	  "Topic:Health":"15",
	  "Topic:History":"16",
	  "Topic:Nature":"17",
	  "Topic:Politics":"18",
	  "Topic:Relationships":"19",
	  "Topic:Religion":"20",
	  "Topic:SocialJustice":"21",
	  "Topic:Sports":"22",
	  "Topic:Technology":"23",
	  "Project:Contributions":"25",
	  "Project:Correspond":"26"}

class Sheet:

	@staticmethod
	def get_data(field):
		return sheetstation.get_sheet(config.DATA_SOURCE,STRUCT[field])

class Data:

	@staticmethod
	def get_profiles():
		profile_data = {}
		for key in STRUCT.keys():
			profile_data[key] = [val.strip() for val in Sheet.get_data(key)][1:]
		return profile_data

class Participant:

	def __init__(self):
		self.participant = {}

	def get_profile(self,id):
		index = int(id)
		for key in STRUCT.keys():
			try:
				self.participant[key] = DATA[key][index]
			except IndexError:
				self.participant[key] = []
		return self.participant

#LOAD ENTIRE SHEET

DATA = Data().get_profiles()

#GET UNIQUE FIELD (EMAIL)

IDS = [id for id in DATA["Artist:Email"] if id !=""]

PARTICIPANTS = {}

#CONVERT EMAIL AS UNIQUE FIELD TO FNAME LNAME

for id in IDS:
	index = IDS.index(id)
	person = Participant()
	full_name = "%s %s" % (DATA["Artist:FirstName"][index],DATA["Artist:LastName"][index])
	full_name = full_name.encode('utf8','replace')
	PARTICIPANTS[full_name] = person.get_profile(index)

#DUMP TO JSON

with codecs.open(config.DATA_SOURCE_FILE,"w",encoding="UTF-8") as f:
	json.dump(PARTICIPANTS,f)
