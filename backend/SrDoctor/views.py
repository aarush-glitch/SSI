from Nurse.views import verify_auth_token
import json
import os
import pickle
from django.http import JsonResponse
from .forms import *
from .register_views import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from configuration import *
from JrDoctor.forms import *
import math
from functools import wraps
from helpers.jwthelper import JWToken
import random
from .models import *


@csrf_exempt
@require_http_methods(["POST"])
@verify_auth_token
def update_sr_doctor_details(request, *args, **kwargs):
    cls_register = SrDoctor()
    EVENT = "UpdateJuniorDoctorDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    try:
        decoded_body = json.loads(request.body.decode())
        form = SrDoctorUpdateForm(decoded_body)

        if not form.is_valid():
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})

        employee_id = kwargs.get('employee_id')
        log.info("EMPLOYEE ID :%s" % employee_id)

        if not employee_id:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Employee ID is required!"})

        phone_number = kwargs.get('phone_number')
        log.info("PHONE NUMBER :%s" % phone_number)

        if not phone_number:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Phone Number is required!"})

        update_data = {
            'employee_id': employee_id,
            'phone_number': phone_number,
            'name': decoded_body.get('name'),
            'email': decoded_body.get('email'),
            'gender': decoded_body.get('gender'),
            'department': decoded_body.get('department'),
            'date_of_birth': decoded_body.get('date_of_birth'),
            'updated_at': datetime.now(),
        }

        log.info(f'{LOG_PREFIX}, "UpdateData": {update_data}')

        sr_doctor_details_update = cls_register._update_sr_doctor(LOG_PREFIX, data=update_data)

        log.info(f'{LOG_PREFIX}, "SeniorDoctorUpdateResult": {sr_doctor_details_update}')

        if sr_doctor_details_update:
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "Senior Doctor details updated successfully!"})
        else:
            return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Failed to update Seniors Doctor details!"})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error"})


@csrf_exempt
@require_http_methods(["POST"])
# @verify_auth_token
def add_srDoctor_details(request, *args, **kwargs):
    EVENT = "AddJrDoctorDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_nurse = SrDoctor()
    try:
        decoded_body = json.loads(request.body.decode())
        form = SrDoctorForm(decoded_body)

        if not form.is_valid():
            log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"Form validation failed", "Errors":{form.errors}')
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})

        phone_number = kwargs.get('phone_number')
        employee_id = kwargs.get('employee_id')
        if not phone_number or not employee_id:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Phone number and employee ID are required"})


        data_dict = {
            'name': decoded_body.get('name'),
            'email': decoded_body.get('email'),
            'gender': decoded_body.get('gender'),
            'department': decoded_body.get('department'),
            'phone_number': phone_number,
            'date_of_birth': decoded_body.get('date_of_birth'),
        }

        insert_jrdoctor = cls_nurse._add_sr_doctor(LOG_PREFIX, data=data_dict)
        log.info(f"INSERT NURSE DETAILS : {insert_jrdoctor}")

        if insert_jrdoctor:
            return JsonResponse(
                {"status": "SUCCESS", "statuscode": 200, "msg": "Senior Doctor details added successfully!"}
            )
        else:
            return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Failed to add Senior Doctor details!"})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})

# UPDATEEEEE

