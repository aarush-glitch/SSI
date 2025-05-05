import json
import os
import pickle
from django.http import JsonResponse
from .forms import *
from .register_views import *
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from configuration import *
import math
from functools import wraps
from helpers.jwthelper import JWToken
import random
from .models import *
from django.http import FileResponse, JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import pandas as pd
from django.http import HttpResponse
import xlsxwriter
from SSIDetectionApp import settings


def verify_auth_token(func):
    cls_jwt = JWToken()

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            log.info("REQUEST HEADERS ::: %s" % request.headers)
            log.info("REQUEST META ::: %s" % request.META)
            authorization_token = request.headers.get('Authorization-Token')
            log.info("AuthorizationToken ::: %s" % authorization_token)
            if not authorization_token:
                return JsonResponse({"status": "FAILURE", "statuscode": 403, "msg": "Authorization token missing"})

            validate_success, token_data = cls_jwt._validate(authorization_token)
            log.info("Validate :: %s" % validate_success)
            log.info("ValidateData :: %s" % token_data)
            if not validate_success:
                error_msg = token_data.get('error', 'Unknown error')
                return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": f"Token validation failed: {error_msg}"})

            token_scope = token_data.get('scope')
            if token_scope not in (TOKEN_SCOPE_NURSE, TOKEN_SCOPE_SR_DOCTOR,TOKEN_SCOPE_JR_DOCTOR):
                return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Invalid Scope!"})

            phone_number = token_data.get('contact')
            employee_id = token_data.get('employee_id')

            kwargs['phone_number'] = phone_number
            kwargs['employee_id'] = employee_id

            log.info("KWARGS :: %s" % kwargs)

            return func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": f"Internal Server Error: {e}"})
    return wrapper


@csrf_exempt
@require_http_methods(["POST"])
@verify_auth_token
def update_nurse_details(request, *args, **kwargs):
    cls_register = Nurse()
    EVENT = "UpdateNurseDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    try:
        decoded_body = json.loads(request.body.decode())
        form = NurseUpdateForm(decoded_body)

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

        nurse_details_update = cls_register._update_nurse(LOG_PREFIX, data=update_data)

        log.info(f'{LOG_PREFIX}, "NurseUpdateResult": {nurse_details_update}')

        if nurse_details_update:
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "Nurse details updated successfully!"})
        else:
            return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Failed to update nurse details!"})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error"})




@csrf_exempt
@require_http_methods(["POST"])
# @verify_auth_token
def add_nurse_details(request, *args, **kwargs):
    EVENT = "AddNurseDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_nurse = Nurse()
    try:
        decoded_body = json.loads(request.body.decode())
        form = NurseForm(decoded_body)

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

        insert_nurse = cls_nurse._add_nurse(LOG_PREFIX, data=data_dict)
        log.info(f"INSERT NURSE DETAILS : {insert_nurse}")

        if insert_nurse:
            return JsonResponse(
                {"status": "SUCCESS", "statuscode": 200, "msg": "Nurse details added successfully!"}
            )
        else:
            return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Failed to add nurse details!"})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})


# @csrf_exempt
# @require_http_methods(["POST"])
# def add_patient_administration_details(request, *args, **kwargs):
#     EVENT = "AddPatientAdministration"
#     IP = client_ip(request)
#     LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
#     cls_nurse = Nurse()

#     try:
#         decoded_body = json.loads((request.body).decode())
#         form = PatientAdministrationForm(decoded_body)

#         if not form.is_valid():
#             return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})


#         patient_id = 'P_' + ''.join(random.choices('0123456789ABCDEF', k=16))

#         request.session['patient_id'] = patient_id
#         request.session['form1_completed'] = True
#         log.info("PATIENT ID :%s" % patient_id)
#         request.session.modified = True  # Mark session as modified to ensure saving

