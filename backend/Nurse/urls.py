from django.urls import path
from .views import *
from Auth import views as authviews
from reports.views import *

urlpatterns = [
    path('otp/', authviews.otp, name='OTP'),
    path('update/', update_nurse_details, name='update_nurse_details'),
    path('register/', add_nurse_details, name='add_nurse_details'),
    path('patient_administration_details/add/', add_patient_administration_details, name='add_patient_administration_details'),
    path('patient_microbiology_details/add/', add_microbiology_details, name='add_microbiology_details'),
    path('patient_antibiotic_surveillance/add/', add_antibiotic_surveillance, name='add_antibiotic_surveillance'),
    path('patient_post_surgery_details/add/', add_post_surgery_details, name='add_post_surgery_details'),
    path('patient_ssi_evaluation_details/add/', add_ssi_evaluation_details, name='add_ssi_evaluation_details'),
    path('patient_event_details/add/', add_event_details, name='add_event_details'),


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
