from datetime import datetime
from helpers.dbhelper import DBOperation
import random
import numpy as np
from .forms import *
from configuration import *


class JrDoctor:
    def __init__(self):
        self.db = DBOperation(DB_NAME)
        self.db_jr_doctor = DBOperation(COLLECTION_JR_DOCTOR)
        self.db_patient_admin = DBOperation(COLLECTION_PATIENT_ADMINISTRATION_DETAILS)
        self.db_microbiology = DBOperation(COLLECTION_MICROBIOLOGY_DETAILS)
        self.db_antibiotic_surveillance = DBOperation(COLLECTION_ANTIBIOTIC_SURVEILLANCE_DETAILS)
        self.db_post_surgery_details = DBOperation(COLLECTION_POST_SURGERY_DETAILS)
        self.db_ssi_evaluation_details = DBOperation(COLLECTION_SSI_EVALUATION_DETAILS)
        self.db_event_details = DBOperation(COLLECTION_EVENT_DETAILS)

    def _find(self, LOG_PREFIX, phone_number):
        success = False
        ACTION = "JrDoctor._find()"
        try:
            profile_user = self.db_jr_doctor._find_one(
                filter={
                    'phone_number': phone_number
                }
            )
            if profile_user:
                log.info(f'{LOG_PREFIX}, "Action":{ACTION}, "MobileNo":"{phone_number}", "Result":"Success"')
                success = True
                return success, profile_user
            log.info(f'{LOG_PREFIX}, "Action":{ACTION}, "MobileNo":"{phone_number}", "Result":"Failure", "Reason":"DataNotFound"')
            return success, None

        except Exception as e:
            log.error(f'{LOG_PREFIX}, "Action":{ACTION}, "MobileNo":"{phone_number}", "Result":"Failure", "Reason":"{e}"')
            return success, None

    def _add_jr_doctor(self, LOG_PREFIX ,data):
        try:
            employee_id = data.get('employee_id')
            phone_number = data.get('phone_number')
            name = data.get('name', '')
            email = data.get('email', '')
            gender = data.get('gender', '')
            department = data.get('department', '')
            date_of_birth = data.get('date_of_birth', '')


            filter_data = {
                'employee_id': employee_id,
                'phone_number': phone_number
            }

            data_dict = {
                'name': name,
                'email': email,
                'gender': gender,
                'department': department,
                'date_of_birth': date_of_birth,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
            }

            register_jr_doctor = self.db_jr_doctor._insert(upsert_filter=filter_data, data=data_dict)
            print("Junior Doctor Data saved successfully!")
            return True if register_jr_doctor.inserted_id else False

        except Exception as e:
            log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    def _update_jr_doctor(self ,LOG_PREFIX, data):
        try:
            employee_id = data.get('employee_id')
            phone_number = data.get('phone_number')
            name = data.get('name')
            email = data.get('email')
            gender = data.get('gender')
            department = data.get('department')
            date_of_birth = data.get('date_of_birth')

            filter_data = {
                'employee_id': employee_id,
                'phone_number': phone_number
            }
            data_dict = {
                'name': name,
                'email': email,
                'gender': gender,
                'department': department,
                'date_of_birth': date_of_birth,
                'verification_status': 'APPROVED',
                'updated_at': datetime.now(),
            }

            update_jr_doctor = self.db_jr_doctor._update(filter_q=filter_data, update_data=data_dict, upsert=True)

            if update_jr_doctor.modified_count > 0:
                print("Junior Doctor profile updated successfully!")
                return True
            else:
                return False

        except Exception as e:
            logging.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None