#         data_dict = {
#             'patient_id': patient_id,
#             'patientName': decoded_body.get('patientName'),
#             'age': decoded_body.get('age'),
#             'gender': decoded_body.get('gender'),
#             'patientOnSteroids': decoded_body.get('patientOnSteroids'),
#             'diabeticPatient': decoded_body.get('diabeticPatient'),
#             'weight': decoded_body.get('weight'),
#             'alcoholConsumption': decoded_body.get('alcoholConsumption'),
#             'tobaccoConsumption': decoded_body.get('tobaccoConsumption'),
#             'lengthOfSurgery': decoded_body.get('lengthOfSurgery'),
#             'dateOfAdmission': decoded_body.get('dateOfAdmission'),
#             'dateOfProcedure': decoded_body.get('dateOfProcedure'),
#             'admittingDepartment': decoded_body.get('admittingDepartment'),
#             'departmentPrimarySurgeon': decoded_body.get('departmentPrimarySurgeon'),
#             'procedureName': decoded_body.get('procedureName'),
#             'diagnosis': decoded_body.get('diagnosis'),
#             'procedureDoneBy': decoded_body.get('procedureDoneBy'),
#             'operationTheatre': decoded_body.get('operationTheatre'),
#             'outpatientProcedure': decoded_body.get('outpatientProcedure'),
#             'scenarioProcedure': decoded_body.get('scenarioProcedure'),
#             'woundClass': decoded_body.get('woundClass'),
#             'papGiven': decoded_body.get('papGiven'),
#             'antibioticsGiven': decoded_body.get('antibioticsGiven'),
#             'durationPAP': decoded_body.get('durationPAP'),
#             'ssiEventOccurred': decoded_body.get('ssiEventOccurred'),
#             'dateOfEvent': decoded_body.get('dateOfEvent')
#         }

#         insert_patient = cls_nurse._add_patient_administration_details(LOG_PREFIX, data=data_dict)
#         log.info("INSERT PATIENT ADMINISTRATION DETAILS :%s" % insert_patient)

#         if insert_patient:
#             return JsonResponse(
#                 {"status": "SUCCESS", "statuscode": 200, "msg": "Patient administration details added successfully!"})
#         else:
#             return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Failed to add patient admininstration details!"})

#     except Exception as e:
#         log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
#         return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})

@csrf_exempt
@require_http_methods(["POST"])
def add_patient_administration_details(request, *args, **kwargs):
    EVENT = "AddPatientAdministration"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_nurse = Nurse()

    try:
        decoded_body = json.loads((request.body).decode())
        form = PatientAdministrationForm(decoded_body)

        if not form.is_valid():
            log.error(f'{LOG_PREFIX}, "FormErrors":"{form.errors.as_json()}"')
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors.as_json()})

        patient_id = 'P_' + ''.join(random.choices('0123456789ABCDEF', k=16))

        request.session['patient_id'] = patient_id
        request.session['form1_completed'] = True
        log.info("PATIENT ID :%s" % patient_id)
        request.session.modified = True

        data_dict = {
            'patient_id': patient_id,
            'patientName': form.cleaned_data['patientName'],
            'age': form.cleaned_data['age'],
            'gender': form.cleaned_data['gender'],
            'patientOnSteroids': form.cleaned_data['patientOnSteroids'],
            'diabeticPatient': form.cleaned_data['diabeticPatient'],
            'weight': form.cleaned_data['weight'],
            'height': form.cleaned_data['height'],
            'bmi': form.cleaned_data['bmi'],
            'alcoholConsumption': form.cleaned_data['alcoholConsumption'],
            'tobaccoConsumption': form.cleaned_data['tobaccoConsumption'],
            'lengthOfSurgery': form.cleaned_data['lengthOfSurgery'],
            'dateOfAdmission': form.cleaned_data['dateOfAdmission'],
            'dateOfProcedure': form.cleaned_data['dateOfProcedure'],
            'admittingDepartment': form.cleaned_data['admittingDepartment'],
            'departmentPrimarySurgeon': form.cleaned_data['departmentPrimarySurgeon'],
            'procedureName': form.cleaned_data['procedureName'],
            'diagnosis': form.cleaned_data['diagnosis'],
            'procedureDoneBy': form.cleaned_data['procedureDoneBy'],
            'operationTheatre': form.cleaned_data['operationTheatre'],
            'outpatientProcedure': form.cleaned_data['outpatientProcedure'],
            'scenarioProcedure': form.cleaned_data['scenarioProcedure'],
            'woundClass': form.cleaned_data['woundClass'],
            'papGiven': form.cleaned_data['papGiven'],
            'antibioticsGiven': form.cleaned_data['antibioticsGiven'],
            'durationPAP': form.cleaned_data['durationPAP'],
            'ssiEventOccurred': form.cleaned_data['ssiEventOccurred'],
            'dateOfEvent': form.cleaned_data['dateOfEvent'],
        }

        insert_patient = cls_nurse._add_patient_administration_details(LOG_PREFIX, data=data_dict)
        log.info(f'{LOG_PREFIX}, "InsertResult":"{insert_patient}"')

        if insert_patient:
            return JsonResponse(
                {"status": "SUCCESS", "statuscode": 200, "msg": "Patient administration details added successfully!"})
        else:
            log.error(f'{LOG_PREFIX}, "InsertFailed":"No details added"')
            return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Failed to add patient administration details!"})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{str(e)}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": f"Internal Server Error: {str(e)}"})
