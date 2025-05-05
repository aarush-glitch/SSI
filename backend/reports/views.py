import json
import os
import pickle
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from configuration import *
from django.http import FileResponse, JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import pandas as pd
from django.http import HttpResponse
import xlsxwriter
from SSIDetectionApp import settings
# GENERATE PDF
from Nurse.register_views import Nurse

@csrf_exempt
@require_http_methods(["GET"])
def generate_patient_admin_pdf(request):
    EVENT = "GeneratePatientAdminPDF"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_register = Nurse()

    patient_id = request.GET.get('patient_id')

    if not patient_id:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"Missing patient_id"')
        return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

    patient_data = cls_register._patient_admin_details(LOG_PREFIX, patient_id)

    if not patient_data:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"DataNotFound", "PatientId":"{patient_id}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient admin details not found"})

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    y_position = 750

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y_position, f"Patient Admin Details - {patient_id}")
    y_position -= 40

    p.setFont("Helvetica", 12)
    for key, value in patient_data.items():
        p.drawString(50, y_position, f"{key}: {value}")
        y_position -= 20

    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"patient_admin_{patient_id}.pdf")


@csrf_exempt
@require_http_methods(["GET"])
def generate_patient_microbiology_pdf(request):
    EVENT = "GeneratePatientMicrobiologyPDF"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_register = Nurse()

    patient_id = request.GET.get('patient_id')

    if not patient_id:
        return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

    patient_data = cls_register._patient_microbiology_details(LOG_PREFIX, patient_id)

    if not patient_data:
        return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient microbiology details not found"})

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    y_position = 750

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y_position, f"Patient Microbiology Details - {patient_id}")
    y_position -= 40

    p.setFont("Helvetica", 12)
    for key, value in patient_data.items():
        p.drawString(50, y_position, f"{key}: {value}")
        y_position -= 20

    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"patient_microbiology_{patient_id}.pdf")


@csrf_exempt
@require_http_methods(["GET"])
def generate_patient_antibiotic_pdf(request):
    EVENT = "GeneratePatientAntibioticPDF"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_register = Nurse()

    patient_id = request.GET.get('patient_id')

    if not patient_id:
        return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

    patient_data = cls_register._patient_antibiotic_surveillance_details(LOG_PREFIX, patient_id)

    if not patient_data:
        return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient antibiotic details not found"})

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    y_position = 750

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y_position, f"Patient Antibiotic Details - {patient_id}")
    y_position -= 40

    p.setFont("Helvetica", 12)
    for key, value in patient_data.items():
        p.drawString(50, y_position, f"{key}: {value}")
        y_position -= 20

    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"patient_antibiotic_{patient_id}.pdf")


@csrf_exempt
@require_http_methods(["GET"])
def generate_patient_post_surgery_pdf(request):
    EVENT = "GeneratePatientPostSurgeryPDF"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_register = Nurse()

    patient_id = request.GET.get('patient_id')

    if not patient_id:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"Missing patient_id"')
        return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

    patient_data = cls_register._patient_post_surgery_details(LOG_PREFIX, patient_id)

    if not patient_data:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"DataNotFound", "PatientId":"{patient_id}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient post surgery details not found"})

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    y_position = 750

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y_position, f"Patient Post Surgery Details - {patient_id}")
    y_position -= 40

    p.setFont("Helvetica", 12)
    for key, value in patient_data.items():
        p.drawString(50, y_position, f"{key}: {value}")
        y_position -= 20

    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"patient_post_surgery_{patient_id}.pdf")


