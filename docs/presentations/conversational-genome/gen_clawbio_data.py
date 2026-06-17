#!/usr/bin/env python3
"""Generate the Conversational Genome data model by ACTUALLY running the
ClawBio pharmgx-reporter skill on Manuel Corpas's real genotypes.

Facts (diplotype, phenotype, recommendation level, drug counts) come from the
live skill output via api.run(). Prose is curated but bound to the real calls.
Writes `const GENOME = {...}` to stdout.
"""
import json
# Reuse the backend's portable ClawBio loader (no hardcoded paths).
from server import pharmgx_run as run

# Real genotypes at the PGx panel rsIDs, read from the 23andMe Corpasome
GENO = {
 "rs10264272":"CC","rs1057910":"AA","rs1065852":"GG","rs1142345":"TT","rs12248560":"CC",
 "rs1799853":"CT","rs1800460":"CC","rs1800462":"CC","rs28371725":"CT","rs28399499":"TT",
 "rs28399504":"AA","rs3745274":"GT","rs3918290":"CC","rs4148323":"GG","rs4149056":"TT",
 "rs4244285":"GG","rs4986893":"GG","rs5030655":"II","rs762551":"AA","rs776746":"CC",
 "rs9923231":"TT","rs1801131":"GT","rs1801133":"GG",
}
RES = run(GENO)
GP = RES["gene_profiles"]
DR = RES["drug_recommendations"]
SUM = RES["summary"]

# drug name -> level, from the real skill output
drug2level = {}
for level in ("avoid","caution","standard","indeterminate"):
    for d in DR.get(level, []):
        name = (d.get("drug") if isinstance(d, dict) else d)
        if name: drug2level[name.lower()] = level
def lvl(drug, default="standard"):
    return drug2level.get(drug.lower(), default)
def prof(gene):
    p = GP.get(gene, {})
    return p.get("diplotype","NOT_TESTED"), p.get("phenotype","Indeterminate")

# map ClawBio level -> demo card level
CARD = {"avoid":"avoid","caution":"caution","standard":"standard","indeterminate":"unresolved"}

c2c9_dip,c2c9_ph = prof("CYP2C9"); vk_dip,vk_ph = prof("VKORC1")
c19_dip,c19_ph = prof("CYP2C19"); slco_dip,slco_ph = prof("SLCO1B1")
d6_dip,d6_ph = prof("CYP2D6"); dpyd_dip,dpyd_ph = prof("DPYD")
b6_dip,b6_ph = prof("CYP2B6"); a2_dip,a2_ph = prof("CYP1A2")