@csrf_exempt
@require_http_methods(["POST"])
def update_patient_admin_details(request, *args, **kwargs):
    cls_nurse = SrDoctor()
    EVENT = "UpdatePatientAdminDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    try:
        decoded_body = json.loads((request.body).decode())
        form = PatientAdministrationUpdateForm(decoded_body)
        if not form.is_valid():
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})
        patient_id = decoded_body.get('patient_id')

        update_data = {
            'patient_id': patient_id,
            'patientName': decoded_body.get('patientName'),
            'age': decoded_body.get('age'),
            'gender': decoded_body.get('gender'),
            'patientOnSteroids': decoded_body.get('patientOnSteroids'),
            'diabeticPatient': decoded_body.get('diabeticPatient'),
            'weight': decoded_body.get('weight'),
            'alcoholConsumption': decoded_body.get('alcoholConsumption'),
            'tobaccoConsumption': decoded_body.get('tobaccoConsumption'),
            'lengthOfSurgery': decoded_body.get('lengthOfSurgery'),
            'dateOfAdmission': decoded_body.get('dateOfAdmission'),
            'dateOfProcedure': decoded_body.get('dateOfProcedure'),
            'admittingDepartment': decoded_body.get('admittingDepartment'),
            'departmentPrimarySurgeon': decoded_body.get('departmentPrimarySurgeon'),
            'procedureName': decoded_body.get('procedureName'),
            'diagnosis': decoded_body.get('diagnosis'),
            'procedureDoneBy': decoded_body.get('procedureDoneBy'),
            'operationTheatre': decoded_body.get('operationTheatre'),
            'outpatientProcedure': decoded_body.get('outpatientProcedure'),
            'scenarioProcedure': decoded_body.get('scenarioProcedure'),
            'woundClass': decoded_body.get('woundClass'),
            'papGiven': decoded_body.get('papGiven'),
            'antibioticsGiven': decoded_body.get('antibioticsGiven'),
            'durationPAP': decoded_body.get('durationPAP'),
            'ssiEventOccurred': decoded_body.get('ssiEventOccurred'),
            'dateOfEvent': decoded_body.get('dateOfEvent')
        }
        log.info("update_data :%s" % update_data)

        if not patient_id:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "PATIENT ID is required"})

        patient_details_update = cls_nurse._update_patient_administration_details(LOG_PREFIX, data=update_data)

        log.info("RES UPDATE :%s" % patient_details_update)

        if patient_details_update:
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "Patient Administration Details updated successfully!"})
        else:
            return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Failed to update Patient Administration Details!"})
    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})


@csrf_exempt
@require_http_methods(["POST"])
def update_microbiology_details(request, *args, **kwargs):
    EVENT = "UpdateMicrobiologyDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_nurse = SrDoctor()

    try:
        patient_id = request.session.get('patient_id')
        log.info(f"{LOG_PREFIX}, 'Step':'Retrieve Patient ID', 'PatientID':{patient_id}")

        if not patient_id:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Patient ID not found in session!"})

        model_path = os.path.join(os.path.dirname(__file__), 'ml_model', 'SSI_model.pkl')
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)

        decoded_body = json.loads(request.body.decode())
        form = MicrobiologyUpdateForm(decoded_body)

        if not form.is_valid():
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})

        data_dict = {
            'patient_id': patient_id,
            'micro_organism': decoded_body.get('micro_organism'),
            'antibiotic': [],
            'predictions': None
        }

        features = [
            decoded_body.get('Ecoli', 0),
            decoded_body.get('Cefuroxime', 0),
            decoded_body.get('Cefuroxime_MIC', 68),
            decoded_body.get('Resistant', 0),
            decoded_body.get('Cefepime', 0),
            decoded_body.get('Cefepime_MIC', 8),
            decoded_body.get('Susceptibility_Dose_Dependent', 0),
            decoded_body.get('Cefoperazone_Sulbactum', 0),
            decoded_body.get('Cefoperazone_Sulbactum_MIC', 32),
            decoded_body.get('Intermediate', 0),
            decoded_body.get('Gentamicin', 0),
            decoded_body.get('Gentamicin_MIC', 0.032),
            decoded_body.get('Sensitive', 0)
        ]

        log.info(f"{LOG_PREFIX}, 'Step':'ML Prediction', 'Features':{features}")

        prediction = model.predict([features])[0]
        data_dict['prediction'] = prediction
        log.info(f"{LOG_PREFIX}, 'Step':'ML Prediction', 'Prediction':{prediction}")

        for antibiotic in ANTIBIOTIC_CHOICES:
            antibiotic_name = antibiotic[0]
            antibiotic_key = antibiotic_name.lower().replace(' ', '_').replace('-', '_')

            mic_value = decoded_body.get(f"{antibiotic_key}_mic")
            interpretation = decoded_body.get(f"{antibiotic_key}_interpretation")

            log.info(f"Antibiotic: {antibiotic_name}, MIC: {mic_value}, Interpretation: {interpretation}")

            if mic_value or interpretation:
                data_dict['antibiotic'].append({
                    'name': antibiotic_name,
                    'mic_value': mic_value if mic_value else None,
                    'interpretation': interpretation if interpretation else None
                })

        if not data_dict['antibiotic']:
            data_dict['antibiotic'].append({
                'name': 'No antibiotic data provided',
                'mic_value': None,
                'interpretation': None
            })

        log.info(f"{LOG_PREFIX}, 'Step':'Data Preparation', 'DataDict':{data_dict}")

        update_result = cls_nurse._update_microbiology_details(LOG_PREFIX, data=data_dict)
        log.info(f"{LOG_PREFIX}, 'Result':'Updated Microbiology Details', 'Details':{update_result}")

        if update_result:
            return JsonResponse(
                {"status": "SUCCESS", "statuscode": 200, "msg": "Patient's Microbiology details updated successfully!"})
        else:
            return JsonResponse(
                {"status": "FAILURE", "statuscode": 500, "msg": "Failed to update patient's microbiology details!"})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})