@csrf_exempt
@require_http_methods(["GET"])
def generate_patient_ssi_evaluation_pdf(request):
    EVENT = "GeneratePatientSSIEvaluationPDF"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_register = Nurse()

    patient_id = request.GET.get('patient_id')

    if not patient_id:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"Missing patient_id"')
        return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

    patient_data = cls_register._patient_ssi_evaluation_details(LOG_PREFIX, patient_id)

    if not patient_data:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"DataNotFound", "PatientId":"{patient_id}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient SSI evaluation details not found"})

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    y_position = 750

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y_position, f"Patient SSI Evaluation Details - {patient_id}")
    y_position -= 40

    p.setFont("Helvetica", 12)
    for key, value in patient_data.items():
        p.drawString(50, y_position, f"{key}: {value}")
        y_position -= 20

    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"patient_ssi_evaluation_{patient_id}.pdf")


@csrf_exempt
@require_http_methods(["GET"])
def generate_patient_event_pdf(request):
    EVENT = "GeneratePatientEventPDF"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    cls_register = Nurse()

    patient_id = request.GET.get('patient_id')

    if not patient_id:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"Missing patient_id"')
        return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

    patient_data = cls_register._patient_event_details(LOG_PREFIX, patient_id)

    if not patient_data:
        log.error(f'{LOG_PREFIX} - "Result":"Failure", "Reason":"DataNotFound", "PatientId":"{patient_id}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient event details not found"})

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    y_position = 750

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y_position, f"Patient Event Details - {patient_id}")
    y_position -= 40

    p.setFont("Helvetica", 12)
    for key, value in patient_data.items():
        p.drawString(50, y_position, f"{key}: {value}")
        y_position -= 20

    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"patient_event_{patient_id}.pdf")


# GENERATE EXCEL


@csrf_exempt
@require_http_methods(["GET"])
def generate_patient_admin_excel(request):
    EVENT = "GeneratePatientAdminExcel"
    IP = request.META.get("REMOTE_ADDR", "")
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'

    log.info(f"{LOG_PREFIX} - Function called.")

    cls_register = Nurse()

    try:
        patient_id = request.GET.get("patient_id")
        log.info(f"{LOG_PREFIX} - Received patient_id: {patient_id}")

        if not patient_id:
            log.error(f"{LOG_PREFIX} - Missing patient_id in request.")
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

        patient_data = cls_register._patient_admin_details(LOG_PREFIX, patient_id)
        log.info(f"{LOG_PREFIX} - Retrieved patient_data: {patient_data}")

        if not patient_data:
            log.error(f"{LOG_PREFIX} - No patient admin details found for patient_id: {patient_id}")
            return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient admin details not found"})

        df = pd.DataFrame([patient_data])
        log.info(f"{LOG_PREFIX} - Dataframe created successfully.")

        file_dir = os.path.join(settings.MEDIA_ROOT, "patient_admin_details")
        os.makedirs(file_dir, exist_ok=True)

        file_path = os.path.join(file_dir, f"patient_admin_{patient_id}.xlsx")

        df.to_excel(file_path, index=False, sheet_name="Patient Admin Details", engine="xlsxwriter")
        log.info(f"{LOG_PREFIX} - Excel file saved successfully: {file_path}")

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f"patient_admin_{patient_id}.xlsx")

    except Exception as e:
        log.error(f"{LOG_PREFIX} - Exception occurred: {str(e)}", exc_info=True)
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error"})


@csrf_exempt
@require_http_methods(["GET"])
def generate_patient_microbiology_excel(request):
    EVENT = "GeneratePatientMicrobiologyExcel"
    IP = request.META.get("REMOTE_ADDR", "")
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'

    log.info(f"{LOG_PREFIX} - Function called.")

    cls_register = Nurse()

    try:
        patient_id = request.GET.get("patient_id")
        log.info(f"{LOG_PREFIX} - Received patient_id: {patient_id}")

        if not patient_id:
            log.error(f"{LOG_PREFIX} - Missing patient_id in request.")
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

        patient_data = cls_register._patient_microbiology_details(LOG_PREFIX, patient_id)
        log.info(f"{LOG_PREFIX} - Retrieved patient_data: {patient_data}")

        if not patient_data:
            log.error(f"{LOG_PREFIX} - No patient microbiology details found for patient_id: {patient_id}")
            return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient microbiology details not found"})

        df = pd.DataFrame([patient_data])
        log.info(f"{LOG_PREFIX} - Dataframe created successfully.")

        file_dir = os.path.join(settings.MEDIA_ROOT, "patient_microbiology_details")
        os.makedirs(file_dir, exist_ok=True)

        file_path = os.path.join(file_dir, f"patient_microbiology_{patient_id}.xlsx")

        df.to_excel(file_path, index=False, sheet_name="Microbiology Details", engine="xlsxwriter")
        log.info(f"{LOG_PREFIX} - Excel file saved successfully: {file_path}")

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f"patient_microbiology_{patient_id}.xlsx")

    except Exception as e:
        log.error(f"{LOG_PREFIX} - Exception occurred: {str(e)}", exc_info=True)
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error"})


