import logging
import pymongo
import os

############################################ Static Values Start ############################################
EXPIRY_MINUTES = 10
SECRET_KEY = b'k2p1IAURFRzyxX7wqATNe2oxpmJCW17aG3_V5AvxHgI='
ACCESS_TOKEN_EXP = 1
REFRESH_TOKEN_EXP = 7
TOKEN_SCOPE_NURSE = 'NURSE'
TOKEN_SCOPE_JR_DOCTOR = 'JR_DOCTOR'
TOKEN_SCOPE_SR_DOCTOR = 'SR_DOCTOR'

############################################ Static Values End ############################################


############################################ Logging Conf Start ############################################
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(BASE_DIR, 'SSIDetection.log')
log = logging.getLogger('')
info_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
formatter = logging.Formatter('{"Time":"%(asctime)s", "Level":"%(levelname)s", "File":"%(filename)s", "Line":"%(lineno)d", %(message)s}')
info_handler.setFormatter(formatter)
log.addHandler(info_handler)
log.setLevel(logging.INFO)
############################################ Logging Conf End ############################################


############################################ Database Connection Start ############################################
DB_HOST = "localhost"
DB_PORT = 27017
DB_NAME = "SSI_Detection_Database"
COLLECTION_OTP = 'OTP'
COLLECTION_NURSE = 'Nurse'
COLLECTION_JR_DOCTOR = 'Jr_Doctor'
COLLECTION_SR_DOCTOR = 'Sr_Doctor'
COLLECTION_PATIENT_ADMINISTRATION_DETAILS = 'Patient_Administration_Details'
COLLECTION_MICROBIOLOGY_DETAILS = 'Microbiology_Details'
COLLECTION_ANTIBIOTIC_SURVEILLANCE_DETAILS = 'Antibiotic_Surveillance'
COLLECTION_POST_SURGERY_DETAILS = 'Post_Surgery_Details'
COLLECTION_SSI_EVALUATION_DETAILS ='SSI_Evaluation_Details'
COLLECTION_EVENT_DETAILS = 'Event_Details'


def db_conn():
    client = pymongo.MongoClient(DB_HOST, DB_PORT)
    db = client[DB_NAME]
    return db
############################################ Database Connection End ############################################


def client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except Exception as e:
        log.error(f'"Event":"GetClientIP", "Result":"Exception", "Reason":"{e}"')
        return None
