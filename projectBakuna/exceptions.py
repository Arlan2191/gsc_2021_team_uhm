class IncorrectResponse(Exception):
    def __str__(self) -> str:
        return "Sorry, your response has not been save. It seems like have a typo in your response. Please enter 'save form' to restart the process."


class IncompleteResponse(Exception):
    def __init__(self, s1Num, s2Num) -> None:
        self.__s1Num = s1Num
        self.__s2Num = s2Num

    def __str__(self) -> str:
        return "Sorry, your response has not been saved. It seems like you have not answered all the questions in the survey. It seems like you only got {} answer/s from survey 1 and {} answer/s from survey 2. Please enter 'save form' again to restart the process.".format(self.__s1Num, self.__s2Num)