##Without prediction
# @csrf_exempt
# @require_http_methods(["POST"])
# def add_microbiology_details(request, *args, **kwargs):
#     EVENT = "AddMicrobiologyDetails"
#     IP = client_ip(request)
#     LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
#     cls_nurse = Nurse()
#
#     try:
#         decoded_body = json.loads(request.body.decode())
#         form = MicrobiologyForm(decoded_body)
#
#         if not form.is_valid():
#             return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})
#
#         data_dict = {
#             'micro_organism': decoded_body.get('micro_organism'),
#             'antibiotic': []
#         }
#
#         for antibiotic in ANTIBIOTIC_CHOICES:
#             antibiotic_name = antibiotic[0]
#             antibiotic_key = antibiotic_name.lower().replace(' ', '_').replace('-', '_')  # Format key for lookup
#
#             mic_value = decoded_body.get(f"{antibiotic_key}_mic")
#             interpretation = decoded_body.get(f"{antibiotic_key}_interpretation")
#
#             log.info(f"Antibiotic: {antibiotic_name}, MIC: {mic_value}, Interpretation: {interpretation}")
#
#             if mic_value or interpretation:
#                 data_dict['antibiotic'].append({
#                     'name': antibiotic_name,
#                     'mic_value': mic_value if mic_value else None,
#                     'interpretation': interpretation if interpretation else None
#                 })
#
#         if not data_dict['antibiotic']:
#             data_dict['antibiotic'].append({
#                 'name': 'No antibiotic data provided',
#                 'mic_value': None,
#                 'interpretation': None
#             })
#
#         log.info(f"Data to insert into _add_microbiology_details: {data_dict}")
#
#         insert_microbiology_details = cls_nurse._add_microbiology_details(LOG_PREFIX, data=data_dict)
#         log.info(f"{LOG_PREFIX}, 'Result':'Inserted Microbiology Details', 'Details':{insert_microbiology_details}")
#
#         if insert_microbiology_details:
#             return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "Patient's Microbiology details added successfully!"})
#         else:
#             return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Failed to add patient's microbiology details!"})
#
#     except Exception as e:
#         log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
#         return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})
#

