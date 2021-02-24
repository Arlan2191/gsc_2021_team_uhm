
from abc import ABC, abstractmethod


class Checker(ABC):
    @abstractmethod
    def isCorrect(self):
        pass
    @abstractmethod
    def isComplete(self):
        pass
    @abstractmethod
    def numberOfAnswers(self):
        pass

class SmsForm(Checker):
    def __init__(self):
        pass
    
    def isCorrect(self, survey1response, survey2response):
        survey1 = survey1response.split("/")
        survey2 = survey2response.split("/")

        for i in range(len(survey1)):
            if survey1[i].lower().strip() == 'hindi' or survey1[i].lower().strip() == 'oo':
                if i == len(survey1):
                    print("Survey 1 Clear\n")    
            else:
                return False


        for i in range(len(survey2)):
            if survey2[i].lower().strip() == 'hindi' or survey2[i].lower().strip() == 'oo':
                if i == len(survey2):
                    print("Survey 2 Clear\n")
            else:
                return False

        return True

    def isComplete(self, personalInfo, survey1response, survey2response):
        pInfo = personalInfo.split("/")
        survey1 = survey1response.split("/")
        survey2 = survey2response.split("/")

        if len(pInfo) != 9: 
            print("number of answers in personal info survey:" + str(len(pInfo))) 
            return False
        #There are 18 questions present in survey 1, it must contain equal amount of answers
        if len(survey1) != 18:
            print("number of answers in survey 1:" + str(len(survey1))) 
            return False
        #There are 14 questions present in survey 2
        if len(survey2) != 14: 
            print("number of answers in survey 2:" + str(len(survey2))) 
            return False

        return True

    def numberOfAnswers(self,survey):
        length = survey.split("/")
        return len(length)

class MessengerForm(Checker):
    def __init__(self):
        pass

    def isCorrect(self, survey1response, survey2response):
        survey1 = survey1response.split("/")
        survey2 = survey2response.split("/")
        
        for i in range(len(survey1)):
            if survey1[i].lower().strip() == 'hindi' or survey1[i].lower().strip() == 'oo':
                if i == len(survey1):
                    print("Survey 1 Clear\n")    
            else:
                return False


        for i in range(len(survey2)):
            if survey2[i].lower().strip() == 'hindi' or survey2[i].lower().strip() == 'oo':
                if i == len(survey2):
                    print("Survey 2 Clear\n")
            else:
                return False

        return True

    
    def isComplete(self,survey1response,survey2response):

        survey1 = survey1response.split("/")
        survey2 = survey2response.split("/")

        #There are 18 questions present in survey 1, it must contain equal amount of answers
        if len(survey1) != 18:
            print("length of survey 1:" + str(len(survey1)))
            return False
        #There are 14 questions present in survey 2
        if len(survey2) != 14: 
            print("length of survey 2:" + str(len(survey2)))
            return False

        return True

    def numberOfAnswers(self,survey):
        length = survey.split("/")
        return len(length)