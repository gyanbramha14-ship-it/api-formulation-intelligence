import streamlit as st
import requests
from urllib.parse import quote

st.set_page_config(
    page_title="API → Formulation Intelligence",
    page_icon="🧪",
    layout="wide"
)

# ============================================================
# EVIDENCE SOURCES
# ============================================================

SOURCES = [
    {
        "title": "ICH Q8(R2) Pharmaceutical Development",
        "url": "https://www.ema.europa.eu/en/ich-q8-r2-pharmaceutical-development-scientific-guideline",
        "type": "Regulatory / ICH"
    },
    {
        "title": "FDA Inactive Ingredient Database",
        "url": "https://www.fda.gov/drugs/drug-approvals-and-databases/inactive-ingredients-database-download",
        "type": "Regulatory / Excipient"
    },
    {
        "title": "FDA Dissolution Resources",
        "url": "https://www.fda.gov/animal-veterinary/new-animal-drug-applications/compilation-fda-guidance-and-resources-in-vitro-dissolution-testing-immediate-release-solid-oral-dosage",
        "type": "Regulatory / Dissolution"
    }
]

# ============================================================
# DEMO API DATABASE
# ============================================================

API_DATABASE = {

    "paracetamol": {
        "name": "Paracetamol",
        "mw": "151.16 g/mol",
        "pka": "~9.5",
        "logp": "~0.5",
        "solubility": "Moderate aqueous solubility; temperature dependent",
        "melting_point": "~169–170 °C",
        "bcs": "Verify according to dose/solubility/permeability criteria",
        "major_risks": [
            "High dose can make dissolution and manufacturability important.",
            "Particle size can influence powder behavior and dissolution.",
            "Compressibility/tabletability should be characterized.",
            "Thermal and processing stability should be considered."
        ]
    },

    "ibuprofen": {
        "name": "Ibuprofen",
        "mw": "206.28 g/mol",
        "pka": "~4.4",
        "logp": "~3.5",
        "solubility": "Low aqueous solubility; pH dependent",
        "melting_point": "~75–78 °C",
        "bcs": "Commonly discussed as BCS II / dissolution-limited context",
        "major_risks": [
            "Low aqueous solubility.",
            "Weak-acid ionization makes pH important.",
            "Dissolution enhancement may require investigation.",
            "Particle size and solid-state properties may affect performance."
        ]
    }
}
st.set_page_config(page_title="API Formulation Intelligence Pro", layout="wide")