#with prediction and statements
# @csrf_exempt
# @require_http_methods(["POST"])
# def add_microbiology_details(request, *args, **kwargs):
#     EVENT = "AddMicrobiologyDetails"
#     IP = client_ip(request)
#     LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
#     cls_nurse = Nurse()
#
#     try:
#         patient_id = request.session.get('patient_id')
#         request.session['form2_completed'] = True
#         log.info("PATIENT ID :%s" % patient_id)
#         request.session.modified = True
#
#         if not patient_id:
#             return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Patient ID not found in session!"})
#
#         # Load the SSI_model machine learning model
#         model_path = os.path.join(os.path.dirname(__file__), 'ml_model', 'SSI_model.pkl')
#         with open(model_path, 'rb') as model_file:
#             model = pickle.load(model_file)
#
#         decoded_body = json.loads(request.body.decode())
#         form = MicrobiologyForm(decoded_body)
#
#         if not form.is_valid():
#             return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})
#
#         # Prepare initial data dictionary
#         data_dict = {
#             'patient_id': patient_id,
#             'micro_organism': decoded_body.get('micro_organism'),
#             'antibiotic': [],
#             'prediction': None  # Add prediction here
#         }
#
#         # Prepare features for the model
#         features = [
#             decoded_body.get('Ecoli', 1),
#             decoded_body.get('Cefuroxime', 0),
#             decoded_body.get('Cefuroxime_MIC', 68),
#             decoded_body.get('Resistant', 1),
#             decoded_body.get('Cefepime', 0),
#             decoded_body.get('Cefepime_MIC', 8),
#             decoded_body.get('Susceptibility_Dose_Dependent', 1),
#             decoded_body.get('Cefoperazone', 0),
#             decoded_body.get('Cefoperazone_MIC', 32),
#             decoded_body.get('Intermediate', 1),
#             decoded_body.get('Gentamicin', 0),
#             decoded_body.get('Gentamicin_MIC', 0.032),
#             decoded_body.get('Sensitive', 1)
#         ]
#
#         log.info(f"{LOG_PREFIX}, 'Step':'ML Prediction', 'Features':{features}")
#
#         # Make prediction with the SSI_model
#         prediction = model.predict([features])[0]
#         data_dict['prediction'] = prediction  # Store prediction in data_dict
#         log.info(f"{LOG_PREFIX}, 'Step':'ML Prediction', 'Prediction':{prediction}")
#
#         # Print additional information based on prediction
#         if prediction == 1:
#             print("CHANCES OF SSI DETECTED : ECOLI POSITIVE")
#             print("Cefuroxime: Resistant 30-50%")
#             print("Cefepime: Susceptibility 5-10%")
#             print("Sulbactum: Intermediate 20-30%")
#             print("Gentamicin: Sensitive 5-15%")
#             print("10-20% - SSI INVOLVEMENT : Suspected Surgery : ABDOMINAL/GASTROINTESTINAL")
#         else:
#             print("CHANCES OF SSI NOT DETECTED : ECOLI NEGATIVE")
#
#         # Process antibiotics
#         for antibiotic in ANTIBIOTIC_CHOICES:
#             antibiotic_name = antibiotic[0]
#             antibiotic_key = antibiotic_name.lower().replace(' ', '_').replace('-', '_')
#
#             mic_value = decoded_body.get(f"{antibiotic_key}_mic")
#             interpretation = decoded_body.get(f"{antibiotic_key}_interpretation")
#
#             log.info(f"Antibiotic: {antibiotic_name}, MIC: {mic_value}, Interpretation: {interpretation}")
#
#             if mic_value or interpretation:
#                 data_dict['antibiotic'].append({
#                     'name': antibiotic_name,
#                     'mic_value': mic_value if mic_value else None,
#                     'interpretation': interpretation if interpretation else None
#                 })
#
#         if not data_dict['antibiotic']:
#             data_dict['antibiotic'].append({
#                 'name': 'No antibiotic data provided',
#                 'mic_value': None,
#                 'interpretation': None
#             })
#
#         log.info(f"{LOG_PREFIX}, 'Step':'Data Preparation', 'DataDict':{data_dict}")
#
#         insert_microbiology_details = cls_nurse._add_microbiology_details(LOG_PREFIX, data=data_dict)
#         log.info(f"{LOG_PREFIX}, 'Result':'Inserted Microbiology Details', 'Details':{insert_microbiology_details}")
#
#         if insert_microbiology_details:
#             return JsonResponse(
#                 {"status": "SUCCESS", "statuscode": 200, "msg": "Patient's Microbiology details added successfully!"})
#         else:
#             return JsonResponse(
#                 {"status": "FAILURE", "statuscode": 500, "msg": "Failed to add patient's microbiology details!"})
#
#     except Exception as e:
#         log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
#         return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})

