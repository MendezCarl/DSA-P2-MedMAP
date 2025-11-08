export const SPECIALTIES = [
  "Cardiology",
  "Dermatology",
  "Endocrinology",
  "Family Medicine / Primary Care",
  "Gastroenterology",
  "General Surgery",
  "Hematology / Oncology",
  "Internal Medicine",
  "Nephrology",
  "Neurology",
  "OB/GYN",
  "Orthopedics",
  "Pediatrics",
  "Psychiatry / Behavioral Health",
  "Pulmonology",
  "Radiology",
  "Rheumatology",
  "Urology",
  "Allergy & Immunology",
  "ENT / Otolaryngology",
  "Pain Medicine",
  "Physical Medicine & Rehabilitation (PM&R)",
  "Sleep Medicine",
  "Infectious Disease"
] as const;

export type Specialty = (typeof SPECIALTIES)[number];