# ---------- DRUG DATABASE ----------
DRUG_DATABASE = {
    "Paracetamol": {
        "api_profile": {
            "Molecular Weight": "151.16 g/mol",
            "BCS": "Class III",
            "pKa": "9.5",
            "LogP": "0.5",
            "Melting Point": "169-170°C"
        },
        "preformulation": [
            "Solubility study",
            "Particle size analysis",
            "Flow properties",
            "Compressibility",
            "Compatibility study (FTIR, DSC)"
        ],
        "excipients": {
            "Diluent": "Microcrystalline Cellulose",
            "Binder": "PVP K30",
            "Disintegrant": "Sodium Starch Glycolate",
            "Lubricant": "Magnesium Stearate",
            "Glidant": "Colloidal Silicon Dioxide"
        },
        "procedure": [
            "API weighing",
            "Sieving",
            "Pre-blending",
            "Lubrication",
            "Compression",
            "Evaluation",
            "Stability study"
        ],
        "evaluation": [
            "Hardness",
            "Friability",
            "Disintegration",
            "Dissolution",
            "Assay",
            "Content Uniformity"
        ],
        "stability": [
            "Accelerated stability",
            "Long-term stability"
        ],
        "references": [
            "PMID:16806756",
            "PMID:37978101",
            "PMID:41408804"
        ]
    }
     "Ibuprofen": {
        "api_profile": {
            "Molecular Weight": "206.28 g/mol",
            "BCS": "Class II",
            "pKa": "4.4",
            "LogP": "3.5"
        },
        "preformulation": [
            "Solubility vs pH",
            "Particle size",
            "Compatibility"
        ],
        "excipients": {
            "Diluent": "Lactose",
            "Binder": "PVP K30",
            "Disintegrant": "Crospovidone",
            "Lubricant": "Magnesium Stearate",
            "Glidant": "Aerosil"
        },
        "procedure": [
            "API characterization",
            "Blending",
            "Compression",
            "Dissolution",
            "Stability"
        ],
        "evaluation": [
            "Hardness",
            "Dissolution",
            "Assay"
        ],
        "stability": [
            "Accelerated stability"
        ],
        "references": [
            "PMID:23614647"
        ]
    }

    DRUG_DATABASE = {
    "Paracetamol": {
        ...
    },

    "Ibuprofen": {
        ...
    },

    "Metformin": {
        ...
    },

    "Amlodipine": {
        ...
    }
}


# ---------- UI ----------
st.title("🧪 API Formulation Intelligence Pro")

drug = st.selectbox("Select API", list(DRUG_DATABASE.keys()))

if st.button("Analyze API"):
    d = DRUG_DATABASE[drug]

    st.header("1. API Profile")
    st.json(d["api_profile"])

    st.header("2. Preformulation Studies")
    for item in d["preformulation"]:
        st.write("•", item)

    st.header("3. Excipients Used")
    st.json(d["excipients"])

    st.header("4. Manufacturing Procedure")
    for i, step in enumerate(d["procedure"], 1):
        st.write(f"{i}. {step}")

    st.header("5. Evaluation Tests")
    for t in d["evaluation"]:
        st.write("•", t)

    st.header("6. Stability Studies")
    for s in d["stability"]:
        st.write("•", s)

    st.header("7. Literature References")
    for r in d["references"]:
        st.write("•", r)
"Metformin": {
    "api_profile":{"MW":"129.16 g/mol","BCS":"Class III","pKa":"12.4","LogP":"-1.4"},
    "excipients":{"Diluent":"MCC","Binder":"PVP K30","Disintegrant":"Crospovidone","Lubricant":"Magnesium Stearate","Glidant":"Aerosil"},
    "procedure":["Weighing","Sieving","Blending","Compression","Evaluation","Stability"]
},

"Amlodipine": {
    "api_profile":{"MW":"408.9 g/mol","BCS":"Class I","pKa":"8.6","LogP":"2.1"},
    "excipients":{"Diluent":"Lactose","Binder":"PVP","Disintegrant":"SSG","Lubricant":"Magnesium Stearate","Glidant":"Talc"},
    "procedure":["Weighing","Blending","Compression","Evaluation","Stability"]
},

"Diclofenac Sodium": {
    "api_profile":{"MW":"318.1 g/mol","BCS":"Class II","pKa":"4.0","LogP":"4.5"},
    "excipients":{"Diluent":"MCC","Binder":"HPMC","Disintegrant":"Crospovidone","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["API study","Blending","Compression","Dissolution","Stability"]
},

"Aspirin": {
    "api_profile":{"MW":"180.16 g/mol","BCS":"Class I","pKa":"3.5","LogP":"1.2"},
    "excipients":{"Diluent":"Starch","Binder":"PVP","Disintegrant":"SSG","Lubricant":"Mg Stearate","Glidant":"Talc"},
    "procedure":["Weighing","Granulation","Drying","Compression","Evaluation"]
},

"Atorvastatin": {
    "api_profile":{"MW":"558.6 g/mol","BCS":"Class II","pKa":"4.5","LogP":"6.3"},
    "excipients":{"Diluent":"Lactose","Binder":"HPMC","Disintegrant":"CCS","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["API characterization","Wet granulation","Compression","Evaluation"]
},

"Rosuvastatin": {
    "api_profile":{"MW":"481.5 g/mol","BCS":"Class III","pKa":"4.6","LogP":"0.1"},
    "excipients":{"Diluent":"MCC","Binder":"PVP","Disintegrant":"Crospovidone","Lubricant":"Mg Stearate","Glidant":"Aerosil"},
    "procedure":["Blending","Compression","Evaluation","Stability"]
},

"Losartan": {
    "api_profile":{"MW":"422.9 g/mol","BCS":"Class III","pKa":"4.0","LogP":"4.0"},
    "excipients":{"Diluent":"Lactose","Binder":"PVP","Disintegrant":"SSG","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Weighing","Blending","Compression","Evaluation"]
},

"Telmisartan": {
    "api_profile":{"MW":"514.6 g/mol","BCS":"Class II","pKa":"4.5","LogP":"7.7"},
    "excipients":{"Diluent":"MCC","Binder":"PVP","Disintegrant":"Crospovidone","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Particle size reduction","Blending","Compression","Evaluation"]
},

"Valsartan": {
    "api_profile":{"MW":"435.5 g/mol","BCS":"Class III","pKa":"4.9","LogP":"1.5"},
    "excipients":{"Diluent":"Lactose","Binder":"PVP","Disintegrant":"CCS","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Blending","Compression","Evaluation"]
},

"Atenolol": {
    "api_profile":{"MW":"266.3 g/mol","BCS":"Class III","pKa":"9.6","LogP":"0.2"},
    "excipients":{"Diluent":"MCC","Binder":"Starch Paste","Disintegrant":"SSG","Lubricant":"Mg Stearate","Glidant":"Talc"},
    "procedure":["Granulation","Compression","Evaluation"]
},

"Propranolol": {
    "api_profile":{"MW":"259.3 g/mol","BCS":"Class I","pKa":"9.5","LogP":"3.5"},
    "excipients":{"Diluent":"Lactose","Binder":"PVP","Disintegrant":"Crospovidone","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Blending","Compression","Evaluation"]
},

"Carvedilol": {
    "api_profile":{"MW":"406.5 g/mol","BCS":"Class II","pKa":"7.8","LogP":"3.8"},
    "excipients":{"Diluent":"MCC","Binder":"PVP","Disintegrant":"SSG","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Wet granulation","Compression","Evaluation"]
},

"Amoxicillin": {
    "api_profile":{"MW":"365.4 g/mol","BCS":"Class III","pKa":"2.8","LogP":"-0.8"},
    "excipients":{"Diluent":"MCC","Binder":"PVP","Disintegrant":"Crospovidone","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Blending","Compression","Evaluation"]
},

"Cefixime": {
    "api_profile":{"MW":"453.5 g/mol","BCS":"Class IV","pKa":"2.5","LogP":"0.4"},
    "excipients":{"Diluent":"Lactose","Binder":"HPMC","Disintegrant":"SSG","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Wet granulation","Compression","Evaluation"]
},

"Ciprofloxacin": {
    "api_profile":{"MW":"331.3 g/mol","BCS":"Class III","pKa":"6.1","LogP":"0.3"},
    "excipients":{"Diluent":"MCC","Binder":"PVP","Disintegrant":"Crospovidone","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Blending","Compression","Evaluation"]
},

"Azithromycin": {
    "api_profile":{"MW":"749 g/mol","BCS":"Class III","pKa":"8.7","LogP":"4.0"},
    "excipients":{"Diluent":"Lactose","Binder":"PVP","Disintegrant":"SSG","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Granulation","Compression","Evaluation"]
},

"Doxycycline": {
    "api_profile":{"MW":"444.4 g/mol","BCS":"Class I","pKa":"3.0","LogP":"-0.2"},
    "excipients":{"Diluent":"MCC","Binder":"PVP","Disintegrant":"CCS","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Blending","Capsule filling","Evaluation"]
},

"Omeprazole": {
    "api_profile":{"MW":"345.4 g/mol","BCS":"Class II","pKa":"4.0","LogP":"2.2"},
    "excipients":{"Diluent":"Mannitol","Binder":"HPMC","Disintegrant":"Crospovidone","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Pellet coating","Capsule filling","Evaluation"]
},

"Pantoprazole": {
    "api_profile":{"MW":"383.4 g/mol","BCS":"Class III","pKa":"3.8","LogP":"2.0"},
    "excipients":{"Diluent":"MCC","Binder":"PVP","Disintegrant":"CCS","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Enteric coating","Compression","Evaluation"]
},

"Rabeprazole": {
    "api_profile":{"MW":"359.4 g/mol","BCS":"Class III","pKa":"5.0","LogP":"2.5"},
    "excipients":{"Diluent":"Mannitol","Binder":"HPMC","Disintegrant":"Crospovidone","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Enteric tablet","Evaluation"]
},

"Cetirizine": {
    "api_profile":{"MW":"388.9 g/mol","BCS":"Class III","pKa":"2.2","LogP":"2.9"},
    "excipients":{"Diluent":"Lactose","Binder":"PVP","Disintegrant":"SSG","Lubricant":"Mg Stearate","Glidant":"Talc"},
    "procedure":["Blending","Compression","Evaluation"]
},

"Levocetirizine": {
    "api_profile":{"MW":"388.9 g/mol","BCS":"Class III","pKa":"2.1","LogP":"2.8"},
    "excipients":{"Diluent":"MCC","Binder":"PVP","Disintegrant":"CCS","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Compression","Evaluation"]
},

"Loratadine": {
    "api_profile":{"MW":"382.9 g/mol","BCS":"Class II","pKa":"5.0","LogP":"5.2"},
    "excipients":{"Diluent":"Lactose","Binder":"PVP","Disintegrant":"Crospovidone","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Blending","Compression","Evaluation"]
},

"Fexofenadine": {
    "api_profile":{"MW":"501.7 g/mol","BCS":"Class III","pKa":"4.3","LogP":"0.5"},
    "excipients":{"Diluent":"MCC","Binder":"PVP","Disintegrant":"SSG","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Compression","Evaluation"]
},

"Salbutamol": {
    "api_profile":{"MW":"239.3 g/mol","BCS":"Class I","pKa":"9.2","LogP":"1.3"},
    "excipients":{"Diluent":"Lactose","Binder":"PVP","Disintegrant":"SSG","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Tablet preparation","Evaluation"]
},

"Theophylline": {
    "api_profile":{"MW":"180.2 g/mol","BCS":"Class I","pKa":"8.6","LogP":"-0.1"},
    "excipients":{"Diluent":"MCC","Binder":"HPMC","Disintegrant":"CCS","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["SR tablet formulation","Evaluation"]
},

"Montelukast": {
    "api_profile":{"MW":"586.2 g/mol","BCS":"Class II","pKa":"5.7","LogP":"8.8"},
    "excipients":{"Diluent":"Lactose","Binder":"PVP","Disintegrant":"Crospovidone","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Compression","Evaluation"]
},

"Fluconazole": {
    "api_profile":{"MW":"306.3 g/mol","BCS":"Class I","pKa":"1.8","LogP":"0.5"},
    "excipients":{"Diluent":"MCC","Binder":"PVP","Disintegrant":"SSG","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Tablet formulation","Evaluation"]
},

"Ketoconazole": {
    "api_profile":{"MW":"531.4 g/mol","BCS":"Class II","pKa":"6.5","LogP":"4.3"},
    "excipients":{"Diluent":"Lactose","Binder":"PVP","Disintegrant":"Crospovidone","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Tablet formulation","Evaluation"]
},

"Clotrimazole": {
    "api_profile":{"MW":"344.8 g/mol","BCS":"Class II","pKa":"6.0","LogP":"6.1"},
    "excipients":{"Diluent":"MCC","Binder":"PVP","Disintegrant":"SSG","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Tablet/Cream formulation","Evaluation"]
},

"Albendazole": {
    "api_profile":{"MW":"265.3 g/mol","BCS":"Class II","pKa":"2.8","LogP":"3.2"},
    "excipients":{"Diluent":"Lactose","Binder":"PVP","Disintegrant":"Crospovidone","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Tablet formulation","Evaluation"]
},

"Mebendazole": {
    "api_profile":{"MW":"295.3 g/mol","BCS":"Class II","pKa":"3.0","LogP":"2.9"},
    "excipients":{"Diluent":"MCC","Binder":"PVP","Disintegrant":"SSG","Lubricant":"Mg Stearate","Glidant":"Silica"},
    "procedure":["Tablet formulation","Evaluation"]
}


# ============================================================
# PUBMED SEARCH
# ============================================================

def search_pubmed(api_name):

    query = (
        f'"{api_name}" AND '
        f'(formulation OR preformulation OR solubility OR '
        f'dissolution OR excipient OR tablet OR granulation)'
    )

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    try:

        response = requests.get(
            url,
            params={
                "db": "pubmed",
                "term": query,
                "retmode": "json",
                "retmax": 15
            },
            timeout=15
        )

        response.raise_for_status()

        ids = response.json()["esearchresult"]["idlist"]

        if not ids:
            return []

        summary_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
            "esummary.fcgi"
        )

        response2 = requests.get(
            summary_url,
            params={
                "db": "pubmed",
                "id": ",".join(ids),
                "retmode": "json"
            },
            timeout=15
        )

        data = response2.json()["result"]

        papers = []

        for pmid in ids:

            item = data.get(pmid, {})

            papers.append({
                "title": item.get("title", ""),
                "journal": item.get("fulljournalname", ""),
                "date": item.get("pubdate", ""),
                "pmid": pmid,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            })

        return papers

    except Exception:
        return []


# ============================================================
# FORMULATION STRATEGIES
# ============================================================

STRATEGIES = {

    "Tablet": {

        "Direct Compression": [

            "API identification and specification verification",

            "Particle-size characterization",

            "Sieve API and excipients where required",

            "Assess powder flow",

            "Assess bulk and tapped density",

            "Calculate Carr's Index / Hausner Ratio",

            "Perform API–excipient compatibility assessment",

            "Prepare pre-blend",

            "Add functional excipients according to formulation design",

            "Assess blend uniformity",

            "Add lubricant/glidant where justified",

            "Final blending",

            "Compression development",

            "In-process checks",

            "Tablet evaluation",

            "Dissolution testing",

            "Stability evaluation"
        ],

        "Wet Granulation": [

            "API characterization",

            "Excipient compatibility",

            "Sieving",

            "Dry blending",

            "Prepare binder solution/suspension",

            "Add granulating liquid under controlled conditions",

            "Wet massing / granulation",

            "Wet screening where applicable",

            "Drying",

            "Determine drying endpoint / moisture",

            "Dry sizing",

            "Final blending",

            "Lubrication",

            "Compression",

            "In-process controls",

            "Finished-tablet evaluation",

            "Dissolution",

            "Stability"
        ],

        "Dry Granulation": [

            "API characterization",

            "Excipient compatibility",

            "Sieving",

            "Pre-blending",

            "Compaction / slugging or roller compaction",

            "Granule sizing",

            "Granule characterization",

            "Final blending",

            "Lubrication",

            "Compression",

            "Tablet evaluation",

            "Dissolution",

            "Stability"
        ]
    },

    "Liquid": {

        "Solution": [

            "API identity and assay confirmation",

            "Determine equilibrium solubility",

            "Develop pH–solubility profile",

            "Identify suitable vehicle system from literature",

            "Evaluate pH and buffer compatibility",

            "Evaluate cosolvent/solubilizer where justified",

            "Prepare vehicle phase",

            "Add API under controlled mixing",

            "Confirm complete dissolution",

            "Adjust pH where justified",

            "Make up final volume",

            "Filter if scientifically appropriate",

            "Evaluate clarity",

            "Assay",

            "Related substances",

            "pH",

            "Microbial quality where applicable",

            "Stability"
        ],

        "Suspension": [

            "API particle-size characterization",

            "Wetting study",

            "Vehicle selection",

            "Suspending-agent screening",

            "Prepare vehicle",

            "Hydrate/disperse polymer if applicable",

            "Wetting / levigation of API",

            "Controlled dispersion",

            "Homogenization where appropriate",

            "Make up final volume",

            "Evaluate sedimentation",

            "Evaluate redispersibility",

            "Particle-size distribution",

            "Assay",

            "Microbial quality where applicable",

            "Stability"
        ]
    },

    "Topical": {

        "Cream/Gel": [

            "API characterization",

            "Solubility in intended vehicle",

            "API–excipient compatibility",

            "Select oil/water or gel system",

            "Prepare appropriate phase",

            "API incorporation",

            "Homogenization",

            "pH adjustment where applicable",

            "Viscosity evaluation",

            "Spreadability",

            "Content uniformity",

            "In-vitro release/permeation where applicable",

            "Microbial quality",

            "Stability"
        ]
    }
}


# ============================================================
# EXCIPIENT FUNCTIONS
# ============================================================

EXCIPIENTS = {

    "Tablet": [
        ("Diluent / filler",
         "Provides bulk and can influence flow, compression and dissolution."),

        ("Binder",
         "Improves particle/granule cohesion where required."),

        ("Disintegrant",
         "Promotes tablet breakup and can influence dissolution."),

        ("Lubricant",
         "Reduces die-wall friction and supports tablet ejection."),

        ("Glidant",
         "Can improve powder flow where justified."),

        ("Surfactant",
         "May improve wetting/solubilization when evidence supports its use."),

        ("Polymer",
         "May be used for modified release or enabling technologies.")
    ],

    "Liquid": [
        ("Vehicle",
         "Provides the liquid medium for the API."),

        ("Cosolvent",
         "May improve apparent solubility where appropriate."),

        ("Surfactant / solubilizer",
         "May improve wetting or solubilization."),

        ("Buffer / pH modifier",
         "Controls pH where required for solubility or stability."),

        ("Suspending agent",
         "Provides physical stability in suspension systems."),

        ("Preservative",
         "May be required for suitable aqueous multidose systems.")
    ]
}


# ============================================================
# APP HEADER
# ============================================================

st.title("🧪 API → Formulation Intelligence")

st.caption(
    "Evidence-oriented formulation development research assistant"
)

st.info(
    "Workflow: API → Properties → Preformulation → "
    "Formulation Strategy → Detailed Procedure → Excipients → "
    "Literature → Evaluation → Stability → Regulatory"
)


# ============================================================
# API INPUT
# ============================================================

st.header("1️⃣ Select API")

api_name = st.text_input(
    "Enter API name",
    placeholder="Example: Paracetamol"
)

if st.button("Continue →", type="primary"):

    if api_name.strip():

        st.session_state["api"] = api_name.strip()

        key = api_name.lower().strip()

        if key in API_DATABASE:
            st.session_state["profile"] = API_DATABASE[key]
        else:
            st.session_state["profile"] = {
                "name": api_name,
                "mw": "",
                "pka": "",
                "logp": "",
                "solubility": "",
                "melting_point": "",
                "bcs": "",
                "major_risks": [
                    "No validated local profile available.",
                    "Retrieve authoritative physicochemical data.",
                    "Do not infer missing values."
                ]
            }


# ============================================================
# PROPERTY INTERFACE
# ============================================================

if "profile" in st.session_state:

    p = st.session_state["profile"]

    st.divider()

    st.header("2️⃣ API Properties")

    c1, c2, c3 = st.columns(3)

    with c1:

        mw = st.text_input(
            "Molecular weight",
            value=p.get("mw", "")
        )

        pka = st.text_input(
            "pKa",
            value=p.get("pka", "")
        )

    with c2:

        logp = st.text_input(
            "LogP / LogD",
            value=p.get("logp", "")
        )

        solubility = st.text_input(
            "Aqueous solubility",
            value=p.get("solubility", "")
        )

    with c3:

        melting = st.text_input(
            "Melting point",
            value=p.get("melting_point", "")
        )

        bcs = st.text_input(
            "BCS classification",
            value=p.get("bcs", "")
        )

    st.subheader("Additional API information")

    col1, col2 = st.columns(2)

    with col1:

        particle_size = st.text_input(
            "Particle size / PSD"
        )

        polymorph = st.text_input(
            "Polymorph / solid-state form"
        )

        hygroscopicity = st.text_input(
            "Hygroscopicity"
        )

    with col2:

        permeability = st.text_input(
            "Permeability"
        )

        stability = st.text_area(
            "Known stability / degradation information"
        )

        dose = st.text_input(
            "Dose"
        )

    if st.button("Analyze Properties →", type="primary"):

        st.session_state["properties_submitted"] = True

        st.success(
            "API properties submitted. Formulation analysis unlocked."
        )


# ============================================================
# MASTER ANALYSIS
# ============================================================

if st.session_state.get("properties_submitted"):

    st.divider()

    st.header(
        f"3️⃣ Formulation Intelligence — "
        f"{st.session_state['api']}"
    )

    tabs = st.tabs([
        "API Analysis",
        "Preformulation",
        "Dosage Form",
        "Detailed Procedure",
        "Excipients",
        "Literature",
        "Evaluation",
        "Stability",
        "Regulatory",
        "Final Report"
    ])


    # ========================================================
    # API ANALYSIS
    # ========================================================

    with tabs[0]:

        st.subheader("API profile")

        p = st.session_state["profile"]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("MW", p.get("mw") or "Research")
        col2.metric("pKa", p.get("pka") or "Research")
        col3.metric("LogP", p.get("logp") or "Research")
        col4.metric("Melting point",
                    p.get("melting_point") or "Research")

        st.write(
            "**Solubility:**",
            p.get("solubility") or "Research required"
        )

        st.write(
            "**BCS:**",
            p.get("bcs") or "Verify from authoritative source"
        )

        st.subheader("Major formulation risks")

        for risk in p["major_risks"]:
            st.warning(risk)


    # ========================================================
    # PREFORMULATION
    # ========================================================

    with tabs[1]:

        st.subheader("Preformulation investigation plan")

        preformulation = [

            ("1. API identity",
             "Confirm identity, purity, assay and API form."),

            ("2. Solubility",
             "Determine equilibrium solubility and, where relevant, "
             "pH–solubility relationship."),

            ("3. Particle size",
             "Characterize PSD because it may influence flow, "
             "surface area and dissolution."),

            ("4. Flow properties",
             "Assess bulk density, tapped density, angle of repose, "
             "Carr Index and Hausner ratio where relevant."),

            ("5. Compressibility",
             "Investigate tabletability, compressibility and "
             "compactibility for solid dosage forms."),

            ("6. Solid state",
             "Assess polymorphism/crystallinity using appropriate "
             "solid-state techniques."),

            ("7. Thermal behavior",
             "Use thermal analysis where relevant to understand "
             "processing and stability."),

            ("8. Hygroscopicity",
             "Determine moisture sensitivity where relevant."),

            ("9. Stability",
             "Investigate degradation pathways and sensitivity "
             "to temperature, humidity, light, oxidation or hydrolysis."),

            ("10. Compatibility",
             "Screen API–excipient compatibility before final formulation.")
        ]

        for title, description in preformulation:

            with st.expander(title):

                st.write(description)

                st.markdown(
                    "**Output:** "
                    "Record experimental result + method + "
                    "acceptance/decision criterion + source."
                )


    # ========================================================
    # DOSAGE FORM
    # ========================================================

    with tabs[2]:

        st.subheader("Choose dosage form")

        dosage_form = st.selectbox(
            "Target dosage form",
            [
                "Tablet",
                "Liquid",
                "Topical"
            ]
        )

        if dosage_form == "Tablet":

            method = st.radio(
                "Manufacturing approach",
                [
                    "Direct Compression",
                    "Wet Granulation",
                    "Dry Granulation"
                ]
            )

            st.success(
                f"Selected: Tablet → {method}"
            )

        elif dosage_form == "Liquid":

            method = st.radio(
                "Liquid approach",
                [
                    "Solution",
                    "Suspension"
                ]
            )

            st.success(
                f"Selected: Liquid → {method}"
            )

        else:

            method = "Cream/Gel"

            st.success(
                "Selected: Topical → Cream/Gel"
            )

        st.session_state["dosage_form"] = dosage_form
        st.session_state["method"] = method


    # ========================================================
    # DETAILED PROCEDURE
    # ========================================================

    with tabs[3]:

        st.subheader("🔬 Detailed development procedure")

        dosage = st.session_state.get(
            "dosage_form",
            "Tablet"
        )

        method = st.session_state.get(
            "method",
            "Direct Compression"
        )

        if dosage in STRATEGIES:

            if method in STRATEGIES[dosage]:

                steps = STRATEGIES[dosage][method]

                for i, step in enumerate(steps, 1):

                    with st.expander(
                        f"Step {i}: {step}"
                    ):

                        st.markdown(
                            "**What to do / investigate**"
                        )

                        st.write(
                            "Define the material, equipment, "
                            "process variable and expected output."
                        )

                        st.markdown(
                            "**What to record**"
                        )

                        st.write(
                            "Material identity • quantity • "
                            "batch information • process condition • "
                            "observation • analytical result"
                        )

                        st.markdown(
                            "**Evidence requirement**"
                        )

                        st.write(
                            "Use API-specific research papers, "
                            "validated development data, pharmacopeial "
                            "methods or applicable regulatory guidance."
                        )

                        st.warning(
                            "Exact quantities, concentrations, "
                            "temperatures and process times should be "
                            "shown as 'reported values' only when "
                             st.info(
    "Exact quantities, concentrations, temperatures, mixing speeds, mixing times, sieve sizes and compression forces must be labelled as reported values only when supported by a verified research paper."
)