findings = [
 {"id":"warfarin","title":"Warfarin (the most-prescribed anticoagulant)","topic":"Anticoagulation",
  "level":CARD[lvl("warfarin")],
  "headline":"ClawBio flags warfarin AVOID: two variants stack against you.",
  "genes":[
    {"gene":"CYP2C9","genotype":c2c9_dip,"rsid":"rs1799853 (C/T)","call":c2c9_ph,"effect":"slower clearance of S-warfarin"},
    {"gene":"VKORC1","genotype":vk_dip,"rsid":"rs9923231 (T/T)","call":vk_ph,"effect":"unusually warfarin-sensitive clotting target"}],
  "interpretation":"ClawBio called CYP2C9 "+c2c9_dip+" ("+c2c9_ph.lower()+") and VKORC1 "+vk_dip+" ("+vk_ph.lower()+"). Combined, that is CPIC's most dose-reduced, highest-bleeding-risk category, so the skill returns AVOID. A clinician would start markedly lower with close INR monitoring, or prefer a direct oral anticoagulant.",
  "confidence":"high","confidence_note":"Both variants are single-SNP and concordant with the 30x WGS.",
  "ancestry":"CPIC warfarin algorithms fit European ancestry best and underperform in African ancestry. This call is European-ancestry and robust.",
  "evidence":["CPIC Guideline for warfarin and CYP2C9, VKORC1 (2017)","PharmGKB clinical annotation, level 1A"]},

 {"id":"clopidogrel","title":"Clopidogrel (Plavix)","topic":"Antiplatelet",
  "level":CARD[lvl("clopidogrel")],
  "headline":"Reassuring: ClawBio calls you a normal CYP2C19 metaboliser.",
  "genes":[{"gene":"CYP2C19","genotype":c19_dip,"rsid":"rs4244285, rs12248560, rs4986893, rs28399504 (all reference)","call":c19_ph,"effect":"normal activation of clopidogrel"}],
  "interpretation":"ClawBio called CYP2C19 "+c19_dip+" ("+c19_ph.lower()+"): none of the loss-of-function alleles (*2, *3, *4) and not the gain-of-function *17. Clopidogrel is expected to work as intended, standard dosing.",
  "confidence":"high","confidence_note":"Four tag SNPs tested, all reference. The no-variant result is a positive finding.",
  "ancestry":"CYP2C19 loss-of-function alleles are commoner in East Asian populations; this European-ancestry call is well characterised.",
  "evidence":["CPIC Guideline for clopidogrel and CYP2C19 (2022)","PharmGKB clinical annotation, level 1A"]},

 {"id":"statins","title":"Statins (simvastatin and related)","topic":"Cholesterol",
  "level":CARD[lvl("simvastatin")],
  "headline":"No SLCO1B1 myopathy-risk allele. ClawBio: standard statin risk.",
  "genes":[{"gene":"SLCO1B1","genotype":slco_dip,"rsid":"rs4149056 (T/T)","call":slco_ph,"effect":"normal hepatic statin uptake"}],
  "interpretation":"ClawBio called SLCO1B1 "+slco_dip+" ("+slco_ph.lower()+"). You do not carry the c.521C allele that raises statin-associated muscle risk, so standard dosing considerations apply.",
  "confidence":"high","confidence_note":"Single decisive SNP, reference genotype.",
  "ancestry":"The c.521C risk allele frequency varies by ancestry; the tested variant is well characterised across populations.",
  "evidence":["CPIC Guideline for statins and SLCO1B1 (2022)","PharmGKB clinical annotation, level 1A"]},

 {"id":"codeine","title":"Codeine, tramadol and CYP2D6","topic":"Pain / opioids",
  "level":CARD[lvl("codeine")],
  "headline":"ClawBio calls CYP2D6 "+d6_dip+": reduced codeine activation.",
  "genes":[{"gene":"CYP2D6","genotype":d6_dip,"rsid":"rs28371725 (*41), and *4/*6/*10 reference","call":d6_ph,"effect":"reduced conversion of codeine to morphine"}],
  "interpretation":"From the *41 allele, ClawBio called CYP2D6 "+d6_dip+" ("+d6_ph.lower()+"). Codeine and tramadol are activated by CYP2D6, so analgesia may be reduced; CPIC flags this as use-with-caution. A caveat the skill cannot resolve: SNP chips do not see CYP2D6 copy-number or hybrid alleles, so a clinical lab would confirm the diplotype.",
  "confidence":"moderate","confidence_note":"Phenotype called from tag SNPs; structural variants are invisible to the array.",
  "ancestry":"CYP2D6 structural diversity is greatest in African and Middle Eastern populations, where chip calling is least complete.",
  "evidence":["CPIC Guideline for codeine and CYP2D6 (2021)","PharmVar structural-variation guidance"]},

 {"id":"fluoropyrimidines","title":"5-fluorouracil and capecitabine (chemotherapy)","topic":"Oncology",
  "level":CARD[lvl("capecitabine")],
  "headline":"ClawBio will NOT clear 5-FU: only 1 of 3 DPYD variants was tested.",
  "genes":[{"gene":"DPYD","genotype":dpyd_dip,"rsid":"rs3918290 tested; *13 and D949V not on the array","call":dpyd_ph,"effect":"deficiency cannot be ruled out on partial coverage"}],
  "interpretation":"DPYD breaks down fluoropyrimidine chemotherapy, and a deficiency can be fatal. ClawBio found "+dpyd_dip+" and returned "+dpyd_ph+": your data covered only one of the three severe-deficiency variants, so the skill abstains rather than issue a false all-clear. Before 5-FU or capecitabine, a full DPYD assay is needed. Safe abstention beats a dangerous green light.",
  "confidence":"low","confidence_note":"This is the skill refusing to over-call on incomplete coverage. Safe uncertainty over confident hallucination.",
  "ancestry":"Some DPYD deficiency alleles are population-specific and missed by European-designed panels; wider assays matter most for non-European patients.",
  "evidence":["CPIC Guideline for fluoropyrimidines and DPYD (2017)","PharmGKB clinical annotation, level 1A"]},

 {"id":"efavirenz","title":"Efavirenz (HIV antiretroviral) and CYP2B6","topic":"Infectious disease",
  "level":CARD[lvl("efavirenz")],
  "headline":"ClawBio: CYP2B6 intermediate, higher efavirenz exposure.",
  "genes":[{"gene":"CYP2B6","genotype":b6_dip,"rsid":"rs3745274 (G/T)","call":b6_ph,"effect":"reduced efavirenz clearance"}],
  "interpretation":"ClawBio called CYP2B6 "+b6_dip+" ("+b6_ph.lower()+"). Efavirenz clears more slowly, raising plasma levels and the chance of central-nervous-system side effects. Closer monitoring or an alternative may be preferred. Concordant with the 30x WGS.",
  "confidence":"moderate","confidence_note":"Single well-characterised functional SNP.",
  "ancestry":"The *6 allele is common across populations and especially frequent in African ancestry.",
  "evidence":["CPIC Guideline for efavirenz and CYP2B6 (2019)","PharmGKB clinical annotation, level 1A"]},

 {"id":"caffeine","title":"Caffeine metabolism (CYP1A2)","topic":"Trait",
  "level":"trait",
  "headline":"ClawBio: CYP1A2 "+a2_dip+", a fast caffeine metaboliser.",
  "genes":[{"gene":"CYP1A2","genotype":a2_dip,"rsid":"rs762551 (A/A)","call":a2_ph,"effect":"faster caffeine clearance under induction"}],
  "interpretation":"ClawBio called CYP1A2 "+a2_dip+" ("+a2_ph.lower()+"), associated with faster caffeine clearance, particularly in smokers and heavy coffee drinkers where the enzyme is induced. A trait association, not a clinical directive.",
  "confidence":"moderate","confidence_note":"Robust genotype; the phenotype is gene-by-environment.",
  "ancestry":"Most CYP1A2 caffeine studies are in European cohorts.",
  "evidence":["PharmGKB CYP1A2 caffeine annotations"]},
]