@csrf_exempt
@require_http_methods(["POST"])
def update_antibiotic_details(request, *args, **kwargs):
    EVENT = "UpdateAntibioticSurveillanceDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_nurse = SrDoctor()

    try:
        decoded_body = json.loads((request.body).decode())

        form = AntibioticSurveillanceUpdateForm(decoded_body)
        if not form.is_valid():
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})
        patient_id = decoded_body.get('patient_id')

        update_data = {
            'patient_id': patient_id,
            'antibiotic_prior_1': decoded_body.get('antibiotic_prior_1'),
            'route_prior_1': decoded_body.get('route_prior_1'),
            'duration_prior_1': decoded_body.get('duration_prior_1'),
            'doses_prior_1': decoded_body.get('doses_prior_1'),
            'antibiotic_prior_2': decoded_body.get('antibiotic_prior_2'),
            'route_prior_2': decoded_body.get('route_prior_2'),
            'duration_prior_2': decoded_body.get('duration_prior_2'),
            'doses_prior_2': decoded_body.get('doses_prior_2'),
            'antibiotic_prior_3': decoded_body.get('antibiotic_prior_3'),
            'route_prior_3': decoded_body.get('route_prior_3'),
            'duration_prior_3' : decoded_body.get('duration_prior_3'),
            'doses_prior_3': decoded_body.get('doses_prior_3'),
            'antibiotic_pre_1': decoded_body.get('antibiotic_pre_1'),
            'route_pre_1': decoded_body.get('route_pre_1'),
            'duration_pre_1': decoded_body.get('duration_pre_1'),
            'doses_pre_1': decoded_body.get('doses_pre_1'),
            'antibiotic_pre_2': decoded_body.get('antibiotic_pre_2'),
            'route_pre_2': decoded_body.get('route_pre_2'),
            'duration_pre_2': decoded_body.get('duration_pre_2'),
            'doses_pre_2': decoded_body.get('doses_pre_2'),
            'antibiotic_pre_3': decoded_body.get('antibiotic_pre_3'),
            'route_pre_3': decoded_body.get('route_pre_3'),
            'duration_pre_3': decoded_body.get('duration_pre_3'),
            'doses_pre_3': decoded_body.get('doses_pre_3'),
            'antibiotic_post_1': decoded_body.get('antibiotic_post_1'),
            'route_post_1': decoded_body.get('route_post_1'),
            'duration_post_1': decoded_body.get('duration_post_1'),
            'doses_post_1': decoded_body.get('doses_post_1'),
            'antibiotic_post_2': decoded_body.get('antibiotic_post_2'),
            'route_post_2': decoded_body.get('route_post_2'),
            'duration_post_2': decoded_body.get('duration_post_2'),
            'doses_post_2': decoded_body.get('doses_post_2'),
            'antibiotic_post_3': decoded_body.get('antibiotic_post_3'),
            'route_post_3': decoded_body.get('route_post_3'),
            'duration_post_3': decoded_body.get('duration_post_3'),
            'doses_post_3': decoded_body.get('doses_post_3'),
            'antibiotic_post_4': decoded_body.get('antibiotic_post_4'),
            'route_post_4': decoded_body.get('route_post_4'),
            'duration_post_4': decoded_body.get('duration_post_4'),
            'doses_post_4': decoded_body.get('doses_post_4'),
            'antibiotic_post_5': decoded_body.get('antibiotic_post_5'),
            'route_post_5': decoded_body.get('route_post_5'),
            'duration_post_5': decoded_body.get('duration_post_5'),
            'doses_post_5': decoded_body.get('doses_post_5'),
            'antibiotic_post_6': decoded_body.get('antibiotic_post_6'),
            'route_post_6': decoded_body.get('route_post_6'),
            'duration_post_6': decoded_body.get('duration_post_6'),
            'doses_post_6': decoded_body.get('doses_post_6'),
            'time_induction': decoded_body.get('time_induction'),
            'time_incision': decoded_body.get('time_incision'),
            'time_end_surgery': decoded_body.get('time_end_surgery')
        }
        log.info("update_data :%s" % update_data)

        if not patient_id:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "PATIENT ID is required"})

        patient_antibiotic_details_update = cls_nurse._update_patient_antibiotic_details(LOG_PREFIX, data=update_data)

        log.info(" UPDATE :%s" % patient_antibiotic_details_update)

        if patient_antibiotic_details_update:
            return JsonResponse(
                {"status": "SUCCESS", "statuscode": 200, "msg": "Patient Antibiotic Surveillance Details updated successfully!"})
        else:
            return JsonResponse(
                {"status": "FAILURE", "statuscode": 500, "msg": "Failed to update Patient Antibiotic Surveillance Details!"})
    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})


