from django.db.models import TextChoices


class StatusChoices(TextChoices):
    PENDING = "PENDING", "Pending"
    CONFIRMED = "CONFIRMED", "Confirmed"
    CANCELLED = "CANCELLED", "Cancelled"
    COMPLETED = "COMPLETED", "Completed"


class RoleChoices(TextChoices):
    USER = "USER", "User"
    ADMIN = "ADMIN", "Admin"
    DOCTOR = "DOCTOR", "Doctor"
    STAFF = "STAFF", "Staff"


class GenderChoices(TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"


class BloodGroupChoices(TextChoices):
    A_POSITIVE = "A+", "A+"
    A_NEGATIVE = "A-", "A-"
    B_POSITIVE = "B+", "B+"
    B_NEGATIVE = "B-", "B-"
    AB_POSITIVE = "AB+", "AB+"
    AB_NEGATIVE = "AB-", "AB-"
    O_POSITIVE = "O+", "O+"
    O_NEGATIVE = "O-", "O-"


class TestTypes(TextChoices):
    BLOOD_TEST = "BLOOD_TEST", "Blood Test"
    URINE_TEST = "URINE_TEST", "Urine Test"
    X_RAY = "X_RAY", "X-Ray"
    MRI = "MRI", "MRI"
    CT_SCAN = "CT_SCAN", "CT Scan"
    ULTRASOUND = "ULTRASOUND", "Ultrasound"
    ECG = "ECG", "ECG (Electrocardiogram)"
    ECHO = "ECHO", "Echocardiogram"
    BLOOD_PRESSURE = "BLOOD_PRESSURE", "Blood Pressure Test"
    LIVER_FUNCTION = "LIVER_FUNCTION", "Liver Function Test"
    KIDNEY_FUNCTION = "KIDNEY_FUNCTION", "Kidney Function Test"
    THYROID_TEST = "THYROID_TEST", "Thyroid Test"
    LIPID_PROFILE = "LIPID_PROFILE", "Lipid Profile"
    CBC = "CBC", "Complete Blood Count (CBC)"
    STOOL_TEST = "STOOL_TEST", "Stool Test"
    BIOPSY = "BIOPSY", "Biopsy"
    ALLERGY_TEST = "ALLERGY_TEST", "Allergy Test"
    HIV_TEST = "HIV_TEST", "HIV Test"
    COVID_19_TEST = "COVID_19_TEST", "COVID-19 Test"
    PULMONARY_FUNCTION = "PULMONARY_FUNCTION", "Pulmonary Function Test"
    EYE_TEST = "EYE_TEST", "Eye Test"
    DEXA_SCAN = "DEXA_SCAN", "DEXA Scan (Bone Density Test)"
    MAMMOGRAM = "MAMMOGRAM", "Mammogram"
    PAP_SMEAR = "PAP_SMEAR", "Pap Smear"
    GENETIC_TEST = "GENETIC_TEST", "Genetic Test"
    MICROBIOLOGY_TEST = "MICROBIOLOGY_TEST", "Microbiology Test"
    CARDIAC_STRESS_TEST = "CARDIAC_STRESS_TEST", "Cardiac Stress Test"
    HORMONE_TEST = "HORMONE_TEST", "Hormone Test"
    GASTROSCOPY = "GASTROSCOPY", "Gastroscopy"
    COLONOSCOPY = "COLONOSCOPY", "Colonoscopy"
    CYSTOSCOPY = "CYSTOSCOPY", "Cystoscopy"
    PET_SCAN = "PET_SCAN", "PET Scan"