####UPDATEEEE

    def _update_patient_administration_details(self,LOG_PREFIX, data):
        try:
            patientName = data.get('patientName')
            patient_id = data.get('patient_id')
            age = data.get('age')
            gender = data.get('gender')
            patientOnSteroids = data.get('patientOnSteroids')
            diabeticPatient = data.get('diabeticPatient')
            weight = data.get('weight')
            alcoholConsumption = data.get('alcoholConsumption')
            tobaccoConsumption = data.get('tobaccoConsumption')
            lengthOfSurgery = data.get('lengthOfSurgery')
            dateOfAdmission = data.get('dateOfAdmission')
            dateOfProcedure = data.get('dateOfProcedure')
            admittingDepartment = data.get('admittingDepartment')
            departmentPrimarySurgeon = data.get('departmentPrimarySurgeon')
            procedureName = data.get('procedureName')
            diagnosis = data.get('diagnosis')
            procedureDoneBy = data.get('procedureDoneBy')
            operationTheatre = data.get('operationTheatre')
            outpatientProcedure = data.get('outpatientProcedure')
            scenarioProcedure = data.get('scenarioProcedure')
            woundClass = data.get('woundClass')
            papGiven = data.get('papGiven')
            antibioticsGiven = data.get('antibioticsGiven')
            durationPAP = data.get('durationPAP')
            ssiEventOccurred = data.get('ssiEventOccurred')
            dateOfEvent = data.get('dateOfEvent')

            filter_data = {
                'patient_id': patient_id
            }

            data_dict = {
                'patientName': patientName,
                'age': age,
                'gender': gender,
                'patientOnSteroids': patientOnSteroids,
                'diabeticPatient': diabeticPatient,
                'weight': weight,
                'alcoholConsumption': alcoholConsumption,
                'tobaccoConsumption': tobaccoConsumption,
                'lengthOfSurgery': lengthOfSurgery,
                'dateOfAdmission': dateOfAdmission,
                'dateOfProcedure': dateOfProcedure,
                'admittingDepartment': admittingDepartment,
                'departmentPrimarySurgeon': departmentPrimarySurgeon,
                'procedureName': procedureName,
                'diagnosis': diagnosis,
                'procedureDoneBy': procedureDoneBy,
                'operationTheatre': operationTheatre,
                'outpatientProcedure': outpatientProcedure,
                'scenarioProcedure': scenarioProcedure,
                'woundClass': woundClass,
                'papGiven': papGiven,
                'antibioticsGiven': antibioticsGiven,
                'durationPAP': durationPAP,
                'ssiEventOccurred': ssiEventOccurred,
                'dateOfEvent': dateOfEvent,
                'status': 'REVIEWED',
                'updated_at': datetime.now(),
            }

            update_patient_admin_details = self.db_patient_admin._update(filter_q=filter_data,update_data=data_dict, upsert=True)

            if update_patient_admin_details.modified_count > 0:
                print("Patient Administration details updated successfully!")
                return True
            else:
                return False

        except Exception as e:
            logging.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    def _update_microbiology_details(self, LOG_PREFIX, data):
        try:
            log.info(f"{LOG_PREFIX} - Received data: {data}")

            patient_id = data.get('patient_id')
            micro_organism = data.get('micro_organism')
            antibiotics_data = data.get('antibiotic', [])
            prediction = data.get('prediction', None)
            predictions = []

            if isinstance(prediction, (np.integer, np.floating)):
                prediction = prediction.item()

            if prediction == 1:
                predictions.append("CHANCES OF SSI DETECTED: ECOLI POSITIVE")
                predictions.append("Cefuroxime: Resistant 30-50%")
                predictions.append("Cefepime: Susceptibility 5-10%")
                predictions.append("Sulbactum: Intermediate 20-30%")
                predictions.append("Gentamicin: Sensitive 5-15%")
                predictions.append("10-20% - SSI INVOLVEMENT: Suspected Surgery: ABDOMINAL/GASTROINTESTINAL")
            elif prediction == 0:
                predictions.append("CHANCES OF SSI NOT DETECTED: ECOLI NEGATIVE")

            filter_data = {
                'patient_id': patient_id
            }

            data_dict = {
                'micro_organism': micro_organism,
                'antibiotic': [],
                'predictions': predictions,
                'status': 'REVIEWED',
                'updated_at': datetime.now()
            }

            for antibiotic in antibiotics_data:
                antibiotic_name = antibiotic.get('name', None)
                mic_value = antibiotic.get('mic_value', 0)
                interpretation_value = antibiotic.get('interpretation', None)

                if isinstance(mic_value, (np.integer, np.floating)):
                    mic_value = mic_value.item()

                log.info(
                    f"{LOG_PREFIX} - Processing antibiotic: {antibiotic_name}, MIC: {mic_value}, Interpretation: {interpretation_value}"
                )

                data_dict['antibiotic'].append({
                    'name': antibiotic_name,
                    'mic_value': mic_value,
                    'interpretation': interpretation_value
                })

            if not data_dict['antibiotic']:
                log.info(f"{LOG_PREFIX} - No antibiotic data provided. Adding placeholder entry.")
                data_dict['antibiotic'].append({
                    'name': 'No antibiotic data provided',
                    'mic_value': None,
                    'interpretation': None
                })

            update_microbiology_details = self.db_microbiology._update(filter_q=filter_data, update_data=data_dict,
                                                                       upsert=True)

            if update_microbiology_details.modified_count > 0:
                log.info(f"{LOG_PREFIX} - Patient microbiology details updated successfully!")
                return True
            else:
                log.warning(f"{LOG_PREFIX} - No records were updated for patient_id: {patient_id}")
                return False

        except Exception as e:
            log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"{e}"')
            return None

    def _update_patient_antibiotic_details(self, LOG_PREFIX, data):
        try:
            patient_id = data.get('patient_id')
            antibiotic_prior_1 = data.get('antibiotic_prior_1')
            route_prior_1 = data.get('route_prior_1')
            duration_prior_1 = data.get('duration_prior_1')
            doses_prior_1 = data.get('doses_prior_1')
            antibiotic_prior_2 = data.get('antibiotic_prior_2')
            route_prior_2 = data.get('route_prior_2')
            duration_prior_2 = data.get('duration_prior_2')
            doses_prior_2 = data.get('doses_prior_2')
            antibiotic_prior_3 = data.get('antibiotic_prior_3')
            route_prior_3 = data.get('route_prior_3')
            duration_prior_3 = data.get('duration_prior_3')
            doses_prior_3 = data.get('doses_prior_3')
            antibiotic_pre_1 = data.get('antibiotic_pre_1')
            route_pre_1 = data.get('route_pre_1')
            duration_pre_1 = data.get('duration_pre_1')
            doses_pre_1 = data.get('doses_pre_1')
            antibiotic_pre_2 = data.get('antibiotic_pre_2')
            route_pre_2 = data.get('route_pre_2')
            duration_pre_2 = data.get('duration_pre_2')
            doses_pre_2 = data.get('doses_pre_2')
            antibiotic_pre_3 = data.get('antibiotic_pre_3')
            route_pre_3 = data.get('route_pre_3')
            duration_pre_3 = data.get('duration_pre_3')
            doses_pre_3 = data.get('doses_pre_3')
            antibiotic_post_1 = data.get('antibiotic_post_1')
            route_post_1 = data.get('route_post_1')
            duration_post_1 = data.get('duration_post_1')
            doses_post_1 = data.get('doses_post_1')
            antibiotic_post_2 = data.get('antibiotic_post_2')
            route_post_2 = data.get('route_post_2')
            duration_post_2 = data.get('duration_post_2')
            doses_post_2 = data.get('doses_post_2')
            antibiotic_post_3 = data.get('antibiotic_post_3')
            route_post_3 = data.get('route_post_3')
            duration_post_3 = data.get('duration_post_3')
            doses_post_3 = data.get('doses_post_3')
            antibiotic_post_4 = data.get('antibiotic_post_4')
            route_post_4 = data.get('route_post_4')
            duration_post_4 = data.get('duration_post_4')
            doses_post_4 = data.get('doses_post_4')
            antibiotic_post_5 = data.get('antibiotic_post_5')
            route_post_5 = data.get('route_post_5')
            duration_post_5 = data.get('duration_post_5')
            doses_post_5 = data.get('doses_post_5')
            antibiotic_post_6 = data.get('antibiotic_post_6')
            route_post_6 = data.get('route_post_6')
            duration_post_6 = data.get('duration_post_6')
            doses_post_6 = data.get('doses_post_6')
            time_induction = data.get('time_induction')
            time_incision = data.get('time_incision')
            time_end_surgery = data.get('time_end_surgery')

            filter_data = {
                'patient_id': patient_id
            }

            data_dict = {
                'antibiotic_prior_1': antibiotic_prior_1,
                'route_prior_1': route_prior_1,
                'duration_prior_1': duration_prior_1,
                'doses_prior_1': doses_prior_1,
                'antibiotic_prior_2': antibiotic_prior_2,
                'route_prior_2': route_prior_2,
                'duration_prior_2': duration_prior_2,
                'doses_prior_2' : doses_prior_2,
                'antibiotic_prior_3': antibiotic_prior_3,
                'route_prior_3': route_prior_3,
                'duration_prior_3': duration_prior_3,
                'doses_prior_3': doses_prior_3,
                'antibiotic_pre_1': antibiotic_pre_1,
                'route_pre_1': route_pre_1,
                'duration_pre_1': duration_pre_1,
                'doses_pre_1': doses_pre_1,
                'antibiotic_pre_2': antibiotic_pre_2,
                'route_pre_2': route_pre_2,
                'duration_pre_2': duration_pre_2,
                'doses_pre_2': doses_pre_2,
                'antibiotic_pre_3': antibiotic_pre_3,
                'route_pre_3': route_pre_3,
                'duration_pre_3': duration_pre_3,
                'doses_pre_3': doses_pre_3,
                'antibiotic_post_1': antibiotic_post_1,
                'route_post_1': route_post_1,
                'duration_post_1': duration_post_1,
                'doses_post_1': doses_post_1,
                'antibiotic_post_2': antibiotic_post_2,
                'route_post_2': route_post_2,
                'duration_post_2': duration_post_2,
                'doses_post_2': doses_post_2,
                'antibiotic_post_3': antibiotic_post_3,
                'route_post_3': route_post_3,
                'duration_post_3': duration_post_3,
                'doses_post_3': doses_post_3,
                'antibiotic_post_4': antibiotic_post_4,
                'route_post_4': route_post_4,
                'duration_post_4': duration_post_4,
                'doses_post_4': doses_post_4,
                'antibiotic_post_5': antibiotic_post_5,
                'route_post_5': route_post_5,
                'duration_post_5': duration_post_5,
                'doses_post_5': doses_post_5,
                'antibiotic_post_6': antibiotic_post_6,
                'route_post_6': route_post_6,
                'duration_post_6': duration_post_6,
                'doses_post_6': doses_post_6,
                'time_induction': time_induction,
                'time_incision': time_incision,
                'time_end_surgery': time_end_surgery,
                'status': 'REVIEWED',
                'updated_at': datetime.now(),
            }

            update_patient_antibiotic_details = self.db_antibiotic_surveillance._update(filter_q=filter_data,update_data=data_dict, upsert=True)

            if update_patient_antibiotic_details.modified_count > 0:
                print("Patient Antibiotic Surveillance details updated successfully!")
                return True
            else:
                return False

        except Exception as e:
            logging.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    def _update_post_op_details(self, LOG_PREFIX, data):
        try:
            log.info(f"{LOG_PREFIX} - Received data: {data}")

            patient_id = data.get('patient_id')
            date_of_procedure = data.get('date_of_procedure')
            name_of_procedure = data.get('name_of_procedure')
            symptoms_data = data.get('symptoms', [])

            filter_data = {
                'patient_id': patient_id
            }

            data_dict = {
                'date_of_procedure': date_of_procedure,
                'name_of_procedure': name_of_procedure,
                'status': 'REVIEWED',
                'symptoms': [],
                'updated_at': datetime.now()
            }

            for symptom_data in symptoms_data:
                symptom = symptom_data.get('symptom', 'No symptom data provided')
                days = symptom_data.get('days', [])

                symptom_entry = {
                    'symptom': symptom,
                    'days': [{'day': day.get('day'), 'status': day.get('status', 'Empty')} for day in days]
                }

                data_dict['symptoms'].append(symptom_entry)

            if not data_dict['symptoms']:
                log.info(f"{LOG_PREFIX} - No symptoms data provided. Adding placeholder entry.")
                data_dict['symptoms'].append({
                    'symptom': 'No symptom data provided',
                    'days': []
                })

            update_post_op_details = self.db_post_surgery_details._update(filter_q=filter_data, update_data=data_dict, upsert=True)

            if update_post_op_details.modified_count > 0:
                print("Patient Post Op details updated successfully!")
                return True
            else:
                return False

        except Exception as e:
            logging.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    def _update_ssi_evaluation_details(self, LOG_PREFIX, data):
        try:
            log.info(f"{LOG_PREFIX} - Received data for update: {data}")

            patient_id = data.get('patient_id')
            procedure_name = data.get('procedure_name')
            patient_name = data.get('patient_name')
            age = data.get('age')
            gender = data.get('gender')
            date_of_procedure = data.get('date_of_procedure')
            evaluation_fields = data.get('evaluation_fields', [])

            filter_data = {
                'patient_id': patient_id
            }

            update_data = {
                'procedure_name': procedure_name,
                'patient_name': patient_name,
                'age': age,
                'gender': gender,
                'date_of_procedure': date_of_procedure,
                'evaluation_fields': evaluation_fields,
                'status': 'REVIEWED',
                'updated_at': datetime.now()
            }

            update_ssi_evaluation_details = self.db_ssi_evaluation_details._update(filter_q=filter_data, update_data=update_data, upsert=True)

            log.info(f"{LOG_PREFIX} - Update result: {update_ssi_evaluation_details}")

            if update_ssi_evaluation_details and update_ssi_evaluation_details.modified_count > 0:
                return True
            else:
                return False

        except Exception as e:
            logging.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    def _update_event_details(self, LOG_PREFIX, data):
        try:
            patient_id = data.get('patient_id')
            specific_event = data.get('specific_event')
            organ_space_site = data.get('organ_space_site')
            detected = data.get('detected')
            sample_types = data.get('sample_types')
            site_of_sample_collection = data.get('site_of_sample_collection')
            secondary_bsi_contributed = data.get('secondary_bsi_contributed')

            filter_data = {
                'patient_id': patient_id
            }

            data_dict = {
                'specific_event': specific_event,
                'organ_space_site': organ_space_site,
                'detected': detected,
                'sample_types': sample_types,
                'site_of_sample_collection': site_of_sample_collection,
                'secondary_bsi_contributed': secondary_bsi_contributed,
                'status': 'REVIEWED',
                'updated_at': datetime.now()
            }

            update_patient_event_details = self.db_event_details._update(filter_q=filter_data, update_data=data_dict, upsert=True)

            if update_patient_event_details.modified_count > 0:
                print("Patient Event details updated successfully!")
                return True
            else:
                return False

        except Exception as e:
            logging.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    ###GET

    def _patient_admin_details(self, LOG_PREFIX, patient_id):
        try:
            data_dict = {
                'patient_id': patient_id,
            }
            log.info("PATIENT ADMIN COLLECTION ::: %s" %self.db_patient_admin.coll_name)
            patient_admin_details = self.db_patient_admin._find_one(filter=data_dict)
            return patient_admin_details

        except Exception as e:
            log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    def _patient_microbiology_details(self, LOG_PREFIX, patient_id):
        try:
            data_dict = {
                'patient_id': patient_id,
            }
            log.info("PATIENT MICROBIOLOGY COLLECTION ::: %s" %self.db_microbiology.coll_name)
            patient_admin_details = self.db_microbiology._find_one(filter=data_dict)
            return patient_admin_details

        except Exception as e:
            log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    def _patient_antibiotic_surveillance_details(self, LOG_PREFIX, patient_id):
        try:
            data_dict = {
                'patient_id': patient_id,
            }
            log.info("PATIENT ANTIBIOTIC SURVEILLANCE COLLECTION ::: %s" % self.db_antibiotic_surveillance.coll_name)
            patient_antibiotic_details = self.db_antibiotic_surveillance._find_one(filter=data_dict)
            return patient_antibiotic_details

        except Exception as e:
            log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    def _patient_post_surgery_details(self, LOG_PREFIX, patient_id):
        try:
            data_dict = {
                'patient_id': patient_id,
            }
            log.info("PATIENT POST SURGERY COLLECTION ::: %s" % self.db_post_surgery_details.coll_name)
            patient_post_surgery_details = self.db_post_surgery_details._find_one(filter=data_dict)
            return patient_post_surgery_details

        except Exception as e:
            log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    def _patient_ssi_evaluation_details(self, LOG_PREFIX, patient_id):
        try:
            data_dict = {
                'patient_id': patient_id,
            }
            log.info("PATIENT SSI EVALUATION COLLECTION ::: %s" % self.db_ssi_evaluation_details.coll_name)
            patient_ssi_evaluation_details = self.db_ssi_evaluation_details._find_one(filter=data_dict)
            return patient_ssi_evaluation_details

        except Exception as e:
            log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    def _patient_event_details(self, LOG_PREFIX, patient_id):
        try:
            data_dict = {
                'patient_id': patient_id,
            }
            log.info("PATIENT EVENT COLLECTION ::: %s" % self.db_event_details.coll_name)
            patient_event_details = self.db_event_details._find_one(filter=data_dict)
            return patient_event_details

        except Exception as e:
            log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    def _get_patient_list(self, LOG_PREFIX, data):
        try:
            query = {}

            required_keys = ['patient_id', 'patientName']

            log.info("QUERY :: %s" % query)

            patient_list = self.db_patient_admin._find_all(filter=query, required_keys=required_keys)

            log.info("COLLECTION : %s" % self.db_patient_admin.coll_name)
            return patient_list

        except Exception as e:
            log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None