@csrf_exempt
@require_http_methods(["POST"])
def update_post_surgery_details(request, *args, **kwargs):
    EVENT = "UpdatePostOpDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_patient = SrDoctor()

    try:
        decoded_body = json.loads((request.body).decode())

        form = PostOpDayUpdateForm(decoded_body)
        if not form.is_valid():
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})
        patient_id = decoded_body.get('patient_id')

        update_data = {
            'patient_id': patient_id,
            'date_of_procedure': decoded_body.get('date_of_procedure'),
            'name_of_procedure': decoded_body.get('name_of_procedure'),
            'symptoms': decoded_body.get('symptoms', []),
        }

        log.info(f"{LOG_PREFIX} - Update data: {update_data}")

        patient_update_result = cls_patient._update_post_op_details(LOG_PREFIX, data=update_data)

        if patient_update_result:
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "Post-op details updated successfully!"})
        else:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Failed to update post-op details!"})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})


@csrf_exempt
@require_http_methods(["POST"])
def update_ssi_evaluation_details(request, *args, **kwargs):
    EVENT = "UpdateSSIEvaluationDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_nurse = SrDoctor()

    try:
        decoded_body = json.loads((request.body).decode())

        form = SSIEvaluationUpdateForm(decoded_body)
        if not form.is_valid():
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})

        patient_id = decoded_body.get('patient_id')
        if not patient_id:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "PATIENT ID is required"})

        update_data = {
            'patient_id': patient_id,
            'procedure_name': decoded_body.get('procedure_name'),
            'patient_name': decoded_body.get('patient_name'),
            'age': decoded_body.get('age'),
            'gender': decoded_body.get('gender'),
            'date_of_procedure': decoded_body.get('date_of_procedure'),
            'evaluation_fields': {},
        }

        for field in SSIEvaluationUpdateForm.dynamic_fields:
            choice_key = f"{field}_choice"
            remarks_key = f"{field}_remarks"

            update_data['evaluation_fields'][field] = {
                'choice': decoded_body.get(choice_key),
                'remarks': decoded_body.get(remarks_key),
            }

        log.info(f"{LOG_PREFIX} - Successfully extracted SSI evaluation update data: {update_data}")

        update_ssi_evaluation_details = cls_nurse._update_ssi_evaluation_details(LOG_PREFIX, data=update_data)

        if update_ssi_evaluation_details:
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "SSI evaluation details updated successfully!"})
        else:
            return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Failed to update SSI evaluation details!"})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})