@csrf_exempt
@require_http_methods(["GET"])
def generate_patient_antibiotic_excel(request):
    EVENT = "GeneratePatientAntibioticExcel"
    IP = request.META.get("REMOTE_ADDR", "")
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'

    log.info(f"{LOG_PREFIX} - Function called.")

    cls_register = Nurse()

    try:
        patient_id = request.GET.get("patient_id")
        log.info(f"{LOG_PREFIX} - Received patient_id: {patient_id}")

        if not patient_id:
            log.error(f"{LOG_PREFIX} - Missing patient_id in request.")
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

        patient_data = cls_register._patient_antibiotic_surveillance_details(LOG_PREFIX, patient_id)
        log.info(f"{LOG_PREFIX} - Retrieved patient_data: {patient_data}")

        if not patient_data:
            log.error(f"{LOG_PREFIX} - No patient antibiotic details found for patient_id: {patient_id}")
            return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient antibiotic details not found"})

        df = pd.DataFrame([patient_data])
        log.info(f"{LOG_PREFIX} - Dataframe created successfully.")

        file_dir = os.path.join(settings.MEDIA_ROOT, "patient_antibiotic_details")
        os.makedirs(file_dir, exist_ok=True)

        file_path = os.path.join(file_dir, f"patient_antibiotic_{patient_id}.xlsx")

        df.to_excel(file_path, index=False, sheet_name="Antibiotic Details", engine="xlsxwriter")
        log.info(f"{LOG_PREFIX} - Excel file saved successfully: {file_path}")

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f"patient_antibiotic_{patient_id}.xlsx")

    except Exception as e:
        log.error(f"{LOG_PREFIX} - Exception occurred: {str(e)}", exc_info=True)
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error"})


@csrf_exempt
@require_http_methods(["GET"])
def generate_patient_post_surgery_excel(request):
    EVENT = "GeneratePatientPostSurgeryExcel"
    IP = request.META.get("REMOTE_ADDR", "")
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'

    log.info(f"{LOG_PREFIX} - Function called.")

    cls_register = Nurse()

    try:
        patient_id = request.GET.get("patient_id")
        log.info(f"{LOG_PREFIX} - Received patient_id: {patient_id}")

        if not patient_id:
            log.error(f"{LOG_PREFIX} - Missing patient_id in request.")
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

        patient_data = cls_register._patient_post_surgery_details(LOG_PREFIX, patient_id)
        log.info(f"{LOG_PREFIX} - Retrieved patient_data: {patient_data}")

        if not patient_data:
            log.error(f"{LOG_PREFIX} - No patient post surgery details found for patient_id: {patient_id}")
            return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient post surgery details not found"})

        df = pd.DataFrame([patient_data])
        log.info(f"{LOG_PREFIX} - Dataframe created successfully.")

        file_dir = os.path.join(settings.MEDIA_ROOT, "patient_post_surgery_details")
        os.makedirs(file_dir, exist_ok=True)

        file_path = os.path.join(file_dir, f"patient_post_surgery_{patient_id}.xlsx")

        df.to_excel(file_path, index=False, sheet_name="Patient Post Surgery Details", engine="xlsxwriter")
        log.info(f"{LOG_PREFIX} - Excel file saved successfully: {file_path}")

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f"patient_post_surgery_{patient_id}.xlsx")

    except Exception as e:
        log.error(f"{LOG_PREFIX} - Exception occurred: {str(e)}", exc_info=True)
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error"})