@csrf_exempt
@require_http_methods(["POST"])
def add_microbiology_details(request, *args, **kwargs):
    EVENT = "AddMicrobiologyDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_nurse = Nurse()

    try:
        patient_id = request.session.get('patient_id')
        request.session['form2_completed'] = True
        log.info("PATIENT ID :%s" % patient_id)
        request.session.modified = True

        if not patient_id:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Patient ID not found in session!"})

        # Loading the SSI_model machine learning model
        model_path = os.path.join(os.path.dirname(__file__), 'ml_model', 'SSI_model.pkl')
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)

        decoded_body = json.loads(request.body.decode())
        form = MicrobiologyForm(decoded_body)

        if not form.is_valid():
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})

        data_dict = {
            'patient_id': patient_id,
            'micro_organism': decoded_body.get('micro_organism'),
            'antibiotic': [],
            'prediction': None
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

        # Make prediction with the SSI_model
        prediction = model.predict([features])[0]
        data_dict['prediction'] = prediction  # Store prediction in data_dict
        log.info(f"{LOG_PREFIX}, 'Step':'ML Prediction', 'Prediction':{prediction}")

        # Process antibiotics
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

        # Insert microbiology details, including prediction
        insert_microbiology_details = cls_nurse._add_microbiology_details(LOG_PREFIX, data=data_dict)
        log.info(f"{LOG_PREFIX}, 'Result':'Inserted Microbiology Details', 'Details':{insert_microbiology_details}")

        if insert_microbiology_details:
            return JsonResponse(
                {"status": "SUCCESS", "statuscode": 200, "msg": "Patient's Microbiology details added successfully!"})
        else:
            return JsonResponse(
                {"status": "FAILURE", "statuscode": 500, "msg": "Failed to add patient's microbiology details!"})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})


@csrf_exempt
@require_http_methods(["POST"])
def add_antibiotic_surveillance(request, *args, **kwargs):
    EVENT = "AddAntibioticSurveillanceDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_nurse = Nurse()

    try:
        patient_id = request.session.get('patient_id')
        log.info("PATIENT ID :%s" % patient_id)
        request.session['form3_completed'] = True
        request.session.modified = True

        if not patient_id:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Patient ID not found in session!"})

        decoded_body = json.loads((request.body).decode())
        form = AntibioticSurveillanceForm(decoded_body)

        if not form.is_valid():
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})

        data_dict = {
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
            'doses_pre_2' : decoded_body.get('doses_pre_2'),
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
        insert_antibiotic_surveillance_details = cls_nurse._add_antibiotic_surveillance(LOG_PREFIX, data=data_dict)
        log.info("INSERT PATIENT ADMINISTRATION DETAILS :%s" % insert_antibiotic_surveillance_details)

        if insert_antibiotic_surveillance_details:
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "Patient's Antibiotic Surveillance details added successfully!"})
        else:
            return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Failed to add Patient's Antibiotic Surveillance details!"})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})


@csrf_exempt
@require_http_methods(["POST"])
def add_post_surgery_details(request, *args, **kwargs):
    EVENT = "AddPostSurgeryDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_nurse = Nurse()

    try:
        patient_id = request.session.get('patient_id')
        log.info("PATIENT ID :%s" % patient_id)
        request.session['form4_completed'] = True
        request.session.modified = True

        if not patient_id:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Patient ID not found in session!"})

        decoded_body = json.loads(request.body.decode())
        form = PostOpDayForm(decoded_body)

        if not form.is_valid():
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})

        data_dict = {
            'patient_id': patient_id,
            'date_of_procedure': decoded_body.get('date_of_procedure'),
            'name_of_procedure': decoded_body.get('name_of_procedure'),
            'symptoms': [],
        }

        symptoms = decoded_body.get('symptoms', [])
        for symptom_data in symptoms:
            if not isinstance(symptom_data, dict):
                log.error(f"{LOG_PREFIX} - Invalid symptom data structure: {symptom_data}")
                continue

            symptom_name = symptom_data.get('symptom', 'No symptom data provided')
            symptom_days = symptom_data.get('days', [])

            if not isinstance(symptom_days, list):
                log.error(f"{LOG_PREFIX} - Invalid days data structure for symptom: {symptom_name}")
                continue

            days_list = []
            for day_entry in symptom_days:
                if not isinstance(day_entry, dict):
                    log.error(f"{LOG_PREFIX} - Invalid day entry: {day_entry}")
                    continue

                day = day_entry.get('day')
                status = day_entry.get('status', 'Empty')

                if day and status != 'Empty':
                    days_list.append({'day': day, 'status': status})

            if days_list:
                data_dict['symptoms'].append({
                    'symptom': symptom_name,
                    'days': days_list
                })

        if not data_dict['symptoms']:
            log.info(f"{LOG_PREFIX} - No symptoms data provided. Adding placeholder entry.")
            data_dict['symptoms'].append({
                'symptom': 'No symptom data provided',
                'days': []
            })

        log.info(f"Data to insert into _add_post_op_details: {data_dict}")

        insert_post_op_details = cls_nurse._add_post_op_details(LOG_PREFIX, data=data_dict)

        if insert_post_op_details:
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "Post-surgery details added successfully!"})
        else:
            return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Failed to add post-surgery details!"})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})


