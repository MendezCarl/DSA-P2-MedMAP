import requests
from geopy.distance import geodesic
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.schemas.output import searchArea, hospitalInfo
from backend.utils.osmImplmentation import getLocationFromAddress

DATABASE_API_URL = "https://data.cms.gov/data-api/v1/dataset/8ba0f9b4-9493-4aa0-9f82-44ea9468d1b5/data"

#checks if service is true
def isTrue(v):
    if v is None:
        return False
    s = str(v).strip().upper()
    return s in {"Y", "1", "TRUE", "T", "YES"}

#checks for service code
def hasCode(v):
    if v is None:
        return False
    s = str(v).strip().upper()
    return s not in {"", "0", "N", "NO"}

# map: (acroynm, full phrase)
SERVICE_FLAG_MAP = {
    # Mental/Behavioral
    "MENTL_HLTH_OFSITE_RSDNT_SW": "Mental Health (Offsite for Residents)",
    "MENTL_HLTH_ONST_NRSDNT_SW":  "Mental Health (Onsite for Nonresidents)",
    "MENTL_HLTH_ONST_RSDNT_SW":   "Mental Health (Onsite for Residents)",
    "PSYCH_UNIT_SW":              "Psychiatric Unit",

    # Rehab / Therapy
    "REHAB_UNIT_SW":              "Rehabilitation Unit",
    "THRPTC_RCRTNL_ONST_RSDNT_SW":"Therapeutic Recreation (Onsite – Residents)",
    "THRPTC_RCRTNL_ONST_NRSDNT_SW":"Therapeutic Recreation (Onsite – Nonresidents)",
    "THRPTC_RCRTNL_OFSITE_RSDNT_SW":"Therapeutic Recreation (Offsite – Residents)",

    # Dialysis
    "HMDLYS_SRVC_SW":             "Hemodialysis",
    "PRTNL_DLYS_SRVC_SW":         "Peritoneal Dialysis",

    # Emergency/Critical Access indicators
    "FREESTNDNG_ASC_SW":          "Freestanding Ambulatory Surgery Center",
    "CAH_PSYCH_DPU_SW":           "CAH Psychiatric DPU",
    "CAH_REHAB_DPU_SW":           "CAH Rehabilitation DPU",
    "CAH_SB_SW":                  "Critical Access Swing Bed",

    # Facility/Operational
    "HOSP_BSD_SW":                "Hospital-Based Facility",
    "INCNTR_NCTRNL_SRVC_SW":      "In-Center Nocturnal Dialysis",
    "MLT_OWND_FAC_ORG_SW":        "Multi-owned Facility",
    "MEET_1861_SW":               "Meets SSA §1861",
    "ORGNZ_FMLY_MBR_GRP_SW":      "Family Member Organization",
    "ORGNZ_RSDNT_GRP_SW":         "Resident Organization",
    "EXPRMT_RSRCH_CNDCTD_SW":     "Experimental Research Conducted",
    "FED_FUNDD_FQHC_SW":          "Federally Funded FQHC",

    # Staffing/Arrangement flags
    "NRSNG_SRVC_EMPLEE_SW":       "Nursing Service (Employee)",
    "NRSNG_SRVC_CNTRCTR_SW":      "Nursing Service (Contractor)",
    "NRSNG_SRVC_ARNGMT_SW":       "Nursing Service (Arrangement)",
    "ORTHTC_PRSTHTC_EMPLEE_SW":   "Orthotics/Prosthetics (Employee)",
    "ORTHTC_PRSTHTC_CNTRCTR_SW":  "Orthotics/Prosthetics (Contractor)",
    "ORTHTC_PRSTHTC_ARNGMT_SW":   "Orthotics/Prosthetics (Arrangement)",
    "OT_EMPLEE_SW":               "Occupational Therapy (Employee)",
    "OT_CNTRCTR_SW":              "Occupational Therapy (Contractor)",
    "OT_ARNGMT_SW":               "Occupational Therapy (Arrangement)",
    "PHYSN_EMPLEE_SW":            "Physician Services (Employee)",
    "PHYSN_CNTRCTR_SW":           "Physician Services (Contractor)",
    "PHYSN_ARNGMT_SW":            "Physician Services (Arrangement)",
    "PSYCHLGCL_EMPLEE_SW":        "Psychology (Employee)",
    "PSYCHLGCL_CNTRCTR_SW":       "Psychology (Contractor)",
    "PSYCHLGCL_ARNGMT_SW":        "Psychology (Arrangement)",
    "PT_EMPLEE_SW":               "Physical Therapy (Employee)",
    "PT_CNTRCTR_SW":              "Physical Therapy (Contractor)",
    "PT_ARNGMT_SW":               "Physical Therapy (Arrangement)",
    "RSPRTRY_CARE_EMPLEE_SW":     "Respiratory Care (Employee)",
    "RSPRTRY_CARE_CNTRCTR_SW":    "Respiratory Care (Contractor)",
    "RSPRTRY_CARE_ARNGMT_SW":     "Respiratory Care (Arrangement)",
    "SCL_EMPLEE_SW":              "Social Work (Employee)",
    "SCL_CNTRCTR_SW":             "Social Work (Contractor)",
    "SCL_ARNGMT_SW":              "Social Work (Arrangement)",
    "SPCH_PTHLGY_EMPLEE_SW":      "Speech Pathology (Employee)",
    "SPCH_PTHLGY_CNTRCTR_SW":     "Speech Pathology (Contractor)",
    "SPCH_PTHLGY_ARNGMT_SW":      "Speech Pathology (Arrangement)",

    # Home training support flags
    "SP_HOME_TRNG_SPRT_HD_SW":    "Home Training Support – Hemodialysis",
    "SP_HOME_TRNG_SPRT_PD_SW":    "Home Training Support – Peritoneal Dialysis",
}