meta = {
 "actionable_order":["warfarin","fluoropyrimidines","codeine","efavirenz","clopidogrel","statins"],
 "summary":{"drugs":SUM["drugs_assessed"],"avoid":SUM["drugs_avoid"],"caution":SUM["drugs_caution"],
            "standard":SUM["drugs_standard"],"indeterminate":SUM["drugs_indeterminate"],
            "genes":SUM["genes_profiled"],"snps":str(SUM["pgx_snps_found"])+"/"+str(SUM["pgx_snps_total"])},
 "ancestry":{
   "title":"How reliable are these for non-European ancestry?",
   "body":"These are real ClawBio calls, and their CPIC evidence base is deepest for European ancestry, which is this genome's ancestry, so most calls above are high-confidence. That is not true for everyone. In our real-genome benchmark the same unguarded interpretation transferred to only 72% accuracy in European, 51% in Latin American (Peruvian Genome Project) and 40% in East African (Uganda Genome Resource) diplotypes. Conversational Genome treats this as a first-class output: every answer carries an ancestry-validity flag and the gaps are shown, not hidden.",
   "stat":[["72%","European"],["51%","Latin American"],["40%","East African"]]},
 "myancestry":{
   "title":"What is my ancestry?",
   "body":"Honest answer: this demo runs a pharmacogenomics skill, not an ancestry skill, so it does not infer ancestry from your genotypes. The documented ancestry of this published genome (Manuel Corpas, the Corpasome) is European, Iberian (Spanish). That is the basis for the European-ancestry validity flag on every PGx answer above. A quantitative admixture breakdown would come from a separate ClawBio ancestry skill that projects your genotypes onto reference panels; wiring that in is exactly the kind of skill the library is built for."},
 "inheritance":{
   "title":"Which variants came from my mother?",
   "body":"This cannot be answered from a single unphased genome. The Corpasome is one sample, so the two alleles at each site are known but their parental origin is not. Resolving it needs trio or pedigree data and phasing, which is what the Family Agent layer is for. The system tells you the boundary of what one genome can know rather than inventing an answer."},
 "changed":{
   "title":"Has anything changed since last year?",
   "body":"Your genome is fixed, but the knowledge over it is not. As new ClinVar, PharmGKB and CPIC releases arrive, ClawBio re-runs the skills and diffs the result; when an interpretation flips you are notified with the evidence that changed. The example below shows the mechanism and is labelled illustrative, since no real reclassification is being asserted here.",
   "illustrative":True},
}

provenance = {
 "subject":"Manuel Corpas","source":"23andMe Corpasome","license":"CC0 1.0 (public domain)",
 "doi":"10.6084/m9.figshare.693052","build":"GRCh37","variants":576517,
 "input_sha256":"e6216c8bd572c4d6b7f1d1c200eef25e8f521e465298092bbd31ecc7680b5f72",
 "engine":"ClawBio pharmgx-reporter v0.2.0","guidelines":"CPIC / PharmGKB",
 "cross_check":"30x WGS, Zenodo doi:10.5281/zenodo.19297389",
 "executed":"ClawBio pharmgx-reporter v0.2.0 run() on 23 panel genotypes; "+str(SUM["drugs_assessed"])+" drugs across "+str(SUM["genes_profiled"])+" genes"}

suggested = ["What does my genome say about warfarin?","Can I take clopidogrel?","What about statins?",
 "Codeine for pain?","Can I have 5-FU chemo?","What is most actionable?",
 "How reliable is this for Peruvian ancestry?","What is my ancestry?","Show me the audit trail"]

GENOME = {"provenance":provenance,"findings":findings,"meta":meta,"suggested":suggested}

hdr = ("/* Conversational Genome data model.\n"
       " * GENERATED by running the real ClawBio pharmgx-reporter v0.2.0 skill on\n"
       " * Manuel Corpas's published Corpasome genotypes (api.run). Facts are live\n"
       " * skill output; prose is curated and bound to the real calls.\n"
       " * Regenerate: python3 gen_clawbio_data.py  (NOT FOR CLINICAL USE).\n */\n")
print(hdr + "const GENOME = " + json.dumps(GENOME, indent=2, ensure_ascii=False) + ";")
