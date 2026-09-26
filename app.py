import re
from urllib.parse import quote

import pandas as pd
import requests
import streamlit as st


st.set_page_config(
    page_title="PharmaLens ",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ----------------------------
# UI styling
# ----------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: #f4f7fb;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
    }

    .hero {
        padding: 30px;
        border-radius: 24px;
        color: white;
        background: linear-gradient(135deg, #075985, #0f766e);
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.18);
        margin-bottom: 18px;
    }

    .hero h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 6px;
    }

    .hero p {
        color: #e0f2fe;
        font-size: 1.08rem;
        margin: 0;
    }

    .notice {
        background: #fff7ed;
        color: #7c2d12;
        border-left: 6px solid #f97316;
        border-radius: 12px;
        padding: 14px;
        margin: 12px 0;
    }

    .success-box {
        background: #ecfdf5;
        color: #064e3b;
        border-left: 6px solid #059669;
        border-radius: 12px;
        padding: 14px;
        margin: 12px 0;
    }

    div[data-testid="stMetric"] {
        background: white;
        border-radius: 15px;
        padding: 12px;
        box-shadow: 0 2px 12px rgba(15, 23, 42, 0.08);
    }

    div[data-testid="stExpander"] {
        border-radius: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ----------------------------
# 100-drug database
# ----------------------------

DRUGS = [
    {
        "name": "Paracetamol",
        "class": "Analgesic / Antipyretic",
        "forms": ["Tablet", "Capsule", "Syrup", "Suspension", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Pain and fever",
        "solubility": "Moderately soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture and excessive heat"
    },
    {
        "name": "Ibuprofen",
        "class": "NSAID",
        "forms": ["Tablet", "Capsule", "Suspension", "Gel"],
        "routes": ["Oral", "Topical"],
        "uses": "Pain, inflammation and fever",
        "solubility": "Practically insoluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture and light"
    },
    {
        "name": "Aspirin",
        "class": "NSAID / Antiplatelet",
        "forms": ["Tablet", "Chewable Tablet"],
        "routes": ["Oral"],
        "uses": "Pain, fever and antiplatelet therapy",
        "solubility": "Slightly soluble in water",
        "dose_type": "Medium dose",
        "stability": "Moisture sensitive; hydrolysis may occur"
    },
    {
        "name": "Naproxen",
        "class": "NSAID",
        "forms": ["Tablet", "Capsule", "Suspension"],
        "routes": ["Oral"],
        "uses": "Pain and inflammation",
        "solubility": "Practically insoluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Diclofenac",
        "class": "NSAID",
        "forms": ["Tablet", "Capsule", "Gel", "Injection", "Suppository"],
        "routes": ["Oral", "Topical", "Intramuscular", "Rectal"],
        "uses": "Pain and inflammation",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture and light"
    },
    {
        "name": "Ketoprofen",
        "class": "NSAID",
        "forms": ["Capsule", "Tablet", "Gel"],
        "routes": ["Oral", "Topical"],
        "uses": "Pain and inflammation",
        "solubility": "Practically insoluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from light"
    },
    {
        "name": "Amoxicillin",
        "class": "Penicillin Antibiotic",
        "forms": ["Tablet", "Capsule", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Bacterial infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "High dose",
        "stability": "Protect from moisture and excessive heat"
    },
    {
        "name": "Azithromycin",
        "class": "Macrolide Antibiotic",
        "forms": ["Tablet", "Capsule", "Oral Suspension", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Bacterial infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Clarithromycin",
        "class": "Macrolide Antibiotic",
        "forms": ["Tablet", "Extended-Release Tablet", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Bacterial infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Ciprofloxacin",
        "class": "Fluoroquinolone Antibiotic",
        "forms": ["Tablet", "Oral Suspension", "Eye Drops", "Injection"],
        "routes": ["Oral", "Ophthalmic", "Intravenous"],
        "uses": "Bacterial infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from light"
    },
    {
        "name": "Levofloxacin",
        "class": "Fluoroquinolone Antibiotic",
        "forms": ["Tablet", "Eye Drops", "Injection"],
        "routes": ["Oral", "Ophthalmic", "Intravenous"],
        "uses": "Bacterial infections",
        "solubility": "Soluble in acidic conditions",
        "dose_type": "Medium dose",
        "stability": "Protect from light"
    },
    {
        "name": "Moxifloxacin",
        "class": "Fluoroquinolone Antibiotic",
        "forms": ["Tablet", "Eye Drops", "Injection"],
        "routes": ["Oral", "Ophthalmic", "Intravenous"],
        "uses": "Bacterial infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from light"
    },
    {
        "name": "Doxycycline",
        "class": "Tetracycline Antibiotic",
        "forms": ["Tablet", "Capsule"],
        "routes": ["Oral"],
        "uses": "Bacterial infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low to medium dose",
        "stability": "Protect from moisture and light"
    },
    {
        "name": "Metronidazole",
        "class": "Antibacterial / Antiprotozoal",
        "forms": ["Tablet", "Suspension", "Gel", "Injection"],
        "routes": ["Oral", "Topical", "Intravenous"],
        "uses": "Anaerobic and protozoal infections",
        "solubility": "Sparingly soluble in water",
        "dose_type": "High dose",
        "stability": "Protect from light"
    },
    {
        "name": "Tinidazole",
        "class": "Antiprotozoal",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Protozoal and anaerobic infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "High dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Cefixime",
        "class": "Cephalosporin Antibiotic",
        "forms": ["Tablet", "Capsule", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Bacterial infections",
        "solubility": "Poorly soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Cephalexin",
        "class": "Cephalosporin Antibiotic",
        "forms": ["Capsule", "Tablet", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Bacterial infections",
        "solubility": "Soluble in water",
        "dose_type": "High dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Cefuroxime",
        "class": "Cephalosporin Antibiotic",
        "forms": ["Tablet", "Oral Suspension", "Injection"],
        "routes": ["Oral", "Intravenous", "Intramuscular"],
        "uses": "Bacterial infections",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Ceftriaxone",
        "class": "Cephalosporin Antibiotic",
        "forms": ["Injection"],
        "routes": ["Intravenous", "Intramuscular"],
        "uses": "Serious bacterial infections",
        "solubility": "Soluble in water",
        "dose_type": "High dose",
        "stability": "Sterile product; protect from light"
    },
    {
        "name": "Meropenem",
        "class": "Carbapenem Antibiotic",
        "forms": ["Injection"],
        "routes": ["Intravenous"],
        "uses": "Serious bacterial infections",
        "solubility": "Soluble depending on formulation",
        "dose_type": "High dose",
        "stability": "Sterile and temperature-controlled handling"
    },
    {
        "name": "Pantoprazole",
        "class": "Proton Pump Inhibitor",
        "forms": ["Delayed-Release Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Acid-related disorders",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Acid sensitive; enteric protection may be required"
    },
    {
        "name": "Omeprazole",
        "class": "Proton Pump Inhibitor",
        "forms": ["Delayed-Release Capsule", "Delayed-Release Tablet"],
        "routes": ["Oral"],
        "uses": "Acid-related disorders",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Acid and moisture sensitive"
    },
    {
        "name": "Esomeprazole",
        "class": "Proton Pump Inhibitor",
        "forms": ["Delayed-Release Tablet", "Delayed-Release Capsule", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Acid-related disorders",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Acid sensitive"
    },
    {
        "name": "Rabeprazole",
        "class": "Proton Pump Inhibitor",
        "forms": ["Delayed-Release Tablet"],
        "routes": ["Oral"],
        "uses": "Acid-related disorders",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Acid and moisture sensitive"
    },
    {
        "name": "Famotidine",
        "class": "H2-Receptor Antagonist",
        "forms": ["Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Acid-related disorders",
        "solubility": "Freely soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Ondansetron",
        "class": "Antiemetic",
        "forms": ["Tablet", "Orally Disintegrating Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Nausea and vomiting",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Domperidone",
        "class": "Gastroprokinetic / Antiemetic",
        "forms": ["Tablet", "Suspension"],
        "routes": ["Oral"],
        "uses": "Nausea and gastric motility disorders",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Metoclopramide",
        "class": "Antiemetic / Gastroprokinetic",
        "forms": ["Tablet", "Injection", "Oral Solution"],
        "routes": ["Oral", "Intravenous", "Intramuscular"],
        "uses": "Nausea and vomiting",
        "solubility": "Soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Loperamide",
        "class": "Antidiarrheal",
        "forms": ["Capsule", "Tablet", "Oral Solution"],
        "routes": ["Oral"],
        "uses": "Diarrhea",
        "solubility": "Practically insoluble in water",
        "dose_type": "Very low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Lactulose",
        "class": "Osmotic Laxative",
        "forms": ["Oral Solution", "Syrup"],
        "routes": ["Oral"],
        "uses": "Constipation and hepatic encephalopathy",
        "solubility": "Freely soluble in water",
        "dose_type": "High volume liquid dose",
        "stability": "Protect from excessive heat"
    },
    {
        "name": "Metformin",
        "class": "Biguanide Antidiabetic",
        "forms": ["Tablet", "Extended-Release Tablet"],
        "routes": ["Oral"],
        "uses": "Type 2 diabetes",
        "solubility": "Freely soluble in water",
        "dose_type": "High dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Glimepiride",
        "class": "Sulfonylurea Antidiabetic",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Type 2 diabetes",
        "solubility": "Practically insoluble in water",
        "dose_type": "Very low dose",
        "stability": "Protect from moisture and light"
    },
    {
        "name": "Gliclazide",
        "class": "Sulfonylurea Antidiabetic",
        "forms": ["Tablet", "Modified-Release Tablet"],
        "routes": ["Oral"],
        "uses": "Type 2 diabetes",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Sitagliptin",
        "class": "DPP-4 Inhibitor",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Type 2 diabetes",
        "solubility": "Soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Vildagliptin",
        "class": "DPP-4 Inhibitor",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Type 2 diabetes",
        "solubility": "Soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Dapagliflozin",
        "class": "SGLT2 Inhibitor",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Diabetes and selected cardiovascular or renal conditions",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Empagliflozin",
        "class": "SGLT2 Inhibitor",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Diabetes and selected cardiovascular or renal conditions",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Pioglitazone",
        "class": "Thiazolidinedione",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Type 2 diabetes",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Levothyroxine",
        "class": "Thyroid Hormone",
        "forms": ["Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Hypothyroidism",
        "solubility": "Very slightly soluble in water",
        "dose_type": "Very low dose",
        "stability": "Sensitive to light and moisture"
    },
    {
        "name": "Amlodipine",
        "class": "Calcium Channel Blocker",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Hypertension and angina",
        "solubility": "Slightly soluble in water",
        "dose_type": "Very low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Atenolol",
        "class": "Beta Blocker",
        "forms": ["Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Hypertension and cardiovascular conditions",
        "solubility": "Soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Metoprolol",
        "class": "Beta Blocker",
        "forms": ["Tablet", "Extended-Release Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Hypertension and cardiovascular conditions",
        "solubility": "Soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Losartan",
        "class": "Angiotensin Receptor Blocker",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Hypertension",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Telmisartan",
        "class": "Angiotensin Receptor Blocker",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Hypertension",
        "solubility": "Practically insoluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Valsartan",
        "class": "Angiotensin Receptor Blocker",
        "forms": ["Tablet", "Capsule"],
        "routes": ["Oral"],
        "uses": "Hypertension and cardiovascular conditions",
        "solubility": "Slightly soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Enalapril",
        "class": "ACE Inhibitor",
        "forms": ["Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Hypertension and heart failure",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Ramipril",
        "class": "ACE Inhibitor",
        "forms": ["Capsule", "Tablet"],
        "routes": ["Oral"],
        "uses": "Hypertension and cardiovascular conditions",
        "solubility": "Practically insoluble in water",
        "dose_type": "Very low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Furosemide",
        "class": "Loop Diuretic",
        "forms": ["Tablet", "Oral Solution", "Injection"],
        "routes": ["Oral", "Intravenous", "Intramuscular"],
        "uses": "Edema and hypertension",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low to medium dose",
        "stability": "Protect from light"
    },
    {
        "name": "Hydrochlorothiazide",
        "class": "Thiazide Diuretic",
        "forms": ["Tablet", "Capsule"],
        "routes": ["Oral"],
        "uses": "Hypertension and edema",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Spironolactone",
        "class": "Potassium-Sparing Diuretic",
        "forms": ["Tablet", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Edema and selected cardiovascular conditions",
        "solubility": "Practically insoluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Atorvastatin",
        "class": "Statin",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Dyslipidemia",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from light and moisture"
    },
    {
        "name": "Rosuvastatin",
        "class": "Statin",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Dyslipidemia",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Simvastatin",
        "class": "Statin",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Dyslipidemia",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Clopidogrel",
        "class": "Antiplatelet",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Prevention of thrombotic cardiovascular events",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Warfarin",
        "class": "Anticoagulant",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Prevention and treatment of thrombosis",
        "solubility": "Slightly soluble depending on salt form",
        "dose_type": "Very low dose",
        "stability": "Protect from light and moisture"
    },
    {
        "name": "Rivaroxaban",
        "class": "Direct Oral Anticoagulant",
        "forms": ["Tablet", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Prevention and treatment of thrombosis",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Apixaban",
        "class": "Direct Oral Anticoagulant",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Prevention and treatment of thrombosis",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Nitroglycerin",
        "class": "Nitrate",
        "forms": ["Sublingual Tablet", "Transdermal Patch", "Sublingual Spray"],
        "routes": ["Sublingual", "Transdermal"],
        "uses": "Angina",
        "solubility": "Soluble in organic solvents",
        "dose_type": "Very low dose",
        "stability": "Protect from light and heat"
    },
    {
        "name": "Salbutamol",
        "class": "Bronchodilator",
        "forms": ["Tablet", "Syrup", "Inhaler", "Nebulizer Solution"],
        "routes": ["Oral", "Inhalation"],
        "uses": "Bronchospasm and asthma",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Budesonide",
        "class": "Corticosteroid",
        "forms": ["Inhaler", "Nebulizer Suspension", "Capsule"],
        "routes": ["Inhalation", "Oral"],
        "uses": "Respiratory and inflammatory conditions",
        "solubility": "Practically insoluble in water",
        "dose_type": "Very low dose",
        "stability": "Protect from light and moisture"
    },
    {
        "name": "Beclomethasone",
        "class": "Corticosteroid",
        "forms": ["Inhaler", "Nasal Spray"],
        "routes": ["Inhalation", "Nasal"],
        "uses": "Respiratory and allergic conditions",
        "solubility": "Practically insoluble in water",
        "dose_type": "Very low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Montelukast",
        "class": "Leukotriene Receptor Antagonist",
        "forms": ["Tablet", "Chewable Tablet", "Granules"],
        "routes": ["Oral"],
        "uses": "Asthma and allergic rhinitis",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Theophylline",
        "class": "Methylxanthine Bronchodilator",
        "forms": ["Tablet", "Extended-Release Tablet", "Oral Solution"],
        "routes": ["Oral"],
        "uses": "Respiratory conditions",
        "solubility": "Slightly soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Cetirizine",
        "class": "Antihistamine",
        "forms": ["Tablet", "Syrup", "Oral Solution"],
        "routes": ["Oral"],
        "uses": "Allergic conditions",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Levocetirizine",
        "class": "Antihistamine",
        "forms": ["Tablet", "Syrup"],
        "routes": ["Oral"],
        "uses": "Allergic conditions",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Loratadine",
        "class": "Antihistamine",
        "forms": ["Tablet", "Syrup"],
        "routes": ["Oral"],
        "uses": "Allergic conditions",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Fexofenadine",
        "class": "Antihistamine",
        "forms": ["Tablet", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Allergic conditions",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Dextromethorphan",
        "class": "Antitussive",
        "forms": ["Syrup", "Lozenge", "Capsule"],
        "routes": ["Oral"],
        "uses": "Cough suppression",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Guaifenesin",
        "class": "Expectorant",
        "forms": ["Syrup", "Tablet", "Extended-Release Tablet"],
        "routes": ["Oral"],
        "uses": "Productive cough",
        "solubility": "Soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Ambroxol",
        "class": "Mucolytic",
        "forms": ["Tablet", "Syrup", "Oral Solution"],
        "routes": ["Oral"],
        "uses": "Mucus-related respiratory conditions",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Bromhexine",
        "class": "Mucolytic",
        "forms": ["Tablet", "Syrup", "Oral Solution"],
        "routes": ["Oral"],
        "uses": "Mucus-related respiratory conditions",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Mupirocin",
        "class": "Topical Antibiotic",
        "forms": ["Cream", "Ointment"],
        "routes": ["Topical"],
        "uses": "Local bacterial skin infections",
        "solubility": "Practically insoluble in water",
        "dose_type": "Topical",
        "stability": "Protect from heat"
    },
    {
        "name": "Clotrimazole",
        "class": "Antifungal",
        "forms": ["Cream", "Lotion", "Vaginal Tablet"],
        "routes": ["Topical", "Vaginal"],
        "uses": "Fungal infections",
        "solubility": "Practically insoluble in water",
        "dose_type": "Topical",
        "stability": "Protect from moisture"
    },
    {
        "name": "Ketoconazole",
        "class": "Antifungal",
        "forms": ["Cream", "Shampoo", "Tablet"],
        "routes": ["Topical", "Oral"],
        "uses": "Fungal infections",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Fluconazole",
        "class": "Triazole Antifungal",
        "forms": ["Tablet", "Capsule", "Oral Suspension", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Fungal infections",
        "solubility": "Soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Acyclovir",
        "class": "Antiviral",
        "forms": ["Tablet", "Cream", "Ointment", "Injection"],
        "routes": ["Oral", "Topical", "Intravenous"],
        "uses": "Herpes virus infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "Medium to high dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Oseltamivir",
        "class": "Antiviral",
        "forms": ["Capsule", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Influenza",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Hydrocortisone",
        "class": "Corticosteroid",
        "forms": ["Cream", "Ointment", "Tablet", "Injection"],
        "routes": ["Topical", "Oral", "Intravenous"],
        "uses": "Inflammatory and allergic conditions",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Betamethasone",
        "class": "Corticosteroid",
        "forms": ["Cream", "Ointment", "Tablet", "Injection"],
        "routes": ["Topical", "Oral", "Intramuscular"],
        "uses": "Inflammatory and allergic conditions",
        "solubility": "Practically insoluble in water",
        "dose_type": "Very low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Adapalene",
        "class": "Topical Retinoid",
        "forms": ["Gel", "Cream"],
        "routes": ["Topical"],
        "uses": "Acne",
        "solubility": "Practically insoluble in water",
        "dose_type": "Topical",
        "stability": "Protect from light"
    },
    {
        "name": "Tretinoin",
        "class": "Topical Retinoid",
        "forms": ["Cream", "Gel", "Lotion"],
        "routes": ["Topical"],
        "uses": "Acne and selected dermatological conditions",
        "solubility": "Practically insoluble in water",
        "dose_type": "Topical",
        "stability": "Protect from light"
    },
    {
        "name": "Povidone Iodine",
        "class": "Antiseptic",
        "forms": ["Solution", "Ointment", "Gargle"],
        "routes": ["Topical", "Oral cavity"],
        "uses": "Antisepsis",
        "solubility": "Soluble in water",
        "dose_type": "Topical",
        "stability": "Protect from light"
    },
    {
        "name": "Chlorhexidine",
        "class": "Antiseptic",
        "forms": ["Solution", "Gel", "Mouthwash"],
        "routes": ["Topical", "Oral cavity"],
        "uses": "Antisepsis and oral hygiene",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Topical",
        "stability": "Protect from light"
    },
    {
        "name": "Silver Sulfadiazine",
        "class": "Topical Antimicrobial",
        "forms": ["Cream"],
        "routes": ["Topical"],
        "uses": "Burn wound infection prevention",
        "solubility": "Practically insoluble in water",
        "dose_type": "Topical",
        "stability": "Protect from light"
    },
    {
        "name": "Calamine",
        "class": "Topical Protective",
        "forms": ["Lotion", "Cream"],
        "routes": ["Topical"],
        "uses": "Skin irritation and itching",
        "solubility": "Insoluble in water",
        "dose_type": "Topical",
        "stability": "Protect from contamination"
    },
    {
        "name": "Lidocaine",
        "class": "Local Anesthetic",
        "forms": ["Gel", "Cream", "Injection", "Spray"],
        "routes": ["Topical", "Local", "Intravenous"],
        "uses": "Local anesthesia",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Low to medium dose",
        "stability": "Protect from light"
    },
    {
        "name": "Bupivacaine",
        "class": "Local Anesthetic",
        "forms": ["Injection"],
        "routes": ["Local", "Epidural"],
        "uses": "Local and regional anesthesia",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Low dose",
        "stability": "Sterile product; protect from light"
    },
    {
        "name": "Tramadol",
        "class": "Opioid Analgesic",
        "forms": ["Tablet", "Capsule", "Oral Drops", "Injection"],
        "routes": ["Oral", "Intravenous", "Intramuscular"],
        "uses": "Moderate pain",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Gabapentin",
        "class": "Anticonvulsant / Neuropathic Pain Agent",
        "forms": ["Capsule", "Tablet", "Oral Solution"],
        "routes": ["Oral"],
        "uses": "Neuropathic pain and seizure disorders",
        "solubility": "Freely soluble in water",
        "dose_type": "Medium to high dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Pregabalin",
        "class": "Anticonvulsant / Neuropathic Pain Agent",
        "forms": ["Capsule", "Oral Solution"],
        "routes": ["Oral"],
        "uses": "Neuropathic pain and seizure disorders",
        "solubility": "Freely soluble in water",
        "dose_type": "Low to medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Ferrous Sulfate",
        "class": "Hematinic",
        "forms": ["Tablet", "Capsule", "Syrup"],
        "routes": ["Oral"],
        "uses": "Iron deficiency",
        "solubility": "Soluble depending on hydrate and medium",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture and oxidation"
    },
    {
        "name": "Folic Acid",
        "class": "Vitamin",
        "forms": ["Tablet", "Oral Solution"],
        "routes": ["Oral"],
        "uses": "Folate deficiency",
        "solubility": "Slightly soluble in water",
        "dose_type": "Very low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Calcium Carbonate",
        "class": "Mineral Supplement / Antacid",
        "forms": ["Tablet", "Chewable Tablet", "Suspension"],
        "routes": ["Oral"],
        "uses": "Calcium supplementation and antacid use",
        "solubility": "Practically insoluble in water",
        "dose_type": "High dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Vitamin D3",
        "class": "Vitamin",
        "forms": ["Tablet", "Capsule", "Oral Drops"],
        "routes": ["Oral"],
        "uses": "Vitamin D supplementation",
        "solubility": "Fat soluble",
        "dose_type": "Very low dose",
        "stability": "Protect from light and oxidation"
    },
    {
        "name": "Vitamin B12",
        "class": "Vitamin",
        "forms": ["Tablet", "Injection", "Oral Solution"],
        "routes": ["Oral", "Intramuscular"],
        "uses": "Vitamin B12 supplementation",
        "solubility": "Soluble depending on form",
        "dose_type": "Very low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Zinc Sulfate",
        "class": "Mineral Supplement",
        "forms": ["Tablet", "Capsule", "Syrup"],
        "routes": ["Oral"],
        "uses": "Zinc supplementation",
        "solubility": "Soluble in water",
        "dose_type": "Low to medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Potassium Chloride",
        "class": "Electrolyte",
        "forms": ["Extended-Release Tablet", "Oral Solution", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Potassium replacement",
        "solubility": "Freely soluble in water",
        "dose_type": "Medium to high dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Sodium Chloride",
        "class": "Electrolyte",
        "forms": ["Injection", "Nasal Solution", "Tablet"],
        "routes": ["Intravenous", "Nasal", "Oral"],
        "uses": "Electrolyte replacement and irrigation",
        "solubility": "Freely soluble in water",
        "dose_type": "Medium to high dose",
        "stability": "Protect from contamination"
    },
    {
        "name": "Insulin Human",
        "class": "Antidiabetic Hormone",
        "forms": ["Injection", "Cartridge"],
        "routes": ["Subcutaneous", "Intravenous"],
        "uses": "Diabetes",
        "solubility": "Protein formulation",
        "dose_type": "Biologic dose",
        "stability": "Temperature controlled; avoid freezing"
    },
    {
        "name": "Sildenafil",
        "class": "PDE-5 Inhibitor",
        "forms": ["Tablet", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Selected cardiovascular and sexual health indications",
        "solubility": "Slightly soluble depending on salt form",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Tamsulosin",
        "class": "Alpha-1 Adrenergic Blocker",
        "forms": ["Modified-Release Capsule"],
        "routes": ["Oral"],
        "uses": "Lower urinary tract symptoms",
        "solubility": "Slightly soluble depending on salt form",
        "dose_type": "Very low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Finasteride",
        "class": "5-Alpha Reductase Inhibitor",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Selected prostate and hair-loss indications",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from light and moisture"
    }
]


# ----------------------------
# Excipient roles
# ----------------------------

EXCIPIENTS = {
    "Diluent": [
        "Microcrystalline cellulose",
        "Lactose monohydrate",
        "Dicalcium phosphate",
        "Mannitol",
        "Calcium carbonate"
    ],
    "Binder": [
        "Povidone",
        "Pregelatinized starch",
        "Hydroxypropyl cellulose",
        "Hypromellose"
    ],
    "Disintegrant": [
        "Croscarmellose sodium",
        "Crospovidone",
        "Sodium starch glycolate"
    ],
    "Lubricant": [
        "Magnesium stearate",
        "Stearic acid",
        "Sodium stearyl fumarate"
    ],
    "Glidant": [
        "Colloidal silicon dioxide",
        "Talc"
    ],
    "Suspending agent": [
        "Sodium carboxymethylcellulose",
        "Xanthan gum",
        "Methylcellulose"
    ],
    "Preservative": [
        "Methylparaben",
        "Propylparaben",
        "Potassium sorbate",
        "Sodium benzoate"
    ],
    "Vehicle": [
        "Purified water",
        "Glycerin",
        "Propylene glycol",
        "Polyethylene glycol"
    ],
    "Sweetener": [
        "Sucrose",
        "Sorbitol",
        "Sucralose",
        "Saccharin sodium"
    ],
    "Film former": [
        "Hypromellose",
        "Polyvinyl alcohol",
        "Cellulose derivatives"
    ],
    "Topical base": [
        "White soft paraffin",
        "Liquid paraffin",
        "Carbomer",
        "Cetostearyl alcohol"
    ],
    "Sterile vehicle": [
        "Water for Injection",
        "Sodium chloride solution",
        "Phosphate buffer"
    ]
}


# ----------------------------
# Process and defect library
# ----------------------------

PROCESS_DATA = {
    "Tablet": {
        "process": [
            "Dispensing and material verification",
            "Sifting or milling where justified",
            "Blending or granulation",
            "Drying and moisture control where applicable",
            "Final blending and lubrication",
            "Compression",
            "Optional film coating",
            "Packing and reconciliation"
        ],
        "defects": [
            "Weight variation from poor powder flow",
            "Capping or lamination from air entrapment or compression conditions",
            "Sticking or picking from excess moisture or tooling issues",
            "Chipping from weak granules or insufficient binding",
            "Slow dissolution from over-lubrication or excessive hardness",
            "Content-uniformity failure from segregation"
        ],
        "tests": [
            "Appearance",
            "Weight variation",
            "Hardness",
            "Friability",
            "Disintegration",
            "Dissolution",
            "Assay",
            "Content uniformity"
        ]
    },
    "Capsule": {
        "process": [
            "Dispensing and sieving",
            "Powder blending or granulation",
            "Flow and bulk-density evaluation",
            "Capsule filling",
            "Fill-weight checks",
            "Visual inspection",
            "Packing and reconciliation"
        ],
        "defects": [
            "Fill-weight variation",
            "Poor flow and machine blockage",
            "Capsule body-cap separation",
            "Powder leakage",
            "Content-uniformity failure",
            "Moisture-related brittleness or softening"
        ],
        "tests": [
            "Appearance",
            "Fill-weight variation",
            "Disintegration",
            "Dissolution",
            "Assay",
            "Content uniformity",
            "Moisture"
        ]
    },
    "Liquid": {
        "process": [
            "Vehicle preparation",
            "Dissolution or dispersion of ingredients",
            "pH adjustment where required",
            "Addition of sweetener, flavor and preservative",
            "Volume make-up",
            "Filtration or homogenization where justified",
            "Filling and packing"
        ],
        "defects": [
            "Precipitation or crystallization",
            "Incorrect pH",
            "Microbial contamination",
            "Viscosity variation",
            "Sedimentation",
            "Fill-volume variation",
            "Color or flavor instability"
        ],
        "tests": [
            "Appearance",
            "pH",
            "Viscosity",
            "Specific gravity",
            "Assay",
            "Microbial limits",
            "Fill volume",
            "Stability"
        ]
    },
    "Suspension": {
        "process": [
            "Vehicle preparation",
            "Wetting and dispersion of API",
            "Particle-size control",
            "Addition of suspending agents",
            "Homogenization",
            "pH and viscosity adjustment",
            "Filling and packing"
        ],
        "defects": [
            "Rapid sedimentation",
            "Caking and poor redispersibility",
            "Particle-size growth",
            "Viscosity drift",
            "Foaming",
            "Microbial contamination",
            "Dose non-uniformity"
        ],
        "tests": [
            "Appearance",
            "pH",
            "Viscosity",
            "Particle-size distribution",
            "Sedimentation volume",
            "Redispersibility",
            "Assay",
            "Microbial limits"
        ]
    },
    "Sterile": {
        "process": [
            "Raw-material and container verification",
            "Solution or suspension preparation",
            "pH and osmolality adjustment",
            "Sterile filtration where applicable",
            "Aseptic filling or validated terminal sterilization",
            "Container closure",
            "Visual inspection",
            "Packaging and quarantine release"
        ],
        "defects": [
            "Sterility failure",
            "Bacterial endotoxin failure",
            "Particulate contamination",
            "pH or osmolality variation",
            "Fill-volume variation",
            "Container-closure leakage",
            "Precipitation or loss of potency"
        ],
        "tests": [
            "Appearance",
            "pH",
            "Assay",
            "Sterility",
            "Bacterial endotoxins",
            "Particulate matter",
            "Fill volume",
            "Container-closure integrity"
        ]
    },
    "Topical": {
        "process": [
            "Oil-phase or base preparation",
            "Aqueous-phase preparation where applicable",
            "API levigation, dissolution or dispersion",
            "Emulsification or polymer hydration",
            "Homogenization",
            "Cooling and de-aeration",
            "Filling and packing"
        ],
        "defects": [
            "Phase separation",
            "Creaming or cracking",
            "Lumping or grittiness",
            "Viscosity variation",
            "Air entrapment",
            "Microbial contamination",
            "Non-uniform API distribution"
        ],
        "tests": [
            "Appearance",
            "Homogeneity",
            "pH",
            "Viscosity",
            "Spreadability",
            "Assay",
            "Microbial limits",
            "Stability"
        ]
    }
}
# ----------------------------
# Utility functions
# ----------------------------

def find_drug(name):
    for item in DRUGS:
        if item["name"] == name:
            return item
    return None


def clean_text(value):
    if isinstance(value, list):
        return " ".join(str(x) for x in value)

    if value:
        return str(value)

    return "Not available"


def get_process_type(form):
    tablet_forms = [
        "Tablet",
        "Delayed-Release Tablet",
        "Chewable Tablet",
        "Extended-Release Tablet",
        "Modified-Release Tablet",
        "Orally Disintegrating Tablet",
        "Sublingual Tablet",
        "Vaginal Tablet",
        "Granules",
        "Lozenge"
    ]

    capsule_forms = [
        "Capsule",
        "Delayed-Release Capsule",
        "Modified-Release Capsule"
    ]

    liquid_forms = [
        "Syrup",
        "Oral Solution",
        "Oral Drops",
        "Nasal Solution",
        "Solution",
        "Mouthwash",
        "Gargle"
    ]

    suspension_forms = [
        "Suspension",
        "Oral Suspension",
        "Nebulizer Suspension"
    ]

    sterile_forms = [
        "Injection",
        "Eye Drops"
    ]

    topical_forms = [
        "Cream",
        "Gel",
        "Ointment",
        "Lotion",
        "Shampoo"
    ]

    if form in tablet_forms:
        return "Tablet"

    if form in capsule_forms:
        return "Capsule"

    if form in liquid_forms:
        return "Liquid"

    if form in suspension_forms:
        return "Suspension"

    if form in sterile_forms:
        return "Sterile"

    if form in topical_forms:
        return "Topical"

    return "Tablet"


def get_daily_med_search_url(name):
    return (
        "https://dailymed.nlm.nih.gov/dailymed/search.cfm?"
        "query=" + quote(name)
    )


def get_suggestions(drug, form):
    result = {}

    tablet_forms = [
        "Tablet",
        "Delayed-Release Tablet",
        "Chewable Tablet",
        "Extended-Release Tablet",
        "Modified-Release Tablet",
        "Orally Disintegrating Tablet",
        "Sublingual Tablet",
        "Vaginal Tablet"
    ]

    capsule_forms = [
        "Capsule",
        "Delayed-Release Capsule",
        "Modified-Release Capsule"
    ]

    liquid_forms = [
        "Syrup",
        "Oral Solution",
        "Suspension",
        "Oral Suspension",
        "Oral Drops",
        "Nasal Solution",
        "Solution",
        "Mouthwash",
        "Gargle"
    ]

    topical_forms = [
        "Cream",
        "Gel",
        "Ointment",
        "Lotion",
        "Shampoo"
    ]

    sterile_forms = [
        "Injection",
        "Eye Drops"
    ]

    if form in tablet_forms:
        result["Diluent"] = EXCIPIENTS["Diluent"]
        result["Binder"] = EXCIPIENTS["Binder"]
        result["Disintegrant"] = EXCIPIENTS["Disintegrant"]
        result["Lubricant"] = EXCIPIENTS["Lubricant"]
        result["Glidant"] = EXCIPIENTS["Glidant"]

    if form in capsule_forms:
        result["Capsule-fill diluent"] = EXCIPIENTS["Diluent"]
        result["Binder or granulation aid"] = EXCIPIENTS["Binder"]
        result["Glidant"] = EXCIPIENTS["Glidant"]
        result["Lubricant"] = EXCIPIENTS["Lubricant"]

    if form in liquid_forms:
        result["Vehicle"] = EXCIPIENTS["Vehicle"]
        result["Preservative"] = EXCIPIENTS["Preservative"]
        result["Sweetener"] = EXCIPIENTS["Sweetener"]

    if form in ["Suspension", "Oral Suspension"]:
        result["Suspending agent"] = EXCIPIENTS["Suspending agent"]

    if form in topical_forms:
        result["Topical base"] = EXCIPIENTS["Topical base"]
        result["Preservative"] = EXCIPIENTS["Preservative"]

    if form in sterile_forms:
        result["Sterile vehicle"] = EXCIPIENTS["Sterile vehicle"]

    if "Practically insoluble" in drug["solubility"]:
        result["Solubility-development topics"] = [
            "Particle-size reduction",
            "Surfactant screening",
            "Cosolvent screening",
            "Salt or pH screening",
            "Solid-dispersion investigation"
        ]

    if "Very low dose" in drug["dose_type"]:
        result["Low-dose control topics"] = [
            "Content uniformity",
            "Geometric dilution",
            "Blend segregation study",
            "Validated assay method"
        ]

    if "High dose" in drug["dose_type"]:
        result["High-dose control topics"] = [
            "Drug-loading capability",
            "Blend uniformity",
            "Powder flow",
            "Dosage-form size"
        ]

    if "Acid sensitive" in drug["stability"]:
        result["Protection topics"] = [
            "Enteric protection development",
            "Microenvironmental pH study",
            "Moisture-protective packaging",
            "Acid-stage dissolution evaluation"
        ]

    return result
    # ----------------------------
# Live public-data functions
# ----------------------------

@st.cache_data(ttl=86400, show_spinner=False)
def get_pubchem_data(name):
    properties = (
        "IUPACName,MolecularFormula,MolecularWeight,"
        "CanonicalSMILES,IsomericSMILES,"
        "HBondDonorCount,HBondAcceptorCount,"
        "RotatableBondCount,XLogP,TPSA"
    )

    url = (
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
        + quote(name)
        + "/property/"
        + properties
        + "/JSON"
    )

    try:
        response = requests.get(url, timeout=25)

        if response.status_code != 200:
            return {"Status": "No PubChem record found"}

        item = response.json()["PropertyTable"]["Properties"][0]

        return {
            "PubChem CID": item.get("CID", "Not available"),
            "IUPAC Name": item.get("IUPACName", "Not available"),
            "Molecular Formula": item.get(
                "MolecularFormula",
                "Not available"
            ),
            "Molecular Weight": item.get(
                "MolecularWeight",
                "Not available"
            ),
            "Hydrogen Bond Donors": item.get(
                "HBondDonorCount",
                "Not available"
            ),
            "Hydrogen Bond Acceptors": item.get(
                "HBondAcceptorCount",
                "Not available"
            ),
            "Rotatable Bonds": item.get(
                "RotatableBondCount",
                "Not available"
            ),
            "XLogP": item.get("XLogP", "Not available"),
            "TPSA": item.get("TPSA", "Not available"),
            "Canonical SMILES": item.get(
                "ConnectivitySMILES",
                "Not available"
            ),
            "Isomeric SMILES": item.get(
                "SMILES",
                "Not available"
            )
        }

    except Exception as error:
        return {"Error": str(error)}


@st.cache_data(ttl=86400, show_spinner=False)
def get_openfda_data(name):
    url = (
        "https://api.fda.gov/drug/label.json?"
        "search=openfda.generic_name:"
        + quote(name.lower())
        + "&limit=1"
    )

    try:
        response = requests.get(url, timeout=25)

        if response.status_code != 200:
            return {"Status": "No matching openFDA label found"}

        result = response.json()["results"][0]

        return {
            "Indications": clean_text(
                result.get("indications_and_usage")
            ),
            "Warnings": clean_text(
                result.get("warnings")
            ),
            "Dosage and Administration": clean_text(
                result.get("dosage_and_administration")
            ),
            "Routes": clean_text(result.get("route")),
            "Manufacturers": clean_text(
                result.get("manufacturer_name")
            ),
            "OpenFDA Brand Names": clean_text(
                result.get("openfda", {}).get("brand_name")
            )
        }

    except Exception as error:
        return {"Error": str(error)}


@st.cache_data(ttl=86400, show_spinner=False)
def get_dailymed_records(name):
    url = (
        "https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?"
        "drug_name=" + quote(name)
    )

    try:
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            return []

        data = response.json()

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            for key in ["data", "results", "spls"]:
                if isinstance(data.get(key), list):
                    return data[key]

        return []

    except Exception:
        return []


def normalize_dailymed_records(records):
    rows = []

    for item in records[:30]:
        set_id = (
            item.get("setid")
            or item.get("setId")
            or item.get("set_id")
            or item.get("SETID")
            or ""
        )

        title = (
            item.get("title")
            or item.get("drug_name")
            or item.get("drugName")
            or item.get("name")
            or "DailyMed label"
        )

        manufacturer = (
            item.get("labeler")
            or item.get("manufacturer")
            or item.get("companyName")
            or "Not listed"
        )

        if set_id:
            url = (
                "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?"
                "setid=" + quote(str(set_id))
            )
        else:
            url = ""

        rows.append(
            {
                "Product / label": title,
                "Manufacturer": manufacturer,
                "Set ID": set_id or "Not available",
                "Label URL": url
            }
        )

    return rows


@st.cache_data(ttl=86400, show_spinner=False)
def get_dailymed_xml(set_id):
    url = (
        "https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/"
        + quote(str(set_id))
        + ".xml"
    )

    try:
        response = requests.get(url, timeout=35)

        if response.status_code != 200:
            return ""

        return response.text

    except Exception:
        return ""


def extract_inactive_ingredients(xml_text):
    if not xml_text:
        return []

    soup = BeautifulSoup(xml_text, "xml")
    ingredients = []

    for element in soup.find_all(
        string=re.compile(
            "inactive ingredients",
            re.IGNORECASE
        )
    ):
        parent = element.parent

        for node in parent.find_all_next(
            ["ingredient", "ingredientSubstance"],
            limit=100
        ):
            text = node.get_text(" ", strip=True)

            if text and text not in ingredients:
                ingredients.append(text)

        if ingredients:
            break

    if ingredients:
        return ingredients

    full_text = soup.get_text(" ", strip=True)

    match = re.search(
        r"inactive ingredients(.{0,5000})",
        full_text,
        flags=re.IGNORECASE
    )

    if match:
        raw = match.group(1)

        parts = re.split(
            r",|;||",
            raw
        )

        return [
            part.strip()
            for part in parts
            if len(part.strip()) > 2
        ][:100]

    return []
    # ----------------------------
# App header and sidebar
# ----------------------------

st.markdown(
    """
    <div class="hero">
        <h1>💊 PharmaLens 100</h1>
        <p>
        API properties, dosage forms, product-label ingredients,
        formulation development and manufacturing-risk dashboard.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="notice">
    <b>Important:</b> This is an educational formulation-research app.
    It is not a validated master formula, batch manufacturing record,
    regulatory submission, prescription tool or medical advice system.
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("🔎 API search")

search_text = st.sidebar.text_input(
    "Search API",
    placeholder="Example: Paracetamol"
)

if search_text:
    filtered = [
        drug for drug in DRUGS
        if search_text.lower() in drug["name"].lower()
    ]
else:
    filtered = DRUGS

if not filtered:
    st.error("API not found. Try another spelling.")
    st.stop()

selected_name = st.sidebar.selectbox(
    "Select API",
    [drug["name"] for drug in filtered]
)

selected_drug = find_drug(selected_name)

selected_form = st.sidebar.selectbox(
    "Select dosage form",
    selected_drug["forms"]
)

st.sidebar.divider()
st.sidebar.metric("APIs loaded", len(DRUGS))
st.sidebar.caption(
    "Exact inactive ingredients are read from a selected product label."
)


# ----------------------------
# Dashboard metrics
# ----------------------------

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("API", selected_drug["name"])

with m2:
    st.metric("Class", selected_drug["class"])

with m3:
    st.metric("Market forms in dataset", len(selected_drug["forms"]))

with m4:
    st.metric("Selected form", selected_form)


tabs = st.tabs(
    [
        "🧬 API profile",
        "🌐 Live properties",
        "🧪 Exact ingredients",
        "🏭 Process defects",
        "📋 Development notes"
    ]
)


# ----------------------------
# API profile
# ----------------------------

with tabs[0]:
    st.subheader("API profile")

    profile = pd.DataFrame(
        [
            ["API name", selected_drug["name"]],
            ["Therapeutic class", selected_drug["class"]],
            ["Common use", selected_drug["uses"]],
            ["Solubility note", selected_drug["solubility"]],
            ["Dose category", selected_drug["dose_type"]],
            ["Stability note", selected_drug["stability"]],
            ["Marketed dosage forms",
             ", ".join(selected_drug["forms"])],
            ["Routes",
             ", ".join(selected_drug["routes"])]
        ],
        columns=["Property", "Information"]
    )

    st.dataframe(
        profile,
        use_container_width=True,
        hide_index=True
    )


# ----------------------------
# Live PubChem/openFDA
# ----------------------------

with tabs[1]:
    st.subheader("Live public properties")

    if st.button(
        "Fetch PubChem + openFDA data",
        type="primary",
        use_container_width=True
    ):
        with st.spinner("Fetching public data..."):
            pubchem_data = get_pubchem_data(selected_name)
            fda_data = get_openfda_data(selected_name)

        st.write("### PubChem chemical properties")
        st.json(pubchem_data)

        st.write("### openFDA label information")

        if "Error" in fda_data or "Status" in fda_data:
            st.warning(fda_data)
        else:
            for title, value in fda_data.items():
                with st.expander(title):
                    st.write(value)


# ----------------------------
# Exact label ingredients
# ----------------------------

with tabs[2]:
    st.subheader(
        f"Product-specific ingredients: {selected_name}"
    )

    st.markdown(
        """
        <div class="success-box">
        Exact inactive ingredients depend on product, strength,
        manufacturer, country and dosage form. Select a specific DailyMed
        label before treating any ingredient list as product-specific.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.link_button(
        "🔗 Open DailyMed manual search",
        get_daily_med_search_url(selected_name),
        use_container_width=True
    )

    if st.button(
        "Search current DailyMed records",
        use_container_width=True
    ):
        with st.spinner("Searching DailyMed records..."):
            records = get_dailymed_records(selected_name)

        normalized = normalize_dailymed_records(records)

        if normalized:
            st.dataframe(
                pd.DataFrame(normalized),
                use_container_width=True,
                hide_index=True
            )

            set_ids = [
                row["Set ID"]
                for row in normalized
                if row["Set ID"] != "Not available"
            ]

            if set_ids:
                selected_set_id = st.selectbox(
                    "Select a product Set ID",
                    set_ids
                )

                if st.button(
                    "Read inactive ingredients from selected label"
                ):
                    with st.spinner("Reading selected SPL label..."):
                        xml_text = get_dailymed_xml(
                            selected_set_id
                        )

                    ingredients = extract_inactive_ingredients(
                        xml_text
                    )

                    if ingredients:
                        ingredient_df = pd.DataFrame(
                            {
                                "Product-specific ingredient record":
                                ingredients
                            }
                        )

                        st.dataframe(
                            ingredient_df,
                            use_container_width=True,
                            hide_index=True
                        )

                        st.info(
                            "Verify this list against the original "
                            "DailyMed label before using it in any report."
                        )
                    else:
                        st.warning(
                            "Automatic extraction failed. Open the "
                            "original DailyMed label manually."
                        )
        else:
            st.warning(
                "No DailyMed API records were returned. Use the manual "
                "search button above."
            )

    st.subheader(
        "Role-based excipient development suggestions"
    )

    st.caption(
        "The following are examples by function, not exact commercial "
        "formula ingredients."
    )

    suggestions = get_suggestions(
        selected_drug,
        selected_form
    )

    rows = []

    for role, items in suggestions.items():
        rows.append(
            {
                "Role / development topic": role,
                "Examples": ", ".join(items),
                "Development note": (
                    "Confirm grade, compatibility, concentration, "
                    "safety, regulatory status and stability."
                )
            }
        )

    if rows:
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

    st.link_button(
        "🔗 FDA Inactive Ingredient Database",
        "https://www.accessdata.fda.gov/scripts/cder/iig/index.cfm",
        use_container_width=True
)
    # ----------------------------
# Process and defects
# ----------------------------

with tabs[3]:
    process_type = get_process_type(selected_form)
    process = PROCESS_DATA[process_type]

    st.subheader(
        f"High-level manufacturing risk map: {selected_form}"
    )

    st.write("### Process stages")

    for number, step in enumerate(process["process"], start=1):
        st.write(f"{number}. {step}")

    st.write("### Possible defects")

    defect_rows = []

    for defect in process["defects"]:
        defect_rows.append(
            {
                "Possible defect": defect,
                "Investigation focus": (
                    "Review material attributes, equipment status, "
                    "process parameters, IPC data, deviation history, "
                    "cleaning and batch documentation."
                )
            }
        )

    st.dataframe(
        pd.DataFrame(defect_rows),
        use_container_width=True,
        hide_index=True
    )

    st.write("### Typical quality checks")

    quality_df = pd.DataFrame(
        {
            "Quality check": process["tests"],
            "Purpose": [
                "Confirm dosage-form performance and consistency"
                for _ in process["tests"]
            ]
        }
    )

    st.dataframe(
        quality_df,
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        "Actual production must follow approved specifications, "
        "validated processes, GMP requirements, authorized SOPs and "
        "approved batch records."
    )


# ----------------------------
# Development notes
# ----------------------------

with tabs[4]:
    st.subheader("Formulation-development checklist")

    checklist = [
        "Confirm API identity, assay, polymorph or salt form where relevant",
        "Evaluate particle size, flow, density, moisture and compatibility",
        "Select dosage form based on therapeutic need and product performance",
        "Screen excipient compatibility and concentration ranges",
        "Define critical quality attributes",
        "Identify critical material attributes and process parameters",
        "Perform stability and packaging studies",
        "Define in-process controls and acceptance criteria",
        "Investigate defects through documented root-cause analysis",
        "Use CAPA and continued process verification after validation"
    ]

    for item in checklist:
        st.checkbox(item, value=False)

    st.markdown(
        """
        FDA process-validation guidance uses a lifecycle approach:
        process design, process qualification and continued process
        verification. [web:85]
        """
    )


# ----------------------------
# Footer
# ----------------------------

st.divider()

st.caption(
    "PharmaLens 100 | Educational research dashboard | "
    "Always verify current product labels and regulatory requirements."
                )
