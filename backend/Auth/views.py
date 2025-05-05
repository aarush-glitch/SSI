import json
import random

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helpers.jwthelper import JWToken

from .forms import OTPForm
from .background import OTP
from configuration import *
from Nurse.register_views import Nurse
from JrDoctor.register_views import JrDoctor
from SrDoctor.register_views import SrDoctor


@require_http_methods(["POST"])
@csrf_exempt
def otp(request):
    otp_handler = OTP()
    cls_jwt = JWToken()
    EVENT = "OTP"
    IP = client_ip(request)
    LOG_PREFIX = f'"EventName":"{EVENT}", "IP":"{IP}"'
    try:
        decoded_body = json.loads((request.body).decode())
        form = OTPForm(decoded_body)
        if not form.is_valid():
            log.info(f'{LOG_PREFIX}, "Action":"ValidateForm", "Result":"Failure", "Reason":"{form.errors}"')
            return JsonResponse({"status": "FAILURE", "statuscode": 400, "msg": form.errors})

        phone_number = decoded_body.get('phone_number')
        action = decoded_body['action']
        uri = request.build_absolute_uri()
        log.info("Requested URL : %s" %uri)

        if "nurse" in uri:
            user_type = "nurse"
            token_scope = TOKEN_SCOPE_NURSE
            prefix = "N_"
            cls_nurse = Nurse()
        elif "jrdoctor" in uri:
            user_type = "jrdoctor"
            token_scope = TOKEN_SCOPE_JR_DOCTOR
            prefix = "J_"
            cls_nurse = JrDoctor()
        elif "srdoctor" in uri:
            user_type = "srdoctor"
            token_scope = TOKEN_SCOPE_SR_DOCTOR
            prefix = "S_"
            cls_nurse = SrDoctor()
        else:
            user_type = "unknown"
            token_scope = ''

        print(f'URI: {uri}, UserType: {user_type}')
        print(uri)
        log.info("Modified URL : %s" %user_type)


        if action == 'generate':
            response = otp_handler.generate(LOG_PREFIX, phone_number, user_type)
            log.info(f'{LOG_PREFIX}, "Action":"GenerateOTP", "Result":"{response}"')
            if response:
                log.info(f'{LOG_PREFIX}, "Action":"GenerateOTP", "MobileNo":"{phone_number}", "UserType":"{user_type}" ,"Result":"Success"')
                return JsonResponse(
                    {"status": "SUCCESS", "statuscode": 200, "msg": "OTP Sent successfully!"})
            log.info(f'{LOG_PREFIX}, "Action":"GenerateOTP", "MobileNo":"{phone_number}","UserType":"{user_type}", "Result":"Failure", "Reason":"InternalServerError"')

        elif action == 'verify':
            otp_code = decoded_body.get('otp')
            v_status, v_response = otp_handler.verify(LOG_PREFIX, phone_number, otp_code, user_type)
            if v_status:
                employee_id = ''.join(random.choices('0123456789ABCDEF', k=14))  # Generate 14-bit random ID
                employee_id = prefix + employee_id
                profile_status, profile_data = cls_nurse._find(LOG_PREFIX, phone_number)
                if profile_status:
                    # user exists in the collection profile_user
                    token_payload = {
                        'contact': profile_data['phone_number'],
                        'employee_id': employee_id,
                        'name': profile_data.get('name', ''),
                        'scope': token_scope,
                    }
                    token_status, token_res = cls_jwt._generate('access', token_payload)
                    refresh_token_status, refresh_token_res = cls_jwt._generate('refresh', token_payload)
                    if token_status and refresh_token_status:
                        log.info(f'{LOG_PREFIX}, "Action":"GenerateOTP", "Result":"Success"')
                        return JsonResponse({
                            "status": "SUCCESS",
                            "statuscode": 200,
                            "msg": "User details found",
                            "access_token": token_res,
                            "refresh_token": refresh_token_res,
                        })
                    log.info(f'{LOG_PREFIX}, "Action":"GenerateOTP", "Result":"Failure", "Reason":"TokenCreationFailed"')
                else:
                    if token_scope == TOKEN_SCOPE_NURSE:

                        data = {
                            'phone_number': phone_number,
                            'employee_id': employee_id
                        }

                        add_result = cls_nurse._add_nurse(LOG_PREFIX, data)
                        log.info("NURSE.....")


                    elif token_scope == TOKEN_SCOPE_JR_DOCTOR:
                        data = {
                            'phone_number': phone_number,
                            'employee_id': employee_id,
                        }
                        add_result = cls_nurse._add_jr_doctor(LOG_PREFIX, data)
                        log.info("JUNIOR DOCTOR.....")

                    else:
                        data = {
                            'phone_number': phone_number,
                            'employee_id': employee_id,
                        }
                        add_result = cls_nurse._add_sr_doctor(LOG_PREFIX, data)
                        log.info("SENIOR DOCTOR.....")

                    if not add_result:
                        log.info(
                            f'{LOG_PREFIX}, "Action":"VerifyOTP", "Result":"Failure", "Reason":"UserProfileCreationFailed"')
                    token_payload = {
                        'contact': phone_number,
                        'employee_id': employee_id,
                        'name': '',
                        'scope': token_scope,
                    }
                    token_status, token_res = cls_jwt._generate('access', token_payload)
                    refresh_token_status, refresh_token_res = cls_jwt._generate('refresh', token_payload)
                    if token_status and refresh_token_status:
                        log.info(f'{LOG_PREFIX}, "Action":"VerifyOTP", "Result":"Success"')
                        return JsonResponse({
                            "status": "SUCCESS",
                            "statuscode": 200,
                            "msg": "User details found",
                            "access_token": token_res,
                            "refresh_token": refresh_token_res,
                        })
                    log.info(
                        f'{LOG_PREFIX}, "Action":"VerifyOTP", "Result":"Failure", "Reason":"TokenCreationFailed"')
            elif v_response:
                log.info(
                    f'{LOG_PREFIX}, "Action":"VerifyOTP", "Result":"Failure", "Reason":"{v_response}"')
                return JsonResponse({
                    "status": "FAILURE",
                    "statuscode": 400,
                    "msg": v_response
                })
            log.info(f'{LOG_PREFIX}, "Action":"VerifyOTP", "MobileNo":"{phone_number}","UserType":"{user_type}", "Result":"Failure", "Reason":"InternalServerError"')

        elif action == 'resend':
            response = otp_handler.resend(LOG_PREFIX, phone_number, user_type)
            if response:
                log.info(f'{LOG_PREFIX}, "Action":"ResendOTP", "Result":"Success"')
                return JsonResponse(
                    {"status": "SUCCESS", "statuscode": 200, "msg": "OTP resent successfully!"})
            log.info(f'{LOG_PREFIX}, "Action":"ResendOTP", "MobileNo":"{phone_number}","UserType":"{user_type}", "Result":"Failure", "Reason":"InternalServerError"')

        return JsonResponse({
            "status": "FAILURE",
            "statuscode": 500,
            "msg": 'Internal Server Error'
        })
    except Exception as e:
        log.error(f'{LOG_PREFIX}, "Result":"Failure", "Reason":"{e}"')
        return JsonResponse({"status": "FAILURE", "statuscode": 500, "msg": 'Internal Server Error'})