@csrf_exempt
@require_http_methods(["POST"])
def update_event_details(request, *args, **kwargs):
    EVENT = "UpdateEventDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_nurse = SrDoctor()

    try:
        decoded_body = json.loads((request.body).decode())

        form = EventDetailUpdateForm(decoded_body)
        if not form.is_valid():
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})
        patient_id = decoded_body.get('patient_id')

        if not patient_id:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "PATIENT ID is required"})

        update_data = {
            'patient_id': patient_id,
            'specific_event': decoded_body.get('specific_event'),
            'organ_space_site': decoded_body.get('organ_space_site'),
            'detected': decoded_body.get('detected'),
            'sample_types': decoded_body.get('sample_types'),
            'site_of_sample_collection': decoded_body.get('site_of_sample_collection'),
            'secondary_bsi_contributed': decoded_body.get('secondary_bsi_contributed'),
        }
        log.info("update_data :%s" % update_data)

        patient_event_update = cls_nurse._update_event_details(LOG_PREFIX, data=update_data)

        log.info(" UPDATE :%s" % patient_event_update)

        if patient_event_update:
            return JsonResponse(
                {"status": "SUCCESS", "statuscode": 200, "msg": "Patient Event Details updated successfully!"})
        else:
            return JsonResponse(
                {"status": "FAILURE", "statuscode": 500, "msg": "Failed to update Patient Event Details!"})
    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})




#GETTT
@csrf_exempt
@require_http_methods(["GET"])
def get_patient_admin_details(request, *args, **kwargs):
    EVENT = "GetPatientAdminDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_register = SrDoctor()

    patient_id = request.GET.get('patient_id')

    if not patient_id:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"Missing patient_id"')
        return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

    try:
        patient_admin_details = cls_register._patient_admin_details(LOG_PREFIX, patient_id)

        if patient_admin_details:
            log.info(
                f'{LOG_PREFIX} - "Result":"Success", "PatientId":"{patient_id}", "PatientAdminDetails":{patient_admin_details}')
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "Patient admin details retrieved successfully", "data": patient_admin_details})
        else:
            log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"DataNotFound", "PatientId":"{patient_id}"')
            return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient admin details not found"})

    except Exception as e:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": f"Internal server error: {str(e)}"})


@csrf_exempt
@require_http_methods(["GET"])
def get_patient_microbiology_details(request, *args, **kwargs):
    EVENT = "GetPatientMicrobiologyDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_register = SrDoctor()

    patient_id = request.GET.get('patient_id')

    if not patient_id:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"Missing patient_id"')
        return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

    try:
        patient_microbiology_details = cls_register._patient_microbiology_details(LOG_PREFIX, patient_id)

        if patient_microbiology_details:
            log.info(
                f'{LOG_PREFIX} - "Result":"Success", "PatientId":"{patient_id}", "PatientMicrobiologyDetails":{patient_microbiology_details}')
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "Patient microbiology details retrieved successfully", "data": patient_microbiology_details})
        else:
            log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"DataNotFound", "PatientId":"{patient_id}"')
            return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient microbiology details not found"})

    except Exception as e:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": f"Internal server error: {str(e)}"})


