import streamlit as st
import requests, re
from urllib.parse import quote

st.set_page_config(page_title="API → Formulation Intelligence", page_icon="🧪", layout="wide")

# Evidence base: authoritative guidance + peer-reviewed reviews.
SOURCES = [
    {"type":"ICH/EMA","title":"ICH Q8(R2) Pharmaceutical Development",
     "url":"https://www.ema.europa.eu/en/ich-q8-r2-pharmaceutical-development-scientific-guideline",
     "why":"Pharmaceutical development, formulation development, QbD, risk assessment and design-space concepts."},
    {"type":"FDA","title":"Inactive Ingredients Database (IID)",
     "url":"https://www.fda.gov/drugs/drug-approvals-and-databases/inactive-ingredients-database-download",
     "why":"Approved-product inactive ingredient, route, dosage form and potency information; useful as an excipient screening reference."},
    {"type":"FDA","title":"FDA dissolution resources for immediate-release solid oral dosage forms",
     "url":"https://www.fda.gov/animal-veterinary/new-animal-drug-applications/compilation-fda-guidance-and-resources-in-vitro-dissolution-testing-immediate-release-solid-oral-dosage",
     "why":"Dissolution method development, media/pH, sink conditions, validation and CMC considerations."},
    {"type":"FDA","title":"Q6A Specifications: Test Procedures and Acceptance Criteria",
     "url":"https://www.fda.gov/regulatory-information/search-fda-guidance-documents/q6a-specifications-test-procedures-and-acceptance-criteria-new-drug-substances-and-new-drug-products",
     "why":"Specification and testing concepts for drug substances and drug products."},
    {"type":"PubMed review","title":"Impact of preformulation on drug development",
     "url":"https://pubmed.ncbi.nlm.nih.gov/23534681/",
     "why":"Highlights physicochemical/biopharmaceutical characterization and its role in formulation selection."},
    {"type":"PubMed review","title":"Recent advances and novel strategies in pre-clinical formulation development",
     "url":"https://pubmed.ncbi.nlm.nih.gov/21763367/",
     "why":"Links solubility, partitioning, permeability, BCS, route and formulation strategy."},
    {"type":"PubMed review","title":"Drug carrier systems for solubility enhancement of BCS class II drugs",
     "url":"https://pubmed.ncbi.nlm.nih.gov/23614647/",
     "why":"Reviews solubility/dissolution enhancement approaches such as particle engineering, pH modification, cosolvents, surfactants and solid dispersion."},
]

DEMO = {
"ibuprofen": {"mw":206.28,"pka":4.4,"logp":3.5,"solubility":"Low aqueous solubility; pH dependent",
              "formulation_risk":["Dissolution/solubility limitation","Weak-acid ionization","Solid-state and particle-size effects"],
              "strategies":["pH-aware solubility enhancement","Particle-size engineering","Solid dispersion / other enabling approaches","Conventional IR solid dosage form if dissolution and manufacturability are adequate"]},
"paracetamol": {"mw":151.16,"pka":9.5,"logp":0.5,"solubility":"Moderate aqueous solubility; temperature dependent",
              "formulation_risk":["Dose/solubility relationship should be assessed","Particle size and dissolution","Thermal/process stability"],
              "strategies":["Conventional IR tablet/capsule development","Particle-size and wetting optimization","Liquid formulation only after solubility/stability confirmation"]},
}

def pubmed_search(api, max_results=8):
    q = f'"{api}" AND (formulation OR preformulation OR solubility OR dissolution OR excipient)'
    u = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    r = requests.get(u, params={"db":"pubmed","term":q,"retmode":"json","retmax":max_results}, timeout=15)
    r.raise_for_status()
    ids = r.json()["esearchresult"]["idlist"]
    if not ids: return []
    s = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    rr = requests.get(s, params={"db":"pubmed","id":",".join(ids),"retmode":"json"}, timeout=15)
    rr.raise_for_status()
    data=rr.json()["result"]
    out=[]
    for i in ids:
        x=data.get(i,{})
        out.append({"title":x.get("title",""),"journal":x.get("fulljournalname",""),
                    "year":(x.get("pubdate","") or "")[:4],"pmid":i,
                    "url":f"https://pubmed.ncbi.nlm.nih.gov/{i}/"})
    return out

