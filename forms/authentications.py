from django_otp.oath import TOTP
from django_otp.util import random_hex
import time


class TOTPAuthentication:
    def __init__(self):
        self.__key = str.encode(random_hex())
        self.__last_verified_counter = -1
        self.__verified = False
        self.__digit_number = 6
        self.__token_validity_period = 300

    def __create_TOTP(self):
        totpObj = TOTP(self.__key, self.__token_validity_period,
                       digits=self.__digit_number)
        totpObj.time = time.time()
        return totpObj

    def generate_token(self):
        totpObj = self.__create_TOTP()
        token = str(totpObj.token()).zfill(6)
        return token

    def verify_token(self, token, tolerance=0):
        try:
            token = int(token)
        except ValueError:
            self.__verified = False
        except:
            totpObj = self.__create_TOTP()
            if ((totpObj.t() > self.__last_verified_counter) and (totpObj.verify(token, tolerance=tolerance))):
                self.__last_verified_counter = totpObj.t()
                self.__verified = True
            else:
                self.__verified = False
        return self.__verified