@csrf_exempt
@require_http_methods(["POST"])
def add_ssi_evaluation_details(request, *args, **kwargs):
    EVENT = "AddSSIEvaluationDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_nurse = Nurse()

    try:
        patient_id = request.session.get('patient_id')
        log.info("PATIENT ID :%s" % patient_id)
        request.session['form5_completed'] = True
        request.session.modified = True

        if not patient_id:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Patient ID not found in session!"})

        decoded_body = json.loads(request.body.decode())
        form = SSIEvaluationForm(decoded_body)

        if not form.is_valid():
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})

        data_dict = {
            'patient_id': patient_id,
            'procedure_name': decoded_body.get('procedure_name'),
            'patient_name': decoded_body.get('patient_name'),
            'age': decoded_body.get('age'),
            'gender': decoded_body.get('gender'),
            'date_of_procedure': decoded_body.get('date_of_procedure'),
            'evaluation_fields': {},
        }

        # Extract evaluation fields and their remarks
        for field in SSIEvaluationForm.dynamic_fields:
            choice_key = f"{field}_choice"
            remarks_key = f"{field}_remarks"

            data_dict['evaluation_fields'][field] = {
                'choice': decoded_body.get(choice_key),
                'remarks': decoded_body.get(remarks_key),
            }

        log.info(f"{LOG_PREFIX} - Successfully extracted SSI evaluation data: {data_dict}")

        # Insert the extracted data into the system
        insert_ssi_evaluation_details = cls_nurse._add_ssi_evaluation(LOG_PREFIX, data=data_dict)

        if insert_ssi_evaluation_details:
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "SSI evaluation details added successfully!"})
        else:
            return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Failed to add SSI evaluation details!"})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})


@csrf_exempt
@require_http_methods(["POST"])
def add_event_details(request, *args, **kwargs):
    EVENT = "AddEventDetails"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_nurse = Nurse()

    try:
        patient_id = request.session.get('patient_id')
        if not patient_id:
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Patient ID not found in session!"})

        decoded_body = json.loads(request.body.decode())
        form = EventDetailForm(decoded_body)

        if not form.is_valid():
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})

        data_dict = {
            'patient_id': patient_id,
            'specific_event': decoded_body.get('specific_event'),
            'organ_space_site': decoded_body.get('organ_space_site'),
            'detected': decoded_body.get('detected'),
            'sample_types': decoded_body.get('sample_types'),
            'site_of_sample_collection': decoded_body.get('site_of_sample_collection'),
            'secondary_bsi_contributed': decoded_body.get('secondary_bsi_contributed'),
        }

        insert_event = cls_nurse._add_event_details(LOG_PREFIX, data=data_dict)
        if not insert_event:
            return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Failed to add event details!"})

        request.session['form6_completed'] = True
        request.session.modified = True

        if all_forms_completed(request.session):
            request.session.flush()
            return JsonResponse({"status": "SUCCESS", "statuscode": 200, "msg": "All forms submitted successfully!"})
        else:
            return JsonResponse({
                "status": "SUCCESS", "statuscode": 200, "msg": "Final form submitted. Waiting for other forms."})

    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error!"})


def all_forms_completed(session):
    required_flags = ['form1_completed', 'form2_completed', 'form3_completed',
                      'form4_completed', 'form5_completed', 'form6_completed']
    return all(session.get(flag, False) for flag in required_flags)