# service field codes
SERVICE_CODE_MAP = {
    # Emergency / Critical Care / Units
    "DCTD_ER_SRVC_CD":            "Dedicated Emergency Department",
    "CRNRY_CARE_UNIT_SRVC_CD":    "Coronary Care Unit",
    "ICU_SRVC_CD":                "Intensive Care Unit",
    "SRGCL_ICU_SRVC_CD":          "Surgical ICU",
    "SHRT_TERM_IP_SRVC_CD":       "Short-Term Inpatient Care",

    # Surgery & Procedures
    "OPEN_HRT_SRGRY_SRVC_CD":     "Open Heart Surgery",
    "OP_SRGRY_UNIT_SRVC_CD":      "Outpatient Surgery Unit",
    "OPRTG_ROOM_SRVC_CD":         "Operating Room Services",
    "IP_SRGCL_SRVC_CD":           "Inpatient Surgical Services",
    "OPTHLMC_SRGY_SRVC_CD":       "Ophthalmic Surgery",
    "ORTHPDC_SRGY_SRVC_CD":       "Orthopedic Surgery",
    "RCNSTRCTN_SRGY_SRVC_CD":     "Reconstructive Surgery",
    "BURN_CARE_UNIT_SRVC_CD":     "Burn Care Unit",
    "CRDC_CTHRTZTN_LAB_SRVC_CD":  "Cardiac Catheterization Lab",

    # Imaging & Diagnostics
    "CT_SCAN_SRVC_CD":            "CT Scan",
    "MGNTC_RSNC_IMG_SRVC_CD":     "MRI",
    "NUCLR_MDCN_SRVC_CD":         "Nuclear Medicine",
    "PET_SCAN_SRVC_CD":           "PET Scan",
    "DGNSTC_RDLGY_SRVC_CD":       "Diagnostic Radiology",
    "THRPTC_RDLGY_SRVC_CD":       "Therapeutic Radiology",
    "XTRCRPRL_SHCK_LTHTRPTR_SRVC_CD": "Extracorporeal Shock Wave Lithotripsy",

    # Clinics / General
    "CL_SRVC_CD":                 "Clinic / Outpatient Services",
    "OP_SRVC_CD":                 "Outpatient Services",
    "OB_SRVC_CD":                 "Obstetrics",
    "NRSNG_SRVC_CD":              "Nursing Services",
    "MDCL_SCL_SRVC_CD":           "Medical Social Services",
    "MDCL_SUPLY_SRVC_CD":         "Medical Supplies",
    "PSYCH_SRVC_CD":              "Psychiatric Services",
    "OP_REHAB_SRVC_CD":           "Outpatient Rehabilitation",
    "CARF_IP_REHAB_SRVC_CD":      "Inpatient Rehabilitation (CARF)",
    "RDLGY_SRVC_CD":              "Radiology",
    "LAB_SRVC_CD":                "Laboratory",
    "PHRMCY_SRVC_CD":             "Pharmacy",
    "VCTNL_GDNC_SRVC_CD":         "Vocational Guidance",

    # Other specialty units
    "NEONTL_ICU_SRVC_CD":         "Neonatal ICU",
    "NEONTL_NRSRY_SRVC_CD":       "Neonatal Nursery",
    "NRSRGCL_SRVC_CD":            "Neurosurgical Services",
    "ORGN_TRNSPLNT_SRVC_CD":      "Organ Transplant Center",
    "MDCR_TRNSPLNT_CNTR_SRVC_CD": "Medicare Transplant Center",
    "SHCK_TRMA_SRVC_CD":          "Shock/Trauma Services",
    "SPCH_THRPY_SRVC_CD":         "Speech Therapy",
    "PT_SRVC_CD":                 "Physical Therapy",
    "OT_SRVC_CD":                 "Occupational Therapy",
    "DNTL_SRVC_CD":               "Dental Services",
    "OPTMTRC_SRVC_CD":            "Optometric Services",
}

