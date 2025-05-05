from datetime import datetime
# from bson.objectid import ObjectId
from helpers.dbhelper import DBOperation
import random
import numpy as np
from .forms import *
from configuration import *


class Nurse:

    def __init__(self):
        self.db = DBOperation(DB_NAME)
        self.db_nurse = DBOperation(COLLECTION_NURSE)
        self.db_patient_admin = DBOperation(COLLECTION_PATIENT_ADMINISTRATION_DETAILS)
        self.db_microbiology = DBOperation(COLLECTION_MICROBIOLOGY_DETAILS)
        self.db_antibiotic_surveillance = DBOperation(COLLECTION_ANTIBIOTIC_SURVEILLANCE_DETAILS)
        self.db_post_surgery_details = DBOperation(COLLECTION_POST_SURGERY_DETAILS)
        self.db_ssi_evaluation_details = DBOperation(COLLECTION_SSI_EVALUATION_DETAILS)
        self.db_event_details = DBOperation(COLLECTION_EVENT_DETAILS)

###NURSE

    def _find(self, LOG_PREFIX, phone_number):
        success = False
        ACTION = "Nurse._find()"
        try:
            profile_user = self.db_nurse._find_one(
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

    def _add_nurse(self, LOG_PREFIX,data):
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

            register_nurse = self.db_nurse._insert(upsert_filter=filter_data, data=data_dict)
            print("Nurse Data saved successfully!")
            return True if register_nurse.inserted_id else False

        except Exception as e:
            log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    def _update_nurse(self,LOG_PREFIX, data):
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

            update_nurse = self.db_nurse._update(filter_q=filter_data, update_data=data_dict, upsert=True)

            if update_nurse.modified_count > 0:
                print("Nurse profile updated successfully!")
                return True
            else:
                return False

        except Exception as e:
            logging.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None


##ADDDD
    def _add_patient_administration_details(self, LOG_PREFIX, data):
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
            data_dict = {
                'patientName': patientName,
                'patient_id': patient_id,
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
                'status': 'ADDED',
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
            }

            insert_patient_admin_details = self.db_patient_admin._insert(data=data_dict)

            return True if insert_patient_admin_details.inserted_id else False

        except Exception as e:
            logging.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    # def _add_microbiology_details(self, LOG_PREFIX, data):
    #     try:
    #         log.info(f"{LOG_PREFIX} - Received data: {data}")
    #
    #         micro_organism = data.get('micro_organism')
    #         antibiotics_data = data.get('antibiotic', [])
    #
    #         data_dict = {
    #             'micro_organism': micro_organism,
    #             'antibiotic': [],
    #             'created_at': datetime.now(),
    #             'updated_at': datetime.now()
    #         }
    #
    #         for antibiotic in antibiotics_data:
    #             antibiotic_name = antibiotic.get('name', None)
    #             mic_value = antibiotic.get('mic_value', 0)
    #             interpretation_value = antibiotic.get('interpretation', None)
    #             log.info(
    #                 f"{LOG_PREFIX} - Processing antibiotic: {antibiotic_name}, MIC: {mic_value}, Interpretation: {interpretation_value}")
    #
    #             data_dict['antibiotic'].append({
    #                 'name': antibiotic_name,
    #                 'mic_value': mic_value,
    #                 'interpretation': interpretation_value
    #             })
    #
    #         if not data_dict['antibiotic']:
    #             log.info(f"{LOG_PREFIX} - No antibiotic data provided. Adding placeholder entry.")
    #             data_dict['antibiotic'].append({
    #                 'name': 'No antibiotic data provided',
    #                 'mic_value': None,
    #                 'interpretation': None
    #             })
    #
    #         log.info(f"{LOG_PREFIX} - Final data dict to insert: {data_dict}")
    #
    #         insert_microbiology_details = self.db_microbiology._insert(data=data_dict)
    #
    #         log.info(f"{LOG_PREFIX} - Insert result: {insert_microbiology_details}")
    #
    #         return True if insert_microbiology_details.inserted_id else False
    #
    #     except Exception as e:
    #         logging.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"{e}"')
    #         return None

    def _add_microbiology_details(self, LOG_PREFIX, data):
        try:
            log.info(f"{LOG_PREFIX} - Received data: {data}")

            patient_id = data.get('patient_id')
            micro_organism = data.get('micro_organism')
            antibiotics_data = data.get('antibiotic', [])
            prediction = data.get('prediction', None)  # Include prediction field
            predictions = []  # Initialize logs list to store log messages

            if isinstance(prediction, (np.integer, np.floating)):
                prediction = prediction.item()

            # Log messages based on prediction
            if prediction == 1:
                predictions.append("CHANCES OF SSI DETECTED: ECOLI POSITIVE")
                predictions.append("Cefuroxime: Resistant 30-50%")
                predictions.append("Cefepime: Susceptibility 5-10%")
                predictions.append("Sulbactum: Intermediate 20-30%")
                predictions.append("Gentamicin: Sensitive 5-15%")
                predictions.append("10-20% - SSI INVOLVEMENT: Suspected Surgery: ABDOMINAL/GASTROINTESTINAL")
            elif prediction == 0:
                predictions.append("CHANCES OF SSI NOT DETECTED: ECOLI NEGATIVE")

            data_dict = {
                'patient_id': patient_id,
                'micro_organism': micro_organism,
                'antibiotic': [],
                # 'prediction': prediction,
                'predictions': predictions,
                'status': 'ADDED',
                'created_at': datetime.now(),
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

            log.info(f"{LOG_PREFIX} - Final data dict to insert: {data_dict}")

            insert_microbiology_details = self.db_microbiology._insert(data=data_dict)

            if insert_microbiology_details and hasattr(insert_microbiology_details, 'inserted_id'):
                log.info(f"{LOG_PREFIX} - Insert result: {insert_microbiology_details.inserted_id}")
                return True
            else:
                log.error(f"{LOG_PREFIX} - Insert failed. Insert result: {insert_microbiology_details}")
                return False

        except Exception as e:
            log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"{e}"')
            return None

    # def _add_microbiology_details(self, LOG_PREFIX, data):
    #     try:
    #         log.info(f"{LOG_PREFIX} - Received data: {data}")
    #
    #         patient_id = data.get('patient_id')
    #         micro_organism = data.get('micro_organism')
    #         antibiotics_data = data.get('antibiotic', [])
    #         prediction = data.get('prediction', None)  # Include prediction field
    #
    #         if isinstance(prediction, (np.integer, np.floating)):
    #             prediction = prediction.item()
    #
    #         data_dict = {
    #             'patient_id': patient_id,
    #             'micro_organism': micro_organism,
    #             'antibiotic': [],
    #             'prediction': prediction,
    #             'created_at': datetime.now(),
    #             'updated_at': datetime.now()
    #         }
    #
    #         for antibiotic in antibiotics_data:
    #             antibiotic_name = antibiotic.get('name', None)
    #             mic_value = antibiotic.get('mic_value', 0)
    #             interpretation_value = antibiotic.get('interpretation', None)
    #
    #             # Convert mic_value to native Python type
    #             if isinstance(mic_value, (np.integer, np.floating)):
    #                 mic_value = mic_value.item()
    #
    #             log.info(
    #                 f"{LOG_PREFIX} - Processing antibiotic: {antibiotic_name}, MIC: {mic_value}, Interpretation: {interpretation_value}"
    #             )
    #
    #             data_dict['antibiotic'].append({
    #                 'name': antibiotic_name,
    #                 'mic_value': mic_value,
    #                 'interpretation': interpretation_value
    #             })
    #
    #         if not data_dict['antibiotic']:
    #             log.info(f"{LOG_PREFIX} - No antibiotic data provided. Adding placeholder entry.")
    #             data_dict['antibiotic'].append({
    #                 'name': 'No antibiotic data provided',
    #                 'mic_value': None,
    #                 'interpretation': None
    #             })
    #
    #         log.info(f"{LOG_PREFIX} - Final data dict to insert: {data_dict}")
    #
    #         insert_microbiology_details = self.db_microbiology._insert(data=data_dict)
    #
    #         if insert_microbiology_details and hasattr(insert_microbiology_details, 'inserted_id'):
    #             log.info(f"{LOG_PREFIX} - Insert result: {insert_microbiology_details.inserted_id}")
    #             return True
    #         else:
    #             log.error(f"{LOG_PREFIX} - Insert failed. Insert result: {insert_microbiology_details}")
    #             return False
    #
    #     except Exception as e:
    #         logging.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"{e}"')
    #         return None

    def _add_antibiotic_surveillance(self, LOG_PREFIX, data):
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

            data_dict = {
                'patient_id': patient_id,
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
                'status': 'ADDED',
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
            }
            insert_antibiotics_surveillance_details = self.db_antibiotic_surveillance._insert(data=data_dict)

            return True if insert_antibiotics_surveillance_details.inserted_id else False

        except Exception as e:
            logging.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None

    def _add_post_op_details(self, LOG_PREFIX, data):
        try:
            log.info(f"{LOG_PREFIX} - Received data: {data}")

            patient_id = data.get('patient_id')
            date_of_procedure = data.get('date_of_procedure')
            name_of_procedure = data.get('name_of_procedure')
            symptoms_data = data.get('symptoms', [])

            data_dict = {
                'patient_id': patient_id,
                'date_of_procedure': date_of_procedure,
                'name_of_procedure': name_of_procedure,
                'symptoms': [],
                'status': 'ADDED',
                'created_at': datetime.now(),
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

            insert_post_op_details = self.db_post_surgery_details._insert(data=data_dict)

            log.info(f"{LOG_PREFIX} - Insert result: {insert_post_op_details}")

            return True if insert_post_op_details.inserted_id else False

        except Exception as e:
            log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"{e}"')
            return None

    def _add_ssi_evaluation(self, LOG_PREFIX, data):
        try:
            log.info(f"{LOG_PREFIX} - Received data: {data}")

            patient_id = data.get('patient_id')
            procedure_name = data.get('procedure_name', 'Not Provided')
            patient_name = data.get('patient_name', 'Unknown')
            age = data.get('age', 'Unknown')
            gender = data.get('gender', 'Not Specified')
            date_of_procedure = data.get('date_of_procedure', 'Not Provided')
            evaluation_fields = data.get('evaluation_fields', {})

            data_dict = {
                'patient_id': patient_id,
                'procedure_name': procedure_name,
                'patient_name': patient_name,
                'age': age,
                'gender': gender,
                'date_of_procedure': date_of_procedure,
                'evaluation_fields': [],
                'status': 'ADDED',
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }

            for field_name, field_data in evaluation_fields.items():
                choice = field_data.get('choice', 'Not Specified')
                remarks = field_data.get('remarks', 'No Remarks')

                field_entry = {
                    'field_name': field_name,
                    'choice': choice,
                    'remarks': remarks
                }

                data_dict['evaluation_fields'].append(field_entry)

            if not data_dict['evaluation_fields']:
                log.info(f"{LOG_PREFIX} - No evaluation fields provided. Adding placeholder entry.")
                data_dict['evaluation_fields'].append({
                    'field_name': 'No Field Data',
                    'choice': 'Not Specified',
                    'remarks': 'No Remarks'
                })

            insert_ssi_evaluation = self.db_ssi_evaluation_details._insert(data=data_dict)

            log.info(f"{LOG_PREFIX} - Insert result: {insert_ssi_evaluation}")

            return True if insert_ssi_evaluation.inserted_id else False

        except Exception as e:
            log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"{e}"')
            return None

    def _add_event_details(self, LOG_PREFIX, data):
        try:
            patient_id = data.get('patient_id')
            specific_event = data.get('specific_event')
            organ_space_site = data.get('organ_space_site')
            detected = data.get('detected')
            sample_types = data.get('sample_types')
            site_of_sample_collection = data.get('site_of_sample_collection')
            secondary_bsi_contributed = data.get('secondary_bsi_contributed')

            data_dict = {
                'patient_id': patient_id,
                'specific_event': specific_event,
                'organ_space_site': organ_space_site,
                'detected': detected,
                'sample_types': sample_types,
                'site_of_sample_collection': site_of_sample_collection,
                'secondary_bsi_contributed': secondary_bsi_contributed,
                'status': 'ADDED',
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
            }

            insert_event_details = self.db_event_details._insert(data=data_dict)

            return True if insert_event_details.inserted_id else False

        except Exception as e:
            logging.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
            return None
