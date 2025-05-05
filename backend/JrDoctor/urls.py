from django.urls import path
from .views import *
from Auth import views as authviews
from reports.views import *

urlpatterns = [
    path('otp/', authviews.otp, name='OTP'),
    path('update/', update_jr_doctor_details, name='update_jr_doctor_details'),
    path('register/', add_jrDoctor_details, name='add_jrDoctor_details'),
    path('patient_administration_details/update/', update_patient_admin_details, name='update_patient_admin_details'),
    path('patient_microbiology_details/update/', update_microbiology_details, name='update_microbiology_details'),
    path('patient_antibiotic_surveillance/update/', update_antibiotic_details, name='update_antibiotic_details'),
    path('patient_post_surgery_details/update/', update_post_surgery_details, name='update_post_surgery_details'),
    path('patient_ssi_evaluation_details/update/', update_ssi_evaluation_details, name='update_ssi_evaluation_details'),
    path('patient_event_details/update/', update_event_details, name='update_event_details'),
    path('patient_administration_details/get/', get_patient_admin_details, name='get_patient_admin_details'),
    path('patient_microbiology_details/get/', get_patient_microbiology_details, name='get_patient_microbiology_details'),
    path('patient_antibiotic_surveillance_details/get/', get_patient_antibiotic_details, name='get_patient_antibiotic_details'),
    path('patient_post_surgery_details/get/', get_patient_post_surgery_details, name='get_patient_post_surgery_details'),
    path('patient_ssi_evaluation_details/get/', get_patient_ssi_evaluation_details, name='get_patient_ssi_evaluation_details'),
    path('patient_event_details_details/get/', get_patient_event_details_details, name='get_patient_event_details_details'),
    path('patient_list/', get_patient_list, name='get_patient_list'),

    path("patient_administration_details/get/pdf/", generate_patient_admin_pdf, name="generate_patient_admin_pdf"),
    path("patient_administration_details/get/excel/", generate_patient_admin_excel, name="generate_patient_admin_excel"),
    path("patient_microbiology_details/get/pdf/", generate_patient_microbiology_pdf, name="generate_patient_microbiology_pdf"),
    path("patient_microbiology_details/get/excel", generate_patient_microbiology_excel, name="generate_patient_microbiology_excel"),
    path("patient/antibiotic/pdf/", generate_patient_antibiotic_pdf, name="generate_patient_antibiotic_pdf"),
    path("patient/antibiotic/excel/", generate_patient_antibiotic_excel, name="generate_patient_antibiotic_excel"),
    path("patient/post_surgery/pdf/", generate_patient_post_surgery_pdf, name="generate_patient_post_surgery_pdf"),
    path("patient/post_surgery/excel/", generate_patient_post_surgery_excel, name="generate_patient_post_surgery_excel"),
    path("patient/ssi_evaluation/pdf/", generate_patient_ssi_evaluation_pdf, name="generate_patient_ssi_evaluation_pdf"),
    path("patient/ssi_evaluation/excel/", generate_patient_ssi_evaluation_excel, name="generate_patient_ssi_evaluation_excel"),
    path("patient/event/pdf/", generate_patient_event_pdf, name="generate_patient_event_pdf"),
    path("patient/event/excel/", generate_patient_event_excel, name="generate_patient_event_excel")
]