def strategy_table(p):
    return [
        ("Immediate-release tablet/capsule","Assess first if dose, solubility, flow/compressibility and dissolution are manageable.",
         "Blend/granulation/compression or encapsulation; verify CQAs and dissolution."),
        ("Solution/suspension","Consider when liquid dosage form is clinically appropriate and solubility/stability support it.",
         "Vehicle/pH, physical stability, microbial control where relevant."),
        ("Solubility/dissolution enhancement","Prioritize when poor dissolution or aqueous solubility is rate limiting.",
         "Salt/pH modification, particle engineering, surfactant/cosolvent systems, solid dispersion or other evidence-supported technologies."),
        ("Modified release","Consider only when pharmacokinetic/clinical rationale supports controlled release.",
         "Polymer/release mechanism, dose dumping risk, discriminatory dissolution and stability.")
    ]

st.title("🧪 API → Formulation Intelligence")
st.caption("Research-backed formulation-development decision-support prototype")

with st.sidebar:
    st.header("Project settings")
    route = st.selectbox("Route", ["Oral","Topical","Parenteral","Inhalation","Other"])
    dosage = st.selectbox("Target dosage form", ["Auto-select","Tablet","Capsule","Solution","Suspension","Cream/Gel","Injection","Modified release"])
    country = st.selectbox("Regulatory context", ["General / ICH","India","US FDA","EU"])
    st.divider()
    st.info("The app separates known facts, literature evidence and model inference. Missing data is flagged rather than invented.")

api = st.text_input("API name", placeholder="e.g., ibuprofen")
col1,col2,col3 = st.columns(3)
with col1: mw_in=st.number_input("MW (g/mol, optional)", min_value=0.0, value=0.0)
with col2: pka_in=st.number_input("pKa (optional)", min_value=0.0, value=0.0)
with col3: logp_in=st.number_input("LogP (optional)", value=0.0)

if st.button("🔎 Analyze API", type="primary") and api.strip():
    key=api.strip().lower()
    p=DEMO.get(key, {})
    mw=mw_in or p.get("mw")
    pka=pka_in or p.get("pka")
    logp=logp_in or p.get("logp")
    st.session_state["api"]=api.strip()
    st.session_state["profile"]={"mw":mw,"pka":pka,"logp":logp,
                                 "solubility":p.get("solubility","Not supplied — literature/experimental research required"),
                                 "risk":p.get("formulation_risk",["Complete API characterization before selecting a formulation strategy."])}
    st.session_state["strategies"]=p.get("strategies",[])
    try:
        st.session_state["papers"]=pubmed_search(api.strip())
    except Exception as e:
        st.session_state["papers"]=[]
        st.warning("PubMed search could not be completed in this session. The evidence framework remains available.")