@csrf_exempt
@require_http_methods(["GET"])
def get_patient_antibiotic_details(request, *args, **kwargs):
    EVENT = "GetPatientAntibioticSurveillanceDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_register = SrDoctor()

    patient_id = request.GET.get('patient_id')

    if not patient_id:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"Missing patient_id"')
        return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

    try:
        patient_antibiotic_surveillance_details = cls_register._patient_antibiotic_surveillance_details(LOG_PREFIX, patient_id)

        if patient_antibiotic_surveillance_details:
            log.info(
                f'{LOG_PREFIX} - "Result":"Success", "PatientId":"{patient_id}", "PatientAntibioticSurveillanceDetails":{patient_antibiotic_surveillance_details}')
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "Patient antibiotic surveillance details retrieved successfully", "data": patient_antibiotic_surveillance_details})
        else:
            log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"DataNotFound", "PatientId":"{patient_id}"')
            return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient antibiotic surveillance details not found"})

    except Exception as e:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": f"Internal server error: {str(e)}"})


@csrf_exempt
@require_http_methods(["GET"])
def get_patient_post_surgery_details(request, *args, **kwargs):
    EVENT = "GetPostSurgeryDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_register = SrDoctor()

    patient_id = request.GET.get('patient_id')

    if not patient_id:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"Missing patient_id"')
        return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

    try:
        patient_post_surgery_details = cls_register._patient_post_surgery_details(LOG_PREFIX, patient_id)

        if patient_post_surgery_details:
            log.info(
                f'{LOG_PREFIX} - "Result":"Success", "PatientId":"{patient_id}", "PatientPostSurgeryDetails":{patient_post_surgery_details}')
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "Patient post surgery details retrieved successfully", "data": patient_post_surgery_details})
        else:
            log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"DataNotFound", "PatientId":"{patient_id}"')
            return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient post surgery details not found"})

    except Exception as e:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": f"Internal server error: {str(e)}"})


@csrf_exempt
@require_http_methods(["GET"])
def get_patient_ssi_evaluation_details(request, *args, **kwargs):
    EVENT = "GetPatientSSIEvaluationDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_register = SrDoctor()

    patient_id = request.GET.get('patient_id')

    if not patient_id:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"Missing patient_id"')
        return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

    try:
        patient_ssi_evaluation_details = cls_register._patient_ssi_evaluation_details(LOG_PREFIX, patient_id)

        if patient_ssi_evaluation_details:
            log.info(
                f'{LOG_PREFIX} - "Result":"Success", "PatientId":"{patient_id}", "PatientSSIEvaluationDetails":{patient_ssi_evaluation_details}')
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "Patient SSI Evaluation details retrieved successfully", "data": patient_ssi_evaluation_details})
        else:
            log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"DataNotFound", "PatientId":"{patient_id}"')
            return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient SSI Evaluation details not found"})

    except Exception as e:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": f"Internal server error: {str(e)}"})


@csrf_exempt
@require_http_methods(["GET"])
def get_patient_event_details_details(request, *args, **kwargs):
    EVENT = "GetPatientEventDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_register = SrDoctor()

    patient_id = request.GET.get('patient_id')

    if not patient_id:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"Missing patient_id"')
        return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

    try:
        patient_event_details = cls_register._patient_event_details(LOG_PREFIX, patient_id)

        if patient_event_details:
            log.info(
                f'{LOG_PREFIX} - "Result":"Success", "PatientId":"{patient_id}", "PatientEventDetails":{patient_event_details}')
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "Patient Event details retrieved successfully", "data": patient_event_details})
        else:
            log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"DataNotFound", "PatientId":"{patient_id}"')
            return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient event details not found"})

    except Exception as e:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": f"Internal server error: {str(e)}"})


@csrf_exempt
@require_http_methods(["GET"])
def get_patient_list(request, *args, **kwargs):
    cls_patient = SrDoctor()
    EVENT = "GetPatientList"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'

    try:
        patient_list = cls_patient._get_patient_list(LOG_PREFIX, data={})
        log.info("Patient List: %s" % patient_list)

        if patient_list:
            patients = [{'patient_id': patient.get('patient_id'), 'patient_name': patient.get('patientName')}
                        for patient in patient_list]

            return JsonResponse({
                "status": "SUCCESS","statuscode": 200,"msg": "Patient list fetched successfully!","patients": patients})
        else:
            return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "No patients found"})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})