def getMedicalFacilities(area: searchArea) -> list[hospitalInfo]:
    try:
        params ={
            'limit': 100000,
            'offset': 0
        }

        if area.city:
            params['filter[city]'] = area.city

        response = requests.get(DATABASE_API_URL, params=params)
        response.raise_for_status()

        data = response.json()
        facilities = []

        #origin, user location
        fromLat = (area.minLatitude + area.maxLatitude) / 2
        fromLon = (area.minLongitude + area.maxLongitude) / 2
        fromCoord = (fromLat, fromLon)

        for facility in data:
            addressParts = []
            if facility.get('ST_ADR'):
                addressParts.append(facility['ST_ADR'])
            if facility.get('CITY_NAME'):
                addressParts.append(facility['CITY_NAME'])
            if facility.get('STATE_CD'):
                addressParts.append(facility['STATE_CD'])
            if facility.get('ZIP_CD'):
                addressParts.append(facility['ZIP_CD'])

            address = ', '.join(addressParts) if addressParts else None

            if not address:
                continue

            location = getLocationFromAddress(address)
            if location is None:
                continue
            
            lat = location.latitude
            lon = location.longitude

            if not (area.minLatitude <= lat <= area.maxLatitude and 
                    area.minLongitude <= lon <= area.maxLongitude):
                continue

            name = facility.get('FAC_NAME', 'Unknown Facility')

            functionality = []

            for col, label in SERVICE_FLAG_MAP.items():
                if isTrue(facility.get(col)):
                    functionality.append(label)

            for col, label in SERVICE_CODE_MAP.items():
                if hasCode(facility.get(col)):
                    functionality.append(label)

            op_rooms = facility.get("OPRTG_ROOM_CNT")
            if op_rooms not in (None, "", "0", 0):
                functionality.append(f"Operating Rooms: {op_rooms}")

            psy_beds = facility.get("PSYCH_UNIT_BED_CNT")
            if psy_beds not in (None, "", "0", 0) and isTrue(facility.get("PSYCH_UNIT_SW")):
                functionality.append(f"Psychiatric Beds: {psy_beds}")

            seen = set()
            functionality = [x for x in functionality if not (x in seen or seen.add(x))]

            #default Fallback
            if not functionality:
                functionality = ["General Medical Facility"]
            
            facilityCoord = (lat, lon)
            distance = geodesic(fromCoord, facilityCoord).meters

            facilities.append(hospitalInfo(
                name=name,
                address=address,
                functionality=functionality,
                longitude=lon,
                latitude=lat,
                distance=round(distance, 2)
            ))

        facilities.sort(key=lambda h: h.distance)
        print(f"There are {len(facilities)} facilities in the search area")
        return facilities
    
    except Exception as e:
        print(f"Not able to access database of facilities: {e}")
        return []