if "profile" in st.session_state:
    p=st.session_state["profile"]
    st.subheader(f"API profile — {st.session_state['api']}")
    a,b,c,d=st.columns(4)
    a.metric("MW", p["mw"] if p["mw"] else "Research required")
    b.metric("pKa", p["pka"] if p["pka"] else "Research required")
    c.metric("LogP", p["logp"] if p["logp"] else "Research required")
    d.metric("Solubility", "See assessment")
    st.write("**Solubility:**", p["solubility"])

    st.subheader("1. Preformulation assessment")
    for x in p["risk"]: st.warning(x)
    st.markdown("**Minimum characterization checklist:**")
    st.write("Identity • assay/related substances • solid state/polymorph • particle-size distribution • water content/hygroscopicity • solubility vs pH • pKa • partitioning • permeability where relevant • degradation pathways • API–excipient compatibility.")

    st.subheader("2. Dosage-form / formulation strategies")
    rows = strategy_table(p)
    if p.get("strategies"):
        rows=[r for r in rows if r[0] in p["strategies"]] + [r for r in rows if r[0] not in p["strategies"]]
    st.dataframe({"Strategy":[r[0] for r in rows],"When to investigate":[r[1] for r in rows],"Development questions":[r[2] for r in rows]}, use_container_width=True, hide_index=True)

    st.subheader("3. Excipient screening engine")
    exc=[
      ("Diluent/filler","Dose, flow, compressibility, compatibility"),
      ("Binder","Granule strength and process robustness"),
      ("Disintegrant","Disintegration and dissolution performance"),
      ("Lubricant/glidant","Ejection, flow and manufacturability"),
      ("Surfactant","Wetting/solubilization when justified"),
      ("Polymer","Release control or amorphous/solid-dispersion strategy where justified"),
      ("Buffer/pH modifier","Ionization and solubility/stability control"),
      ("Preservative/antioxidant","Only where route, formulation and degradation risk justify it")
    ]
    st.dataframe({"Excipient function":[x[0] for x in exc],"Screening rationale":[x[1] for x in exc]},use_container_width=True,hide_index=True)
    st.caption("Production version should cross-check route, dosage form and potency against the current FDA IID or the applicable regional excipient/compendial framework.")

    st.subheader("4. Solvent / vehicle research")
    st.write("The engine should retrieve API-specific solubility data and rank vehicles by evidence, route suitability, concentration, safety/quality status, compatibility and stability. It should not invent a solvent or concentration when evidence is absent.")
    st.write("Key variables: water solubility • pH-solubility profile • pKa • cosolvent/vehicle evidence • precipitation risk • API stability • excipient compatibility • intended route.")

    st.subheader("5. Development roadmap")
    roadmap=["API characterization","Preformulation","API–excipient compatibility","Prototype formulation","Process selection","DoE / optimization","Analytical method development","Performance testing","Stability studies","Scale-up / process validation","Regulatory CMC documentation"]
    for i,x in enumerate(roadmap,1): st.markdown(f"**{i}. {x}** →")

    st.subheader("6. Evaluation / CQA checklist")
    st.write("Assay • content uniformity • related substances • dissolution/release • disintegration where applicable • hardness/friability for tablets • pH/viscosity for liquids where relevant • particle-size/sedimentation for suspensions • microbial quality where relevant • moisture • appearance • stability.")
    st.caption("FDA resources describe dissolution as a tool for formulation evaluation and QC; media should consider formulation properties, solubility and API stability, and methods should be scientifically sound and discriminatory.")

    st.subheader("7. Regulatory / documentation")
    st.write(f"Context: **{country}**")
    st.write("Drug substance characterization/specifications • formulation composition • excipient justification • manufacturing process • critical process parameters • controls • finished-product specifications • analytical methods • container closure • stability • development rationale and risk assessment • applicable CTD sections.")
    if country=="US FDA":
        st.info("Use current FDA guidance and the current Inactive Ingredients Database for US-specific checks.")
    elif country=="EU":
        st.info("ICH Q8(R2) is directly relevant to pharmaceutical development and CTD 3.2.P.2.")
    elif country=="India":
        st.info("Production implementation should add current CDSCO/Indian Pharmacopoeia requirements and product-specific rules; verify current official sources before regulatory use.")

    st.subheader("8. Live PubMed evidence")
    papers=st.session_state.get("papers",[])
    if papers:
        for x in papers:
            st.markdown(f"- **{x['title']}** ({x['year']}) — {x['journal']} — [PubMed PMID {x['pmid']}]({x['url']})")
    else:
        st.write("No live results available or search returned no matching papers.")

st.divider()
st.subheader("Core evidence base")
for s in SOURCES:
    st.markdown(f"- **{s['type']} — [{s['title']}]({s['url']})** — {s['why']}")

st.caption("Educational/R&D decision-support only. Literature findings must be checked against the full article, current regulatory requirements, API form/grade, route, dose, and laboratory data. This prototype does not constitute a validated manufacturing formula or regulatory advice.")
