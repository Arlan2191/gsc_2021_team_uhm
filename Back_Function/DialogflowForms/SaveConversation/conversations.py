from datetime import datetime
from google.cloud import datastore

#Instantiates a client 
datastore_client = datastore.Client()
#the entity
kind = 'Records'

class Log:
    def __init__(self):
        pass

    def saveSMSForms(self, sessionID, fromNumber, info, intent):
        #name/ID for the entity
        sid = sessionID 
        #Cloud Datastore key for the entity
        task_key = datastore_client.key(kind,sid)
        #For preparing the entity
        task = datastore.Entity(key=task_key)

        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")

        personalInfo = info[0].split("/")
        survey1response = info[1].split("/")
        survey2response = info[2].split("/")

        task['User Intent'] = intent
        task['First Name'] = personalInfo[0]
        task['Middle Name'] = personalInfo[1]
        task['Last Name'] = personalInfo[2]
        task['Birthdate'] = personalInfo[3]
        task['Sex'] = personalInfo[4]
        task['Mobile Number'] = personalInfo[5]
        task['Home Address'] = personalInfo[6]
        task['City'] = personalInfo[7]
        task['Survey 1 Response'] = {'answers': survey1response}
        task['Survey 2 Response'] = {'answers' : survey2response}
        task['Date'] = str(self.date) + "/" + str(self.current_time)

        datastore_client.put(task)

        print('Saved {}: {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(task.key.name, task['User Intent'], task['First Name'], task['Middle Name'], task['Last Name'], task['Birthdate'], task['Sex'], task['Mobile Number'], task['Home Address'], task['City'], task['Barangay'], task['Date']))


    def saveMessengerForms(self, sessionID, info, intent):
        #name/ID for the entity
        sid = sessionID 
        #Cloud Datastore key for the entity
        task_key = datastore_client.key(kind,sid)
        #For preparing the entity
        task = datastore.Entity(key=task_key)

        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")

        survey1response = info[9].split("/")
        survey2response = info[10].split("/")

        task['User Intent'] = intent
        task['First Name'] = info[0]
        task['Middle Name'] = info[1]
        task['Last Name'] = info[2]
        task['Birthdate'] = info[3]
        task['Sex'] = info[4]
        task['Mobile Number'] = info[5]
        task['Home Address'] = info[6]
        task['City'] = info[7]
        task['Barangay'] = info[8]
        task['Survey 1 Response'] = {'answers': survey1response}
        task['Survey 2 Response'] = {'answers' : survey2response}
        task['Date'] = str(self.date) + "/" + str(self.current_time)

        datastore_client.put(task)

        print('Saved {}: {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(task.key.name, task['User Intent'], task['First Name'], task['Middle Name'], task['Last Name'], task['Birthdate'], task['Sex'], task['Mobile Number'], task['Home Address'], task['City'], task['Barangay'], task['Date']))


    