@csrf_exempt
@require_http_methods(["GET"])
def generate_patient_ssi_evaluation_excel(request):
    EVENT = "GeneratePatientSSIEvaluationExcel"
    IP = request.META.get("REMOTE_ADDR", "")
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'

    log.info(f"{LOG_PREFIX} - Function called.")

    cls_register = Nurse()

    try:
        patient_id = request.GET.get("patient_id")
        log.info(f"{LOG_PREFIX} - Received patient_id: {patient_id}")

        if not patient_id:
            log.error(f"{LOG_PREFIX} - Missing patient_id in request.")
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

        patient_data = cls_register._patient_ssi_evaluation_details(LOG_PREFIX, patient_id)
        log.info(f"{LOG_PREFIX} - Retrieved patient_data: {patient_data}")

        if not patient_data:
            log.error(f"{LOG_PREFIX} - No patient ssi evaluation details found for patient_id: {patient_id}")
            return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient ssi evaluation details not found"})

        df = pd.DataFrame([patient_data])
        log.info(f"{LOG_PREFIX} - Dataframe created successfully.")

        file_dir = os.path.join(settings.MEDIA_ROOT, "patient_ssi_evaluation_details")
        os.makedirs(file_dir, exist_ok=True)

        file_path = os.path.join(file_dir, f"patient_ssi_evaluation_{patient_id}.xlsx")

        df.to_excel(file_path, index=False, sheet_name="Patient SSI Evaluation Details", engine="xlsxwriter")
        log.info(f"{LOG_PREFIX} - Excel file saved successfully: {file_path}")

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f"patient_ssi_evaluation_{patient_id}.xlsx")

    except Exception as e:
        log.error(f"{LOG_PREFIX} - Exception occurred: {str(e)}", exc_info=True)
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error"})


@csrf_exempt
@require_http_methods(["GET"])
def generate_patient_event_excel(request):
    EVENT = "GeneratePatientEventExcel"
    IP = request.META.get("REMOTE_ADDR", "")
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'

    log.info(f"{LOG_PREFIX} - Function called.")

    cls_register = Nurse()

    try:
        patient_id = request.GET.get("patient_id")
        log.info(f"{LOG_PREFIX} - Received patient_id: {patient_id}")

        if not patient_id:
            log.error(f"{LOG_PREFIX} - Missing patient_id in request.")
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": "Missing patient_id"})

        patient_data = cls_register._patient_event_details(LOG_PREFIX, patient_id)
        log.info(f"{LOG_PREFIX} - Retrieved patient_data: {patient_data}")

        if not patient_data:
            log.error(f"{LOG_PREFIX} - No patient event details found for patient_id: {patient_id}")
            return JsonResponse({"status": "FAILURE", "statuscode": 404, "msg": "Patient event details not found"})

        df = pd.DataFrame([patient_data])
        log.info(f"{LOG_PREFIX} - Dataframe created successfully.")

        file_dir = os.path.join(settings.MEDIA_ROOT, "patient_event_details")
        os.makedirs(file_dir, exist_ok=True)

        file_path = os.path.join(file_dir, f"patient_event_{patient_id}.xlsx")

        df.to_excel(file_path, index=False, sheet_name="Patient Event Details", engine="xlsxwriter")
        log.info(f"{LOG_PREFIX} - Excel file saved successfully: {file_path}")

        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f"patient_event_{patient_id}.xlsx")

    except Exception as e:
        log.error(f"{LOG_PREFIX} - Exception occurred: {str(e)}", exc_info=True)
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": "Internal Server Error"})

