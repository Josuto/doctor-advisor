# Research: source material for `conditions.yaml` and `general_red_flags.yaml`

> **Snapshot.** This file records what the sources said on the retrieval date. Later decisions override parts of it: ICD-10 codes are dropped, the paediatric red flags (`unresponsive_child`, `febrile_young_infant`) and the vertigo + hearing loss variant are removed, and the 4 UNVERIFIED ICD-11 codes are left empty. The conditions knowledge base spec is authoritative.
>
> Contains public sector information licensed under the Open Government Licence v3.0.

Retrieved 2026-10-25. This is source material for a later spec, not a file schema. It uses the vocabulary in `GLOSSARY.md`: Condition, Candidate Condition, Finding, Red Flag, Speciality, Patient. Red flags follow ADR 0002: they are defined once in a normalised catalogue, each one is a combination of required findings, and conditions reference them by id.

**How this was produced**

- **ICD-11 codes.** Every ICD-11 code, title and URI below was checked against WHO's official release file, *ICD-11 MMS Simple Tabulation, release 2026-01* (file header `Version:2026 Jan 17`) [icd11-file]. Each one can be opened in the WHO browser at `https://icd.who.int/browse/2026-01/mms/en#<entity-id>`, where the entity id is the last path segment of the URI. The browser loads its content with JavaScript, so it could not be scraped. The release file it is built from was used instead [icd11-browser].
- **ICD-10 codes.** Every ICD-10 code and title was checked live against the WHO ICD-10 2019 browser's own JSON endpoint (`icd.who.int/browse10/2019/en/JsonGetConcept?ConceptId=…`). Each one can be opened at `https://icd.who.int/browse10/2019/en#/<code>` [icd10-browser].
- **Clinical content.** Clinical claims come from nhs.uk condition and symptom pages, fetched as server-rendered HTML on the date above. Where nhs.uk has no page, they come from MedlinePlus. Each condition block names its sources.
- **Lay phrasings are not sourced.** I wrote the lay phrasings (§4) from the NHS plain-English wording plus common colloquial variants. Treat them as **author-generated** and validate them against real symptom descriptions and the red-flag eval.

---

## 1. Sources and licensing

| Source | Used for | Reuse terms | Implication |
|---|---|---|---|
| **WHO ICD-11 MMS** [icd11-file] | Codes, titles, URIs | **CC BY-ND 3.0 IGO**. Commercial use is allowed if the codes are not adapted and the work is cited [who-class-licence]. The ICD-11 licence says that incorporating the codes into software is not an adaptation. It also says (1.2.3): *"Incorporation of Classifications into a software product, in data transmission and storage must include Classifications code, title and URI"*, and (1.2.4): *"Mapping or producing crosswalks between other classifications and terminologies and Classifications … are not covered by the Classifications License and are subject to a separate written agreement from WHO."* [icd11-licence] | Store the **code, title and URI** together for ICD-11. Section 6 has a judgement call on clause 1.2.4. |
| **WHO ICD-10 (2019)** [icd10-browser] | Codes, titles | WHO holds the copyright. WHO's ICD-10 licensing FAQ says: *"WHO is able to issue commercial licences to companies wishing to incorporate and distribute WHO classifications in their software products … Licensees are not permitted to modify, translate or amend the codes or descriptions"* [who-icd10-faq]. That FAQ is undated and may predate the CC BY-ND classifications page. | ICD-10 in a commercial product may need a WHO licence. Confirm with licensing@who.int, or store ICD-11 only. |
| **NHS website (nhs.uk)** [nhs-terms] | Symptoms, red flags, urgency | Content is released under the **Open Government Licence v3.0**, except images, logos, third-party material and "medical devices". Clause 3.6(b) covers adapted content: *"you must include the standard attribution 'Contains public sector information licensed under the Open Government Licence v3.0.' … You must not attribute the content to the NHS website or cite the NHS specifically as the source of the adapted, updated or non-refreshed content."* The terms also say that adapting content may invalidate its clinical approval [nhs-terms]. | Our YAML is an **adaptation**. In the app, show the OGL statement, not "from the NHS". Keep NHS URLs internally for provenance only. Do not reuse NHS images or symptom-checker tools. |
| **MedlinePlus** [mlp-using] | Strep throat, viral gastroenteritis, subconjunctival haemorrhage, BPPV, swimmer's ear, ectopic heartbeat | Health-topic summaries are public domain. **The Medical Encyclopedia (`/ency/` pages) is A.D.A.M. copyrighted content.** Reuse beyond fair use needs written permission from A.D.A.M. [mlp-using]. | Every MedlinePlus page cited here is an `/ency/` page. Use the **facts**, write our own wording, and never copy the text. |
| **NICE CKS** | Not used | The NICE UK open content licence is UK-only. Its page says CKS is *"not covered by the terms of this licence"* and to contact Agilio Software for permission [nice-open]. NICE content is not intended for use outside the UK without agreement [nice-terms]. | Not used. Licensing risk for a non-UK insurer. |
| **SNOMED CT** | Skipped (confirmed) | Free in SNOMED International Member countries. *"Charges may apply for affiliate use of SNOMED CT in non-Member territories"*, and web applications need special permission [snomed-get]. | Skipped as planned. It would need an Affiliate Licence and, in non-Member countries, fees. |

---

## 2. Condition list (53)

The 15 existing conditions are marked ★. Speciality ids match the app's list. The urgency values are judgement calls taken from the NHS "see a pharmacist / GP / urgent GP" tiers. Here, *self-care* means pharmacy or home care is the first line, *routine* means a GP or specialist appointment, and *urgent* means the NHS says to get an urgent GP appointment or call 111 for the typical presentation.

| # | id | Preferred name | Speciality | Urgency | ICD-11 (2026-01) | ICD-10 (2019) |
|---|---|---|---|---|---|---|
| 1 | `common_cold` ★ | Common cold | general_practitioner | self-care | CA00 Acute nasopharyngitis | J00 Acute nasopharyngitis [common cold] |
| 2 | `influenza` ★ | Flu (influenza) | general_practitioner | self-care | 1E32 Influenza, virus not identified | J11.1 Influenza with other respiratory manifestations, virus not identified |
| 3 | `covid_19` | COVID-19 | general_practitioner | self-care | RA01.0 COVID-19, virus identified | U07.1 COVID-19, virus identified |
| 4 | `strep_throat` ★ | Strep throat | general_practitioner | routine | 1B51 Streptococcal pharyngitis | J02.0 Streptococcal pharyngitis |
| 5 | `gastroenteritis` ★ | Gastroenteritis (stomach bug) | general_practitioner | self-care | 1A40.Z Infectious gastroenteritis or colitis without specification of infectious agent | A09.0 Other and unspecified gastroenteritis and colitis of infectious origin |
| 6 | `dehydration` ★ | Dehydration | general_practitioner | self-care | 5C70.0 Dehydration | E86 Volume depletion (includes "Dehydration") |
| 7 | `insomnia` ★ | Insomnia | general_practitioner | routine | 7A0Z Insomnia disorders, unspecified | G47.0 Disorders of initiating and maintaining sleep [insomnias] |
| 8 | `motion_sickness` ★ | Motion sickness | general_practitioner | self-care | NF08.3 Motion sickness | T75.3 Motion sickness |
| 9 | `tension_headache` ★ | Tension headache | general_practitioner | self-care | 8A81.Z Tension-type headache, unspecified | G44.2 Tension-type headache |
| 10 | `acute_bronchitis` ★ | Bronchitis (acute) | general_practitioner | self-care | CA42.Z Acute bronchitis, unspecified | J20.9 Acute bronchitis, unspecified |
| 11 | `urinary_tract_infection` | Urinary tract infection (UTI) | general_practitioner | routine | GC08.Z Urinary tract infection, site and agent not specified | N39.0 Urinary tract infection, site not specified |
| 12 | `asthma` | Asthma | pulmonology | routine | CA23.32 Unspecified asthma, uncomplicated | J45.9 Asthma, unspecified |
| 13 | `copd` | Chronic obstructive pulmonary disease | pulmonology | routine | CA22.Z Chronic obstructive pulmonary disease, unspecified | J44.9 Chronic obstructive pulmonary disease, unspecified |
| 14 | `pneumonia` | Pneumonia | pulmonology | urgent | CA40.Z Pneumonia, organism unspecified | J18.9 Pneumonia, unspecified |
| 15 | `obstructive_sleep_apnoea` | Obstructive sleep apnoea | pulmonology | routine | 7A41 Obstructive sleep apnoea | G47.3 Sleep apnoea |
| 16 | `gord` ★ | Acid reflux / GORD | digestive | self-care | DA22.Z Gastro-oesophageal reflux disease, unspecified | K21.9 Gastro-oesophageal reflux disease without oesophagitis |
| 17 | `irritable_bowel_syndrome` | Irritable bowel syndrome (IBS) | digestive | routine | DD91.0Z Irritable bowel syndrome, type unspecified | K58.8 Other and unspecified irritable bowel syndrome |
| 18 | `constipation` | Constipation | digestive | self-care | ME05.0 Constipation (alt. DD91.1 Functional constipation) | K59.0 Constipation |
| 19 | `gallstones` | Gallstones | digestive | urgent | DC11.Z Cholelithiasis, unspecified | K80.2 Calculus of gallbladder without cholecystitis |
| 20 | `peptic_ulcer` | Stomach (peptic) ulcer | digestive | routine | DA61 Peptic ulcer, site unspecified | K27.9 Peptic ulcer, site unspecified: unspecified as acute or chronic, without haemorrhage or perforation |
| 21 | `coeliac_disease` | Coeliac disease | digestive | routine | DA95 Coeliac disease | K90.0 Coeliac disease |
| 22 | `conjunctivitis` ★ | Conjunctivitis (pink eye) | ophthalmology | self-care | 9A60.Z Conjunctivitis, unspecified | H10.9 Conjunctivitis, unspecified |
| 23 | `dry_eye` | Dry eyes | ophthalmology | self-care | **UNVERIFIED**. Best title match: 9A79 Keratoconjunctivitis sicca | H04.1 Other disorders of lacrimal gland (Incl.: "Dry eye syndrome") |
| 24 | `stye` | Stye (hordeolum) | ophthalmology | self-care | 9A01.2Z Hordeolum, unspecified | H00.0 Hordeolum and other deep inflammation of eyelid |
| 25 | `blepharitis` | Blepharitis | ophthalmology | self-care | **UNVERIFIED**. No generic category; candidates are 9A02.1 Posterior blepharitis and 9A01.3 Infectious blepharitis | H01.0 Blepharitis |
| 26 | `subconjunctival_haemorrhage` | Subconjunctival haemorrhage (burst blood vessel in the eye) | ophthalmology | self-care | 9A61.5 Conjunctival or subconjunctival haemorrhage | H11.3 Conjunctival haemorrhage |
| 27 | `allergic_rhinitis` ★ | Hay fever / seasonal allergic rhinitis | allergist | self-care | CA08.00 Allergic rhinitis due to pollen | J30.1 Allergic rhinitis due to pollen |
| 28 | `food_allergy` | Food allergy | allergist | routine | 4A85.2Z Food hypersensitivity, unspecified | T78.1 Other adverse food reactions, not elsewhere classified (imperfect fit, see §6) |
| 29 | `urticaria` | Hives (urticaria) | allergist | self-care | EB00.0 Acute urticaria | L50.9 Urticaria, unspecified |
| 30 | `angioedema` | Angioedema | allergist | urgent | **UNVERIFIED**. Candidates: EB04 Idiopathic angioedema, 4A85.21 Food-induced urticaria or angioedema, 4A00.14/4A00.15 Hereditary/Acquired angioedema | T78.3 Angioneurotic oedema |
| 31 | `hypertension` | High blood pressure | cardiology | routine | BA00.Z Essential hypertension, unspecified | I10 Essential (primary) hypertension |
| 32 | `atrial_fibrillation` | Atrial fibrillation | cardiology | routine | BC81.3Z Atrial fibrillation, unspecified | I48.9 Atrial fibrillation and atrial flutter, unspecified |
| 33 | `angina` | Angina | cardiology | urgent | BA40.Z Angina pectoris, unspecified | I20.9 Angina pectoris, unspecified |
| 34 | `heart_failure` | Heart failure | cardiology | urgent | BD1Z Heart failure, unspecified | I50.9 Heart failure, unspecified |
| 35 | `ectopic_beats` | Ectopic heartbeats (palpitations) | cardiology | routine | BC60 Atrial premature depolarization / BC70 Ventricular premature depolarization | I49.4 Other and unspecified premature depolarization |
| 36 | `migraine` ★ | Migraine | neurology | routine | 8A80.Z Migraine, unspecified | G43.9 Migraine, unspecified |
| 37 | `cluster_headache` | Cluster headache | neurology | routine | **UNVERIFIED**. 8A82 Trigeminal autonomic cephalalgias (a leaf in MMS; no separate "cluster headache" category) | G44.0 Cluster headache syndrome |
| 38 | `carpal_tunnel_syndrome` | Carpal tunnel syndrome | neurology | routine | 8C10.0 Carpal tunnel syndrome | G56.0 Carpal tunnel syndrome |
| 39 | `bells_palsy` | Bell's palsy | neurology | urgent | 8B88.0 Bell palsy | G51.0 Bell palsy |
| 40 | `restless_legs_syndrome` | Restless legs syndrome | neurology | routine | 7A80 Restless legs syndrome | G25.8 Other specified extrapyramidal and movement disorders (Incl.: "Restless legs syndrome") |
| 41 | `atopic_eczema` ★ | Eczema (atopic dermatitis) | dermatology | routine | EA80.Z Atopic eczema, unspecified | L20.9 Atopic dermatitis, unspecified |
| 42 | `psoriasis` | Psoriasis | dermatology | routine | EA90.0 Plaque psoriasis | L40.0 Psoriasis vulgaris |
| 43 | `acne` | Acne | dermatology | self-care | ED80.Z Acne, unspecified | L70.0 Acne vulgaris |
| 44 | `contact_dermatitis` | Contact dermatitis | dermatology | self-care | EK00 Allergic contact dermatitis / EK02 Irritant contact dermatitis (no generic category) | L25.9 Unspecified contact dermatitis, unspecified cause |
| 45 | `athletes_foot` | Athlete's foot | dermatology | self-care | 1F28.2 Dermatophytosis of foot | B35.3 Tinea pedis |
| 46 | `shingles` | Shingles | dermatology | urgent | 1E91.0 Zoster without complications | B02.9 Zoster without complication |
| 47 | `sinusitis` ★ | Sinusitis | otolaryngology | self-care | CA01 Acute sinusitis | J01.9 Acute sinusitis, unspecified |
| 48 | `tonsillitis` | Tonsillitis | otolaryngology | self-care | CA03.Z Acute tonsillitis, unspecified | J03.9 Acute tonsillitis, unspecified |
| 49 | `otitis_media` | Middle ear infection | otolaryngology | self-care | AB00 Acute otitis media | H66.9 Otitis media, unspecified |
| 50 | `otitis_externa` | Outer ear infection (swimmer's ear) | otolaryngology | routine | AA3Z Otitis externa, unspecified | H60.9 Otitis externa, unspecified |
| 51 | `earwax_build_up` | Earwax build-up | otolaryngology | self-care | AA42 Impacted cerumen | H61.2 Impacted cerumen |
| 52 | `bppv` | Benign paroxysmal positional vertigo (BPPV) | otolaryngology | routine | AB31.2 Benign positional paroxysmal vertigo | H81.1 Benign paroxysmal vertigo |
| 53 | `labyrinthitis` | Labyrinthitis / vestibular neuritis | otolaryngology | routine | AB30.1 Labyrinthitis (vestibular neuritis: AB30.0) | H83.0 Labyrinthitis (vestibular neuritis: H81.2 Vestibular neuronitis) |

**Count by speciality:** general_practitioner 11, pulmonology 4, digestive 6, ophthalmology 5, allergist 4, cardiology 5, neurology 5, dermatology 6, otolaryngology 7.

**Groups with overlapping symptoms, for discrimination:**
- **Headache:** tension, migraine, cluster, sinusitis, plus headache in flu and hay fever.
- **Cough / breathlessness:** cold, flu, COVID-19, bronchitis, pneumonia, asthma, COPD, heart failure, GORD (recurring cough).
- **Sore throat:** cold, strep throat, tonsillitis, flu.
- **Abdominal:** gastroenteritis, IBS, constipation, gallstones, peptic ulcer, coeliac, GORD, food allergy.
- **Red / irritated eye:** conjunctivitis, dry eye, blepharitis, stye, subconjunctival haemorrhage, hay fever, cluster headache.
- **Itchy skin / rash:** atopic eczema, contact dermatitis, psoriasis, hives, athlete's foot, shingles.
- **Dizziness / vertigo:** BPPV, labyrinthitis, motion sickness, earwax, dehydration, AF.
- **Palpitations / chest:** AF, ectopic beats, angina, GORD.
- **Ear:** otitis media, otitis externa, earwax, labyrinthitis.

**ICD-11 URIs**, all under `http://id.who.int/icd/release/11/mms/`, in table order. Each URI was checked against the release file:
CA00 `2066255370` · 1E32 `1235618695` · RA01.0 `1790791774` · 1B51 `1642172022` · 1A40.Z `1688127370/unspecified` · 5C70.0 `578744597` · 7A0Z `1038292737/unspecified` · NF08.3 `1078108554` · 8A81.Z `1410019257/unspecified` · CA42.Z `727572936/unspecified` · GC08.Z `1848472780/unspecified` · CA23.32 `577724120` · CA22.Z `133207228/unspecified` · CA40.Z `142052508/unspecified` · 7A41 `1919233290` · DA22.Z `1391387859/unspecified` · DD91.0Z `1158238623/unspecified` · ME05.0 `502284069` · DC11.Z `1268183934/unspecified` · DA61 `1145813715` · DA95 `2005943638` · 9A60.Z `831696556/unspecified` · 9A79 `1067300253` · 9A01.2Z `1259721857/unspecified` · 9A02.1 `1248470145` · 9A61.5 `861564880` · CA08.00 `704335372` · 4A85.2Z `1028477872/unspecified` · EB00.0 `24521776` · EB04 `330898059` · BA00.Z `761947693/unspecified` · BC81.3Z `171698302/unspecified` · BA40.Z `718946808/unspecified` · BD1Z `1458683894/unspecified` · BC60 `1661573494` · BC70 `1928266781` · 8A80.Z `669367341/unspecified` · 8A82 `607078588` · 8C10.0 `1275186848` · 8B88.0 `2004402146` · 7A80 `1254916765` · EA80.Z `215767047/unspecified` · EA90.0 `1088800108` · ED80.Z `1892393023/unspecified` · EK00 `2020673786` · EK02 `195009390` · 1F28.2 `1993674550` · 1E91.0 `1659043996` · CA01 `509821856` · CA03.Z `260431605/unspecified` · AB00 `476505279` · AA3Z `1303990434/unspecified` · AA42 `643255245` · AB31.2 `1300772836` · AB30.1 `901550793` · AB30.0 `958752541`.

---

## 3. Recommended additional specialities (not added)

The app's speciality list is not extended here. These cases would justify a new speciality:
- **Psychiatry / clinical psychology.** Insomnia is often linked to anxiety and depression, and the `suicidal_crisis` general red flag has nowhere to route a non-emergency follow-up. Today it would have to go to general_practitioner.
- **Urology / gynaecology.** Recurrent UTIs, and UTIs in men, are both NHS urgent-GP triggers [nhs-uti]. Today they go to general_practitioner.
- **Rheumatology.** Psoriasis with joint pain, stiffness or swelling is an NHS "see a GP" trigger [nhs-psoriasis].
- **Trauma / orthopaedics.** Back pain was left out, both for this reason and because the `cauda_equina_syndrome` general red flag covers its emergency presentation [nhs-back].
- **Endocrinology.** There is no endocrine condition in the list. DKA appears only as a general red flag [nhs-dka].

---

## 4. Findings lexicon (shared across conditions and red flags)

Each Finding has an id and lay phrasings. Phrasings are written in **base (lemma) forms**, so that "coughing up blood", "coughed up blood" and "cough up blood" all match `cough up blood`. US spellings are added where they differ. All phrasings are author-generated (see the note at the top).

| Finding id | Lay phrasings (base forms) |
|---|---|
| `runny_nose` | runny nose · nose run · drippy nose · snot · nose keep run |
| `blocked_nose` | blocked nose · stuffy nose · congested · can't breathe through nose · bunged up |
| `sneezing` | sneeze · keep sneeze · sneezing fit |
| `sore_throat` | sore throat · throat hurt · scratchy throat · throat pain |
| `painful_swallowing` | hurt to swallow · pain when swallow · difficult to swallow · swallowing hurt |
| `hoarse_voice` | hoarse · croaky voice · lose voice · raspy voice |
| `cough` | cough · keep cough · hacking cough |
| `dry_cough` | dry cough · tickly cough · nothing come up when cough |
| `productive_cough` | cough up phlegm · cough up mucus · chesty cough · green phlegm · yellow phlegm |
| `continuous_cough` | constant cough · cough for more than an hour · cough fit · new continuous cough |
| `fever` | fever · high temperature · temperature · feel hot · hot and cold · shivery · chills · shiver |
| `tiredness` | tired · exhausted · no energy · fatigue · worn out · wiped out |
| `muscle_aches` | aching body · body ache · muscle ache · ache all over · sore muscles |
| `headache` | headache · head hurt · head ache · head pain · pounding head |
| `loss_of_smell_or_taste` | lose sense of smell · can't smell · can't taste · food taste different · no taste |
| `ear_or_face_pressure` | pressure in ear · pressure in face · face feel full · ear feel pressure |
| `loss_of_appetite` | not hungry · lose appetite · off food · don't feel like eat |
| `trouble_falling_asleep` | can't fall asleep · can't get to sleep · lie awake · toss and turn |
| `night_waking` | wake up in the night · wake up several times · keep wake up at night |
| `early_waking` | wake up too early · wake early and can't get back to sleep |
| `unrefreshing_sleep` | wake up tired · still tired after sleep · never feel rested |
| `daytime_sleepiness` | sleepy during the day · tired all day · nod off · groggy |
| `poor_concentration` | can't concentrate · can't focus · brain fog |
| `irritability` | irritable · snappy · grumpy · mood swing |
| `diarrhoea` | diarrhoea · diarrhea · the runs · loose stool · watery poo · runny poo |
| `nausea` | feel sick · nausea · nauseous · queasy · want to throw up |
| `vomiting` | vomit · be sick · throw up · puke · can't keep anything down |
| `abdominal_pain` | stomach ache · tummy ache · stomach pain · belly pain · abdominal pain · stomach cramp |
| `upper_abdominal_burning_pain` | burning pain at top of stomach · gnawing stomach pain · pain under breastbone · upper stomach pain |
| `right_upper_abdominal_pain` | pain under right rib · pain upper right tummy · right side under rib |
| `pain_relieved_by_pooing` | pain better after poo · cramp ease after toilet |
| `bloating` | bloat · bloated · swollen tummy · stomach feel full · puffy belly |
| `flatulence` | fart · wind · gas · pass gas |
| `constipation_hard_stool` | constipated · can't poo · hard poo · lumpy poo · strain on the toilet · not poo for days |
| `incomplete_emptying` | not fully empty · still need to go after toilet |
| `mucus_in_stool` | mucus in poo · slime in stool |
| `heartburn` | heartburn · burning chest after eat · acid in chest · burning behind breastbone |
| `acid_regurgitation` | sour taste · acid come up · bitter taste in mouth · bring up food · regurgitate |
| `burping` | burp · belch |
| `thirst` | thirsty · very thirsty · always thirsty |
| `dry_mouth` | dry mouth · dry lips · dry tongue |
| `dark_urine` | dark pee · dark yellow pee · dark urine · strong smell pee |
| `reduced_urination` | pee less · hardly pee · not pee much |
| `dizziness` | dizzy · light-headed · lightheaded · woozy · feel faint |
| `vertigo` | room spin · everything spin · spinning · vertigo · world spin |
| `loss_of_balance` | unsteady · off balance · lose balance · can't walk straight |
| `sunken_eyes` | sunken eyes · eyes look sunken |
| `sweating` | sweat · sweaty · clammy · cold sweat |
| `pallor` | pale · go white · look pale · grey face |
| `travel_trigger` | in the car · on a boat · on a plane · on the train · when travel · seasick · carsick |
| `band_like_headache` | tight band round head · pressure on head · head in a vice · pain both sides of head |
| `scalp_tenderness` | scalp tender · scalp sore · head hurt to touch |
| `throbbing_one_sided_headache` | throbbing headache · pounding one side · pulsing headache · headache on one side |
| `photophobia` | light hurt eyes · sensitive to light · bright light bother · can't look at light |
| `phonophobia` | sensitive to noise · noise hurt · can't stand sound |
| `visual_aura` | zigzag lines · flashing lights · blind spot · see sparkle |
| `pins_and_needles` | pins and needles · tingling · tingle · prickle |
| `numbness` | numb · no feeling · can't feel |
| `one_sided_eye_pain` | pain around one eye · stabbing pain behind eye · burning pain in eye socket |
| `restless_during_pain` | can't sit still · pace around · rock back and forth |
| `attacks_at_set_times` | same time every day · same time of year · come in clusters · wake me at the same time |
| `red_watery_eye_one_side` | one eye red and water · eye water on same side |
| `droopy_eyelid` | eyelid droop · droopy eyelid · eyelid hang down |
| `unequal_pupils` | one pupil bigger · pupils different size · small pupil one side |
| `shortness_of_breath` | short of breath · breathless · out of breath · can't catch breath · hard to breathe |
| `breathless_lying_down` | breathless lying down · can't breathe lying flat · need extra pillows |
| `wheezing` | wheeze · whistling breath · whistling chest |
| `chest_tightness` | tight chest · chest feel tight · chest feel heavy |
| `chest_pain` | chest pain · pain in chest · chest hurt · chest ache · pressure in chest · squeezing chest · crushing chest |
| `chest_pain_on_cough_or_breath` | chest hurt when cough · hurt to breathe in · pain when breathe |
| `exertional_chest_pain` | chest pain when walk · chest pain on stairs · chest pain with exercise · go away when rest |
| `pain_radiating_arm_neck_jaw_back` | pain spread to arm · pain down left arm · pain in jaw · pain go to neck · pain go to back |
| `frequent_chest_infections` | keep get chest infections · always have chest infection |
| `swollen_ankles` | swollen ankle · swollen feet · puffy legs · legs swell |
| `sudden_weight_gain` | sudden weight gain · put on weight quickly |
| `night_cough` | cough at night · cough when lie down |
| `pink_frothy_sputum` | frothy pink phlegm · pink foamy spit |
| `snoring` | snore · loud snoring |
| `witnessed_apnoea` | stop breathing in sleep · breathing stop and start · gasp in sleep · choke in sleep · snort awake |
| `morning_headache` | headache when wake up · morning headache |
| `painful_urination` | burn when pee · sting when pee · pain when pee · hurt to wee |
| `frequent_urination` | pee a lot · wee often · keep need the toilet · pee more often |
| `urinary_urgency` | sudden urge to pee · can't hold it · desperate to pee |
| `nocturia` | get up at night to pee · wee at night |
| `cloudy_urine` | cloudy pee · cloudy urine · smelly pee |
| `blood_in_urine` | blood in pee · pink pee · red pee · brown pee |
| `loin_pain` | pain in back under rib · side pain · kidney pain · flank pain |
| `red_eye` | red eye · bloodshot eye · pink eye · eye look red |
| `gritty_eye` | gritty eye · sand in eye · eye burn · eye feel scratchy |
| `sticky_eye_discharge` | sticky eye · pus in eye · crusty eyelash · eyes glue shut · eye discharge |
| `itchy_eyes` | itchy eye · eye itch |
| `watery_eyes` | watery eye · eye stream · eye water |
| `blurred_vision` | blurry vision · blurred vision · can't see clearly · vision fuzzy |
| `eyelid_lump` | lump on eyelid · bump on eyelid · spot on eyelid · pimple on eyelid |
| `swollen_eyelid` | swollen eyelid · puffy eyelid |
| `eyelid_crusting` | flake on eyelash · crusty eyelid · dandruff on lash · eyelids stick together |
| `sore_eyelids` | sore eyelid · eyelid hurt · eyelid burn |
| `red_patch_on_white_of_eye` | red patch on white of eye · blood spot in eye · burst blood vessel in eye |
| `itchy_nose_throat_ears` | itchy throat · itchy mouth · itchy ear · itchy nose · itchy roof of mouth |
| `seasonal_pattern` | every spring · every summer · pollen season · when pollen count high |
| `hives` | hives · raised itchy rash · welt · nettle rash · itchy bump · urticaria |
| `face_lip_swelling` | swollen lip · swollen face · puffy eye · lip swell |
| `swelling_hands_feet_genitals` | swollen hand · swollen foot · swollen genitals |
| `after_eating_trigger` | after eat · after I eat · when I eat nut · after eat shellfish |
| `palpitations` | palpitation · heart race · heart pound · heart flutter · heart thump |
| `irregular_pulse` | irregular heartbeat · pulse all over the place · uneven pulse |
| `fast_heartbeat` | fast heartbeat · heart beat fast · rapid pulse |
| `skipped_beats` | skip a beat · skipped beat · extra beat · heart miss a beat · heart stop for a second |
| `exercise_intolerance` | can't exercise like before · tire quickly when exercise |
| `high_blood_pressure_reading` | high blood pressure · blood pressure high · high reading |
| `hand_numbness_tingling` | numb finger · tingling finger · pins and needles in hand · hand go numb at night |
| `weak_grip` | weak grip · drop things · weak thumb |
| `one_sided_facial_weakness` | face droop · one side of face droop · can't move one side of face · mouth droop · can't smile |
| `drooling` | drool · dribble |
| `urge_to_move_legs` | need to move leg · restless leg · legs won't keep still · creepy crawly leg |
| `itchy_skin` | itchy skin · itch · scratch all the time |
| `dry_cracked_skin` | dry skin · cracked skin · rough skin · flaky skin · scaly skin |
| `discoloured_skin_patches` | red patch · red blotch · dark patch · discoloured patch |
| `silvery_scaly_plaques` | silvery scale · scaly patch on elbow · thick flaky patch |
| `nail_pitting` | pitted nail · dent in nail |
| `joint_pain_swelling` | joint pain · swollen joint · stiff joint |
| `spots` | spot · pimple · zit · blackhead · whitehead · breakout |
| `greasy_skin` | oily skin · greasy skin |
| `painful_skin_lumps` | painful lump under skin · cyst · deep spot |
| `blisters` | blister · fluid-filled blister · weepy skin |
| `rash_after_contact` | rash after use · rash where touch · reaction to new soap · rash from glove · rash from jewellery |
| `itchy_between_toes` | itchy between toes · white skin between toes · peel feet · crack between toes |
| `one_sided_band_rash` | rash on one side · band of blister · stripe rash on one side |
| `localised_skin_pain_tingling` | burning patch of skin · tingling patch of skin · skin hurt to touch |
| `facial_pain_pressure` | pain in cheek · pain around eye · forehead pressure · face hurt when bend down |
| `coloured_nasal_discharge` | green snot · yellow mucus · thick nasal discharge |
| `toothache` | toothache · upper teeth ache |
| `bad_breath` | bad breath · breath smell |
| `swollen_neck_glands` | swollen gland · lump in neck · swollen lymph node |
| `white_patches_on_tonsils` | white spot on tonsil · pus on tonsil · white patch in throat |
| `sandpaper_rash` | rough rash · sandpaper rash |
| `earache` | earache · ear hurt · ear pain · pain in ear |
| `ear_discharge` | ear discharge · fluid come out of ear · pus from ear · ear leak |
| `hearing_loss` | can't hear · muffled hearing · hearing loss · deaf in one ear |
| `ear_fullness` | ear feel blocked · ear full · plugged ear |
| `ear_itch` | itchy ear · ear itch |
| `pain_on_pulling_ear` | hurt when pull ear · ear hurt when touch |
| `tinnitus` | ringing in ear · buzzing in ear · ear ring · tinnitus |
| `head_movement_trigger` | roll over in bed · when look up · when turn head · when tilt head |
| **Red-flag-only findings** | |
| `sudden_onset` | sudden · suddenly · all at once · out of nowhere · in seconds · came on fast |
| `severe_pain` | worst ever · extremely painful · unbearable · excruciating · severe · agony |
| `persistent` | won't go away · not go away · doesn't stop · still there |
| `breathing_struggle` | gasp · choke · can't get words out · can't speak in sentences · struggle to breathe · can't breathe |
| `cyanosis` | blue lips · lips turn blue · grey skin · blue skin · grey lips · blue tongue |
| `mottled_skin` | blotchy skin · mottled skin |
| `cough_up_blood` | cough up blood · blood in phlegm · spit blood |
| `arm_or_side_weakness` | can't lift arm · arm weak · arm numb · weakness down one side · one side of body numb · leg weak |
| `speech_problem` | slur · slurred speech · can't speak properly · words come out wrong · garbled speech · can't find words |
| `stiff_neck` | stiff neck · can't bend neck · neck stiff |
| `non_blanching_rash` | rash not fade under glass · rash not fade when press · purple spot · pinprick rash |
| `confusion` | confused · not make sense · disoriented · don't know where I am · muddled |
| `drowsiness` | very sleepy · drowsy · hard to wake · can't stay awake |
| `seizure` | seizure · fit · convulsion · shake uncontrollably |
| `head_injury` | hit head · head injury · bang head · fall on head |
| `vision_loss` | lose vision · can't see · go blind · double vision · lose sight |
| `memory_problem` | can't remember · memory loss |
| `throat_swelling_or_tightness` | throat swell · throat tight · throat close · tongue swell · struggle to swallow |
| `rapid_breathing` | breathe very fast · quick short breath · pant |
| `no_urine` | not pee all day · no pee · not pass urine |
| `cold_skin` | cold skin · cold to touch · cold hands and feet |
| `vomit_blood` | vomit blood · throw up blood · coffee-ground vomit · sick look like coffee grounds |
| `black_tarry_stool` | black poo · black stool · tar-like poo · sticky black poo |
| `heavy_rectal_bleeding` | lot of blood from bottom · toilet water turn red · blood clot from bottom · bleeding won't stop |
| `green_vomit` | green vomit · green sick · bile vomit |
| `cannot_pass_stool_or_wind` | can't poo or fart · can't pass wind |
| `cannot_pee` | can't pee at all · can't urinate |
| `jaundice` | yellow skin · yellow eye · white of eye yellow |
| `pain_spreading_to_back` | pain go through to back · pain spread to back |
| `unresponsive` | pass out and not wake · unconscious · won't wake up · not respond · collapse |
| `fainting` | faint · pass out · black out |
| `eye_injury_or_foreign_body` | something stuck in eye · glass in eye · grit in eye · hit in the eye · pierce eye |
| `chemical_in_eye` | chemical in eye · bleach in eye · splash in eye |
| `very_dark_red_eye` | eye very dark red · eye deep red |
| `cannot_swallow` | can't swallow · can't swallow spit |
| `stridor` | high-pitched breathing · noisy breathing in · whistle when breathe in · stridor |
| `difficulty_opening_mouth` | can't open mouth · jaw won't open |
| `swelling_in_mouth_or_throat` | swelling in throat · back of throat swollen · swelling in mouth |
| `calf_swelling_or_pain` | swollen calf · painful calf · one leg swollen |
| `asthma_attack` | asthma attack · can't get my breath with asthma |
| `inhaler_not_helping` | inhaler not work · reliever not help · blue inhaler doesn't help |
| `no_inhaler` | no inhaler · lost inhaler · don't have inhaler |
| `widespread_red_skin_with_pustules` | pus-filled bump · white pustule · skin turn red all over · pus spot all over |
| `suicidal_intent` | kill myself · end my life · want to die · suicide · harm myself |
| `self_harm_done` | take an overdose · overdose · cut myself badly · swallow pills |
| `fruity_breath` | breath smell fruity · breath smell like nail polish remover · pear drop breath |
| `high_ketones` | ketones high · high ketone |
| `pregnant_or_missed_period` | pregnant · missed period · period late |
| `back_pain` | back pain · back hurt · lower back pain |
| `saddle_numbness` | numb around bottom · numb genitals · can't feel when I wipe |
| `new_bladder_or_bowel_problem` | can't pee · wet myself · lose control of bowel · poo myself |
| `both_legs_weak_or_numb` | both legs weak · both legs numb · tingling in both legs |
| `floppy_child` | floppy · limp · baby won't wake · not respond like normal |
| `young_infant` | baby under 3 months · newborn · 2-month-old · 8-week-old |

---

## 5. Conditions in detail

Each block gives the definition (plain-language paraphrase), the findings with frequency (`c` = common or main, `o` = occasional or "may also"), red flag references (§7), urgent non-emergency triggers, and sources. Frequency is "n/s" where the source does not rank symptoms. Synonyms and lay names are author-generated.

### general_practitioner

**`common_cold` — Common cold.** *Synonyms:* cold, head cold, coryza, the sniffles.
- *Definition:* A virus infection of the nose and throat. Symptoms come on gradually over 2–3 days, and you usually feel better in 1–2 weeks [nhs-cold].
- *Findings:* c: runny_nose, blocked_nose, sneezing, sore_throat, hoarse_voice, cough, tiredness. o: fever, muscle_aches, loss_of_smell_or_taste, ear_or_face_pressure [nhs-cold].
- *Discriminator:* a cold comes on gradually and affects mainly the nose and throat. Flu comes on within hours and is exhausting [nhs-cold].
- *Red flags:* none at emergency level on the source page.
- *Urgent/GP:* temperature lasting more than 3 days, short of breath or chest pain, cough lasting more than 3 weeks, long-term condition or weakened immunity [nhs-cold].

**`influenza` — Flu.** *Synonyms:* influenza, the flu, flu bug.
- *Definition:* A virus infection whose symptoms come on very quickly. It often gets better on its own but can make some people seriously ill [nhs-flu].
- *Findings (n/s):* fever (sudden), muscle_aches, tiredness, dry_cough, sore_throat, headache, trouble_falling_asleep, loss_of_appetite [nhs-flu].
- *Red flags:* `possible_heart_attack` (variant: sudden chest pain), `severe_breathing_difficulty`, `coughing_up_blood` [nhs-flu].
- *Urgent:* age 65 or over, pregnant, long-term condition, short of breath, not improving after 7 days [nhs-flu].

**`covid_19` — COVID-19.** *Synonyms:* covid, coronavirus, corona.
- *Definition:* A virus infection whose symptoms are very similar to colds and flu. Most people feel better within a few weeks [nhs-covid].
- *Findings (n/s):* fever, continuous_cough, loss_of_smell_or_taste, shortness_of_breath, tiredness, muscle_aches, headache, sore_throat, blocked_nose/runny_nose, loss_of_appetite, diarrhoea, nausea/vomiting [nhs-covid].
- *Red flags:* `possible_heart_attack` (sudden chest pain), `severe_breathing_difficulty`, `coughing_up_blood`, `loss_of_consciousness` (collapse or faint), `first_seizure`, `meningitis_signs` (non-blanching rash) [nhs-covid].
- *Urgent:* high temperature for 5 days or more, symptoms getting worse [nhs-covid].

**`strep_throat` ★ — Strep throat.** *Synonyms:* streptococcal sore throat, strep A throat infection.
- *Definition:* A sore throat caused by group A streptococcus bacteria. Symptoms appear 2–5 days after contact [mlp-strep]. Strep A can also cause tonsillitis, scarlet fever and impetigo [nhs-strepa].
- *Findings:* c: fever (may start suddenly), chills, sore_throat (red, may have white patches → white_patches_on_tonsils), painful_swallowing, swollen_neck_glands. o: tiredness/malaise, loss_of_appetite, headache, nausea, sandpaper_rash [mlp-strep].
- *Red flags:* `upper_airway_obstruction` [nhs-sore-throat], `cyanosis`, `unresponsive_child` [nhs-strepa].
- *Urgent:* very high temperature or shivery, signs of dehydration, weakened immunity [nhs-sore-throat].

**`gastroenteritis` ★ — Gastroenteritis.** *Synonyms:* stomach bug, stomach flu, tummy bug, D&V, norovirus.
- *Definition:* An infection of the gut, usually from a virus such as norovirus or rotavirus. Symptoms usually start 4–48 hours after exposure [mlp-gastro]. Diarrhoea usually stops in 5–7 days and vomiting in 1–2 days [nhs-dv].
- *Findings:* c: diarrhoea, nausea, vomiting, abdominal_pain. o: fever, chills/sweating, muscle_aches [mlp-gastro].
- *Red flags:* `gi_bleeding` (vomit blood or coffee grounds), `acute_abdomen` (green vomit, sudden severe tummy ache), `meningitis_signs` (stiff neck plus light pain), `thunderclap_headache`, `cyanosis`, `severe_breathing_difficulty`, `sudden_confusion` [nhs-dv].
- *Urgent:* cannot keep fluids down, bloody diarrhoea, diarrhoea for more than 7 days or vomiting for more than 2 days [nhs-dv].

**`dehydration` ★ — Dehydration.** *Synonyms:* dehydrated, not drinking enough.
- *Definition:* The body loses more fluid than it takes in. Untreated, it can become serious [nhs-dehydration].
- *Findings (n/s):* thirst, headache, dizziness, dark_urine, reduced_urination, tiredness, dry_mouth, sunken_eyes [nhs-dehydration].
- *Red flags:* `severe_dehydration_shock`, `cyanosis`, `sudden_confusion` [nhs-dehydration].
- *Urgent:* dizzy on standing and it does not go away, peeing less than normal, breathing quickly or fast heart rate [nhs-dehydration].

**`insomnia` ★ — Insomnia.** *Synonyms:* can't sleep, sleeplessness, sleep problems.
- *Definition:* Regular problems sleeping. It is short-term if it lasts less than 3 months and long-term if it lasts 3 months or more [nhs-insomnia].
- *Findings (n/s):* trouble_falling_asleep, night_waking, early_waking, unrefreshing_sleep, daytime_sleepiness, irritability, poor_concentration [nhs-insomnia].
- *Red flags:* none on the source page.
- *GP:* trouble sleeping for months, or it is hard to cope [nhs-insomnia].

**`motion_sickness` ★ — Motion sickness.** *Synonyms:* travel sickness, car sickness, seasickness, airsickness.
- *Definition:* Feeling dizzy, or feeling or being sick, when travelling by car, boat, plane or train [nhs-motion].
- *Findings (n/s):* dizziness, nausea, vomiting, headache, pallor (feeling cold and going pale), sweating, plus the travel_trigger context [nhs-motion].
- *Red flags:* none on the source page.

**`tension_headache` ★ — Tension headache.** *Synonyms:* tension-type headache, stress headache.
- *Definition:* A very common headache. You can usually carry on with daily activities. It lasts at least 30 minutes and can last several days [nhs-tension].
- *Findings:* c: headache, band_like_headache (both sides of head, face or neck), scalp_tenderness [nhs-tension].
- *Discriminator:* a throbbing one-sided headache with nausea or light sensitivity suggests migraine or cluster headache instead [nhs-tension].
- *Red flags:* `thunderclap_headache`, `headache_with_neuro_signs` (including head injury and red eye), `meningitis_signs` [nhs-tension].
- *Urgent:* severe headache with jaw pain when eating, blurred or double vision, sore scalp, or numbness or weakness [nhs-tension].

**`acute_bronchitis` ★ — Bronchitis.** *Synonyms:* chest infection, chesty cough.
- *Definition:* Inflammation of the airways in the lungs, usually from an infection. It often gets better without treatment in about 3 weeks [nhs-bronchitis].
- *Findings (n/s):* productive_cough, chest_pain_on_cough_or_breath, shortness_of_breath, sore_throat, runny_nose, fever [nhs-bronchitis].
- *Red flags:* `severe_breathing_difficulty`, `cyanosis`, `sudden_confusion`, `unresponsive_child` [nhs-bronchitis].
- *Urgent:* cough lasting more than 3 weeks, coughing up blood or blood-stained mucus, chest pain [nhs-bronchitis]. **Conflict:** see §8.

**`urinary_tract_infection` — UTI.** *Synonyms:* cystitis, bladder infection, water infection.
- *Definition:* An infection of the urinary tract, including cystitis (bladder) and kidney infection [nhs-uti].
- *Findings (n/s):* painful_urination, frequent_urination, nocturia, urinary_urgency, cloudy_urine, blood_in_urine, abdominal_pain (lower) or loin_pain, fever, tiredness [nhs-uti].
- *Red flags:* `sudden_confusion` (confused, drowsy or difficulty speaking) [nhs-uti], `possible_sepsis` (kidney infection can cause sepsis) [nhs-uti] [nhs-kidney].
- *Urgent:* men, age 65 or over, pregnant, loin pain, blood in urine, very high or low temperature [nhs-uti].

### pulmonology

**`asthma` — Asthma.** *Synonyms:* asthmatic, wheezy chest.
- *Definition:* A long-term condition affecting breathing. Symptoms come and go and are often worse at night and early morning. Triggers include exercise, cold air and allergens [nhs-asthma].
- *Findings:* c: wheezing, cough, shortness_of_breath, chest_tightness [nhs-asthma].
- *Red flags:* `severe_asthma_attack` [nhs-asthma], `severe_breathing_difficulty` [nhs-sob].
- *Urgent:* GP within 2 days after any asthma attack [nhs-asthma].

**`copd` — COPD.** *Synonyms:* emphysema, chronic bronchitis, smoker's cough.
- *Definition:* A group of lung conditions, including emphysema and chronic bronchitis, that cause breathing difficulties. Symptoms gradually get worse, with flare-ups [nhs-copd] [nhs-copd-symptoms].
- *Findings:* c: shortness_of_breath (on activity), productive_cough, frequent_chest_infections, wheezing. o: weight loss, tiredness, swollen_ankles [nhs-copd-symptoms].
- *Red flags:* `severe_breathing_difficulty`, `cyanosis` [nhs-sob]. The COPD page has no 999 box, so these come from the generic shortness-of-breath page.
- *GP:* persistent symptoms, especially in people over 35 who smoke or used to smoke [nhs-copd-symptoms].

**`pneumonia` — Pneumonia.** *Synonyms:* lung infection, chest infection.
- *Definition:* Inflammation of the lungs, usually caused by an infection [nhs-pneumonia].
- *Findings (n/s):* cough, shortness_of_breath, fever, chest_pain, muscle_aches, tiredness, loss_of_appetite, wheezing, confusion (older people) [nhs-pneumonia].
- *Red flags:* `severe_breathing_difficulty`, `cyanosis`, `coughing_up_blood`, `sudden_confusion`, `unresponsive_child` [nhs-pneumonia].
- *Urgent:* yellow or green phlegm, chest pain on breathing or coughing, short of breath [nhs-pneumonia].

**`obstructive_sleep_apnoea` — Obstructive sleep apnoea.** *Synonyms:* sleep apnoea, sleep apnea, OSA.
- *Definition:* Breathing stops and starts during sleep [nhs-osa].
- *Findings:* c (during sleep): witnessed_apnoea, gasping/snorting, night_waking, snoring. c (daytime): daytime_sleepiness, poor_concentration, irritability (mood swings), morning_headache [nhs-osa].
- *Red flags:* none. *GP:* any main symptom [nhs-osa].

### digestive

**`gord` ★ — Acid reflux / GORD.** *Synonyms:* heartburn, acid reflux, reflux, indigestion, GERD.
- *Definition:* Stomach acid travels up towards the throat. When it keeps happening, it may be called gastro-oesophageal reflux disease [nhs-reflux].
- *Findings:* c: heartburn, acid_regurgitation. o: recurring cough or hiccups, hoarse_voice, bad_breath, bloating, nausea. Worse after eating, lying down or bending over [nhs-reflux].
- *Red flags:* `possible_heart_attack`. Heart-attack chest pain can feel like burning or indigestion [nhs-chest-pain] [nhs-heart-attack].
- *GP:* heartburn most days, food sticking, frequent vomiting, weight loss [nhs-reflux].

**`irritable_bowel_syndrome` — IBS.** *Synonyms:* IBS, irritable bowel, spastic colon.
- *Definition:* A common, usually lifelong condition of the digestive system. It causes cramps, bloating and diarrhoea or constipation, with flare-ups [nhs-ibs] [nhs-ibs-symptoms].
- *Findings:* c: abdominal_pain with pain_relieved_by_pooing, bloating, diarrhoea, constipation_hard_stool. o: flatulence, mucus_in_stool, tiredness, nausea, back pain, urinary symptoms [nhs-ibs-symptoms].
- *Red flags:* none at 999 level. *Urgent:* unexplained weight loss, bleeding from the bottom or bloody diarrhoea, a lump in the tummy [nhs-ibs-symptoms].

**`constipation` — Constipation.** *Synonyms:* blocked up, can't go, bunged up.
- *Definition:* Pooing less often, or finding it hard to poo [nhs-constipation].
- *Findings:* c: constipation_hard_stool (fewer than 3 times a week; dry, hard or lumpy), straining, incomplete_emptying. o: abdominal_pain, bloating, nausea [nhs-constipation].
- *Red flags:* `acute_abdomen` (variant: cannot poo or fart) [nhs-stomach-ache].
- *GP:* blood in poo, weight loss, regular constipation [nhs-constipation].

**`gallstones` — Gallstones.** *Synonyms:* gallbladder stones, biliary colic, gallbladder attack.
- *Definition:* Small stones in the gallbladder. They often cause no symptoms, but can cause tummy pain if they block a bile duct [nhs-gallstones].
- *Findings:* c (when symptomatic): right_upper_abdominal_pain or central abdominal_pain that is severe, constant and lasts more than 30 minutes up to several hours, with nausea/vomiting [nhs-gallstones].
- *Red flags:* `acute_abdomen`, `biliary_emergency` [nhs-gallstones].
- *Urgent:* tummy pain lasting more than 30 minutes [nhs-gallstones].

**`peptic_ulcer` — Stomach ulcer.** *Synonyms:* stomach ulcer, gastric ulcer, duodenal ulcer, peptic ulcer.
- *Definition:* Sores in the stomach. Most people recover with treatment [nhs-ulcer].
- *Findings:* c: upper_abdominal_burning_pain, often worse at night. o: indigestion, heartburn, bloating, nausea/vomiting [nhs-ulcer].
- *Red flags:* `gi_bleeding`, `acute_abdomen` (severe pain, or painful to touch), `possible_heart_attack` (sudden chest pain) [nhs-ulcer].
- *Urgent:* weight loss, feeling full quickly, difficulty swallowing, persistent vomiting [nhs-ulcer].

**`coeliac_disease` — Coeliac disease.** *Synonyms:* celiac, gluten intolerance (lay, inaccurate).
- *Definition:* The immune system attacks the gut when gluten is eaten, damaging the small intestine [nhs-coeliac].
- *Findings:* c (gut): diarrhoea (may smell bad), abdominal_pain, bloating, flatulence, indigestion, constipation_hard_stool. o: tiredness, weight loss, itchy rash [nhs-coeliac].
- *Red flags:* none on the source page.

### ophthalmology

**`conjunctivitis` ★ — Conjunctivitis.** *Synonyms:* pink eye, red eye, sticky eye.
- *Definition:* An eye condition caused by infection or allergies. It usually gets better in a couple of weeks and usually affects both eyes [nhs-conjunctivitis].
- *Findings (n/s):* red_eye, gritty_eye (burning), sticky_eye_discharge, itchy_eyes, watery_eyes [nhs-conjunctivitis].
- *Red flags:* `acute_red_eye_emergency` [nhs-red-eye]. **Conflict:** see §8.
- *Urgent:* eye pain, light sensitivity, vision changes, very red eyes [nhs-conjunctivitis].

**`dry_eye` — Dry eyes.** *Synonyms:* dry eye syndrome, gritty eyes.
- *Definition:* A common, usually not serious, eye problem [nhs-dry-eyes].
- *Findings (n/s):* itchy_eyes, sore eyes, gritty_eye, red_eye, blurred_vision, photophobia, watery_eyes [nhs-dry-eyes].
- *Red flags:* `acute_red_eye_emergency` [nhs-dry-eyes].
- *Urgent:* painful red eye, red eye in a contact-lens wearer [nhs-dry-eyes].

**`stye` — Stye.** *Synonyms:* sty, hordeolum, eyelid boil.
- *Definition:* A small, painful lump on the eyelid that usually goes within a week. It usually affects one eye [nhs-stye].
- *Findings:* c: eyelid_lump (painful), swollen_eyelid, red_eye, watery_eyes. Vision is not affected [nhs-stye].
- *Discriminator:* no lump suggests conjunctivitis or blepharitis instead [nhs-stye].
- *Red flags:* none at 999 level. *Urgent:* very painful, affects vision, infection spreading [nhs-stye].

**`blepharitis` — Blepharitis.** *Synonyms:* inflamed eyelids, crusty eyelids.
- *Definition:* Swollen, itchy eyelids. Not usually serious [nhs-blepharitis].
- *Findings (n/s):* sore_eyelids, itchy_eyes, gritty_eye, eyelid_crusting (including eyelids stuck together in the morning) [nhs-blepharitis].
- *Red flags:* none at 999 level. *Urgent:* eye pain, vision changes, very red eyes [nhs-blepharitis].

**`subconjunctival_haemorrhage` — Burst blood vessel in the eye.** *Synonyms:* broken blood vessel in eye, blood spot in eye, subconjunctival hemorrhage.
- *Definition:* A small blood vessel breaks under the clear surface of the eye. It often clears in 2–3 weeks [mlp-sch]. NHS lists it as a cause of a "bright red area in the white of your eye" [nhs-red-eye].
- *Findings:* c: red_patch_on_white_of_eye. Painless, no discharge, vision unchanged [mlp-sch].
- *Red flags:* `acute_red_eye_emergency` (very dark red eye, injury) [nhs-red-eye].

### allergist

**`allergic_rhinitis` ★ — Hay fever.** *Synonyms:* hay fever, seasonal allergies, pollen allergy, allergic rhinitis.
- *Definition:* A common allergy (to pollen) that causes sneezing, coughing and itchy eyes. It is usually worst from late March to September and can last weeks or months [nhs-hayfever].
- *Findings (n/s):* sneezing, cough, runny_nose/blocked_nose, itchy_eyes/red_eye/watery_eyes, itchy_nose_throat_ears, loss_of_smell_or_taste, facial_pain_pressure (sides of head and forehead), headache, tiredness, seasonal_pattern [nhs-hayfever].
- *Discriminator:* a cold usually goes in 1–2 weeks. Hay fever lasts weeks to months [nhs-hayfever].
- *Red flags:* none on the source page.

**`food_allergy` — Food allergy.** *Synonyms:* allergic to food, nut allergy, shellfish allergy.
- *Definition:* The body reacts to certain foods. It is often mild but can be very serious. It is different from food intolerance [nhs-food-allergy].
- *Findings (n/s):* dizziness, hives/itchy_skin, face_lip_swelling, cough/wheezing/shortness_of_breath/hoarse_voice, sneezing/runny_nose, nausea/vomiting, abdominal_pain, diarrhoea, plus the after_eating_trigger context [nhs-food-allergy].
- *Red flags:* `anaphylaxis`, `loss_of_consciousness`, `unresponsive_child` [nhs-food-allergy].

**`urticaria` — Hives.** *Synonyms:* hives, nettle rash, welts.
- *Definition:* An itchy raised rash that usually gets better within a few days [nhs-hives].
- *Findings:* c: hives (raised bumps or patches, anywhere), itchy_skin (itchy, stinging or burning) [nhs-hives].
- *Red flags:* `anaphylaxis` [nhs-hives].
- *Urgent:* not improving after 2 days, spreading, swelling under the skin [nhs-hives].

**`angioedema` — Angioedema.** *Synonyms:* allergic swelling, swollen lips.
- *Definition:* Sudden swelling, often from an allergic reaction. It is serious if the throat swells [nhs-angioedema].
- *Findings:* c: face_lip_swelling (lips, tongue, eyelids), swelling_hands_feet_genitals. o: hives, abdominal_pain (bowel swelling) [nhs-angioedema].
- *Red flags:* `anaphylaxis` [nhs-angioedema].
- *Urgent:* any sudden swelling of part of the body [nhs-angioedema].

### cardiology

**`hypertension` — High blood pressure.** *Synonyms:* high BP, hypertension.
- *Definition:* Usually causes no symptoms, so the only way to know is a blood-pressure check. It can lead to heart attacks or strokes [nhs-bp].
- *Findings:* high_blood_pressure_reading (self-reported). Rarely headache, blurred_vision, chest_pain [nhs-bp].
- *Red flags:* `possible_heart_attack` [nhs-bp].
- *Urgent:* frequent headaches or blurred vision, chest pain that comes and goes [nhs-bp].

**`atrial_fibrillation` — Atrial fibrillation.** *Synonyms:* AF, afib, irregular heartbeat.
- *Definition:* A heart rhythm problem in which the heartbeat is not steady [nhs-af].
- *Findings (n/s):* irregular_pulse, palpitations, fast_heartbeat (over 100 bpm), tiredness, exercise_intolerance, chest_tightness, shortness_of_breath, dizziness. It can cause no symptoms [nhs-af].
- *Red flags:* `palpitations_with_red_signs`, `stroke_fast` [nhs-af].

**`angina` — Angina.** *Synonyms:* chest angina, heart pain.
- *Definition:* Pain or tightness, usually in the chest, that can be a sign of a heart problem. Attacks are usually triggered by exertion, stress or cold, last under 10 minutes, and ease with rest [nhs-angina].
- *Findings:* c: exertional_chest_pain / chest_tightness, pain_radiating_arm_neck_jaw_back (neck, shoulders, jaw, arms). o: nausea, shortness_of_breath, dizziness, sweating [nhs-angina].
- *Red flags:* `possible_heart_attack`, including the variant where angina pain does not stop after rest or medicine [nhs-angina].
- *Urgent:* chest pain that comes and goes, or angina that is worse or happens at rest [nhs-angina].

**`heart_failure` — Heart failure.** *Synonyms:* weak heart, congestive heart failure.
- *Definition:* The heart cannot pump blood properly. It does not mean the heart has stopped [nhs-hf].
- *Findings (n/s):* shortness_of_breath, breathless_lying_down, tiredness, dizziness, swollen_ankles/bloating, sudden_weight_gain, night_cough, pink_frothy_sputum [nhs-hf].
- *Red flags:* `severe_breathing_difficulty`, `cyanosis`, `loss_of_consciousness` [nhs-hf].
- *Urgent:* breathless lying down, pink frothy phlegm, sudden weight gain [nhs-hf].

**`ectopic_beats` — Ectopic heartbeats.** *Synonyms:* extra heartbeats, skipped beats, palpitations, PVCs, PACs.
- *Definition:* Changes to an otherwise normal heartbeat that cause extra or skipped beats. They are common in adults and may cause no symptoms [mlp-ectopic]. Palpitations are usually harmless. Common triggers are exercise, lack of sleep, stress, alcohol and caffeine [nhs-palpitations].
- *Findings:* c: palpitations, skipped_beats (feels like the heart stopped or skipped), occasional forceful beats [mlp-ectopic] [nhs-palpitations].
- *Red flags:* `palpitations_with_red_signs` [nhs-palpitations].

### neurology

**`migraine` ★ — Migraine.** *Synonyms:* migraine headache, sick headache.
- *Definition:* Attacks of severe headache, nausea and light sensitivity, lasting 4 hours to 3 days [nhs-migraine].
- *Findings:* c: throbbing_one_sided_headache (worse on movement), nausea/vomiting, photophobia, phonophobia. o (aura): visual_aura, pins_and_needles, dizziness, speech difficulty. o (early warning): tiredness/yawning, food cravings, stiff neck [nhs-migraine].
- *Red flags:* `thunderclap_headache`, `headache_with_neuro_signs`, `stroke_fast`, `meningitis_signs`, `first_seizure` [nhs-migraine].
- *Urgent:* attack lasting more than 72 hours, aura lasting more than 1 hour, pregnant [nhs-migraine].

**`cluster_headache` — Cluster headache.** *Synonyms:* cluster headaches, suicide headache (lay).
- *Definition:* Severe attacks of pain that happen multiple times a day for weeks or months. They are not caused by another illness [nhs-cluster].
- *Findings:* c: one_sided_eye_pain (sharp, burning or piercing), attacks_at_set_times, sudden start and stop, restless_during_pain, attacks lasting 15 minutes to 3 hours. o: red_watery_eye_one_side, nausea, droopy_eyelid/swollen_eyelid, unequal_pupils (smaller on the pain side), face sweating, runny_nose/blocked_nose [nhs-cluster].
- *Red flags:* `new_droopy_eyelid_or_unequal_pupil` [nhs-cluster].
- *Urgent:* temporal-arteritis signs: jaw pain, vision changes, sore scalp [nhs-cluster].

**`carpal_tunnel_syndrome` — Carpal tunnel syndrome.** *Synonyms:* CTS, trapped nerve in the wrist.
- *Definition:* Pressure on a nerve in the wrist that causes tingling, numbness and pain in the hand. Often worse at night [nhs-cts].
- *Findings:* c: hand or arm pain, hand_numbness_tingling, weak_grip [nhs-cts].
- *Red flags:* none.

**`bells_palsy` — Bell's palsy.** *Synonyms:* facial palsy, facial paralysis.
- *Definition:* Temporary weakness of one side of the face. Treatment works best within 72 hours [nhs-bells].
- *Findings:* c: one_sided_facial_weakness (develops over a few days), drooping eyelid or mouth corner, drooling, dry_mouth, loss of taste, dry or watery eye, difficulty closing the eye [nhs-bells].
- *Red flags:* `stroke_fast`. The NHS page leads with the FAST signs [nhs-bells]. See §8.
- *Urgent:* any symptoms [nhs-bells].

**`restless_legs_syndrome` — Restless legs syndrome.** *Synonyms:* RLS, Willis–Ekbom disease, twitchy legs.
- *Definition:* A strong urge to move the legs, usually when resting at night [nhs-rls].
- *Findings:* c: urge_to_move_legs, leg tingling, throbbing or itching, leg pain. Worse at night [nhs-rls].
- *Red flags:* none.

### dermatology

**`atopic_eczema` ★ — Eczema.** *Synonyms:* eczema, atopic dermatitis.
- *Definition:* A common long-term condition causing itchy skin. It is most common in young children and comes in flare-ups [nhs-eczema].
- *Findings:* c: itchy_skin, dry_cracked_skin, discoloured_skin_patches, sometimes blisters or bleeding. Often on elbows, knees and hands [nhs-eczema].
- *Red flags:* none at 999 level. *Urgent:* infected or eczema herpeticum signs: weeping, crusting, pus, fever [nhs-eczema].

**`psoriasis` — Psoriasis.** *Synonyms:* plaque psoriasis, scaly skin.
- *Definition:* A common long-term condition causing itchy, painful patches of dry, flaky skin [nhs-psoriasis].
- *Findings:* c: silvery_scaly_plaques, itchy_skin, dry_cracked_skin, on the scalp, elbows, knees and back. o: nail_pitting, joint_pain_swelling [nhs-psoriasis].
- *Red flags:* `severe_psoriasis_flare` [nhs-psoriasis].

**`acne` — Acne.** *Synonyms:* spots, pimples, breakouts.
- *Definition:* A common skin condition causing spots, usually on the face, chest and back [nhs-acne].
- *Findings (n/s):* spots, greasy_skin, painful_skin_lumps, scarring [nhs-acne].
- *Red flags:* none.

**`contact_dermatitis` — Contact dermatitis.** *Synonyms:* skin allergy, allergic rash, irritant rash.
- *Definition:* A type of eczema triggered by contact with a substance. It occurs within hours to days, most often on the hands and face [nhs-contact].
- *Findings:* c: itchy_skin, blisters, dry_cracked_skin, discoloured_skin_patches, plus the rash_after_contact context [nhs-contact].
- *Red flags:* none.

**`athletes_foot` — Athlete's foot.** *Synonyms:* tinea pedis, foot fungus.
- *Definition:* A common fungal infection of the feet [nhs-athletes].
- *Findings:* c: itchy_between_toes. o: sore flaky patches, cracked or bleeding skin, blisters [nhs-athletes].
- *Red flags:* none. *GP:* foot hot, painful and red; diabetes [nhs-athletes].

**`shingles` — Shingles.** *Synonyms:* herpes zoster, zoster.
- *Definition:* An infection causing a painful one-sided rash. See a pharmacist within 3 days [nhs-shingles].
- *Findings:* c: localised_skin_pain_tingling (early), headache or feeling unwell, one_sided_band_rash that turns into blisters and then scabs [nhs-shingles].
- *Red flags:* none at 999 level. *Urgent:* rash on the eye or nose, vision changes, pregnant, immunosuppressed [nhs-shingles].

### otolaryngology

**`sinusitis` ★ — Sinusitis.** *Synonyms:* sinus infection, blocked sinuses.
- *Definition:* Swelling of the sinuses, usually from infection and often after a cold. It usually clears within 4 weeks [nhs-sinusitis].
- *Findings:* c: facial_pain_pressure, blocked_nose/runny_nose, loss_of_smell_or_taste, coloured_nasal_discharge, fever. o: headache, toothache, bad_breath, cough, ear_or_face_pressure [nhs-sinusitis].
- *Red flags:* none at 999 level. *Urgent:* very unwell, worsening, immunosuppressed [nhs-sinusitis].

**`tonsillitis` — Tonsillitis.** *Synonyms:* swollen tonsils, throat infection.
- *Definition:* Infection of the tonsils at the sides of the throat [nhs-tonsillitis].
- *Findings:* c: sore_throat, painful_swallowing, fever, cough, headache, nausea/vomiting, earache, tiredness. o (more severe): swollen_neck_glands, white_patches_on_tonsils, bad_breath [nhs-tonsillitis].
- *Red flags:* `upper_airway_obstruction`, framed by NHS as quinsy [nhs-tonsillitis].
- *Urgent:* pus on the tonsils, too painful to eat or drink [nhs-tonsillitis].

**`otitis_media` — Middle ear infection.** *Synonyms:* ear infection, otitis media.
- *Definition:* An infection behind the eardrum, usually in children and caused by cold and flu viruses. Most clear up within 3 days [nhs-ear].
- *Findings (n/s):* earache, fever, hearing_loss, ear_discharge, ear_fullness. In children: pulling at the ear, irritability [nhs-ear].
- *Red flags:* none at 999 level. *Urgent:* swelling around the ear, discharge, new hearing loss, very high temperature [nhs-ear].

**`otitis_externa` — Outer ear infection.** *Synonyms:* swimmer's ear, ear canal infection.
- *Definition:* Inflammation or infection of the ear canal [mlp-oe], often caused by water, eczema or earplugs [nhs-ear].
- *Findings:* c: ear_discharge, pain_on_pulling_ear, hearing_loss, ear_itch [mlp-oe]. o: scaly skin in and around the ear [nhs-ear].
- *Red flags:* none at 999 level. MedlinePlus says to contact a provider for fever or for pain and redness of the skull behind the ear, because malignant otitis externa is a risk in diabetes [mlp-oe].

**`earwax_build_up` — Earwax build-up.** *Synonyms:* blocked ear, impacted earwax.
- *Definition:* Earwax blocking the ear [nhs-earwax].
- *Findings (n/s):* hearing_loss, earache/ear_fullness, tinnitus, vertigo [nhs-earwax].
- *Red flags:* none.

**`bppv` — BPPV.** *Synonyms:* positional vertigo, benign positional vertigo.
- *Definition:* The most common cause of vertigo. Calcium crystals inside the inner ear cause brief spinning when the head moves [mlp-bppv] [nhs-vertigo].
- *Findings:* c: vertigo triggered by head_movement_trigger (rolling over in bed, looking up), lasting seconds to minutes, loss_of_balance, nausea/vomiting [mlp-bppv].
- *Red flags:* `vertigo_with_neuro_signs` [mlp-bppv] [nhs-vertigo].

**`labyrinthitis` — Labyrinthitis / vestibular neuritis.** *Synonyms:* inner ear infection, vestibular neuritis.
- *Definition:* Inner-ear infections that affect balance. They usually get better within a few weeks. Vestibular neuritis does not cause hearing loss or tinnitus [nhs-labyrinthitis].
- *Findings:* c: vertigo, loss_of_balance, nausea/vomiting, hearing_loss, tinnitus. Sudden onset [nhs-labyrinthitis].
- *Red flags:* `vertigo_with_neuro_signs` [nhs-vertigo]. **Conflict** on hearing loss: see §8.
- *Urgent:* sudden hearing loss in one ear [nhs-labyrinthitis].

---

## 6. Licensing and coding judgement calls

1. **ICD-11 clause 1.2.4 (mapping or crosswalks).** Tagging a knowledge-base entry with an ICD code is arguably not a "crosswalk between terminologies". Storing ICD-10 **and** ICD-11 side by side, however, could be read as an ICD-10↔ICD-11 crosswalk [icd11-licence]. Get a human or legal read, or ask licensing@who.int.
2. **ICD-11 clause 1.2.3.** Storage must keep **code + title + URI** together [icd11-licence]. The spec should require all three.
3. **Pick a specificity level per condition.** I chose "unspecified" leaves where they exist, such as 8A81.Z rather than 8A81. Either choice is defensible.
4. **Food allergy in ICD-10.** WHO ICD-10 has no clean "food allergy" category. T78.1 is "Other adverse food reactions, NEC" [icd10-browser]. In ICD-11, 4A85.2 "Food hypersensitivity" fits better [icd11-file].
5. **Contact dermatitis in ICD-11** has no unspecified parent. Pick EK00 (allergic) or EK02 (irritant), or split the condition in two [icd11-file].
6. **Ectopic beats in ICD-11** are split into atrial (BC60) and ventricular (BC70). ICD-10 merges them in I49.4 [icd11-file] [icd10-browser].
7. **Constipation:** ME05.0 is a symptom code. DD91.1 "Functional constipation" is a disorder code [icd11-file].

---

## 7. Normalised red-flag catalogue

Each red flag fires when **all** findings in **one** of its variants are present. Variants are alternative AND-sets that share one emergency message. The finding ids are defined in §4. The message wording is a draft adapted from the NHS 999 boxes. The emergency number must be configurable, because the insurer's country is unknown (999 UK, 112 EU, 911 US). Per [nhs-terms] §3.6(b), do not attribute these messages to the NHS.

| # | id | Variants (all findings required) | Draft emergency message | Referenced by | Sources |
|---|---|---|---|---|---|
| 1 | `possible_heart_attack` | a) chest_pain + pain_radiating_arm_neck_jaw_back · b) chest_pain + sweating · c) chest_pain + shortness_of_breath · d) chest_pain + nausea · e) chest_pain + dizziness · f) chest_pain + sudden_onset · g) chest_pain + persistent · h) exertional_chest_pain + persistent (angina not settling with rest or medicine) | "Chest pain like this can be a sign of a heart attack. Call {emergency_number} now. Do not drive yourself." | influenza, covid_19, gord, peptic_ulcer, hypertension, angina | [nhs-chest-pain] [nhs-heart-attack] [nhs-angina] [nhs-bp] [nhs-flu] [nhs-covid] [nhs-ulcer] |
| 2 | `severe_breathing_difficulty` | a) breathing_struggle | "Severe difficulty breathing needs emergency care. Call {emergency_number} now." | influenza, covid_19, gastroenteritis, acute_bronchitis, asthma, copd, pneumonia, heart_failure | [nhs-sob] [nhs-flu] [nhs-covid] [nhs-bronchitis] [nhs-pneumonia] [nhs-hf] [nhs-dv] |
| 3 | `cyanosis` | a) cyanosis | "Blue, grey or very pale lips or skin can mean you are not getting enough oxygen. Call {emergency_number} now." | strep_throat, gastroenteritis, dehydration, acute_bronchitis, copd, pneumonia, heart_failure | [nhs-sob] [nhs-bronchitis] [nhs-pneumonia] [nhs-hf] [nhs-dehydration] [nhs-dv] [nhs-strepa] |
| 4 | `coughing_up_blood` | a) cough_up_blood | "Coughing up blood needs urgent assessment. If it is more than a few streaks, or you are breathless or have chest pain, call {emergency_number} now." | influenza, covid_19, pneumonia | [nhs-flu] [nhs-covid] [nhs-pneumonia] [nhs-cough-blood] |
| 5 | `stroke_fast` | a) one_sided_facial_weakness · b) arm_or_side_weakness · c) speech_problem | "Face drooping, arm weakness or speech problems can be signs of a stroke. Call {emergency_number} now, even if the symptoms stop." | migraine, bells_palsy, atrial_fibrillation | [nhs-stroke] [nhs-tia] [nhs-bells] [nhs-af] [nhs-migraine] |
| 6 | `thunderclap_headache` | a) headache + sudden_onset + severe_pain | "A sudden, extremely painful headache needs emergency care. Call {emergency_number} now." | gastroenteritis, tension_headache, migraine | [nhs-sah] [nhs-headaches] [nhs-tension] [nhs-migraine] [nhs-dv] |
| 7 | `meningitis_signs` | a) stiff_neck + photophobia · b) non_blanching_rash · c) headache + fever + stiff_neck | "These can be signs of meningitis. Call {emergency_number} or go to the emergency department now." | covid_19, gastroenteritis, tension_headache, migraine | [nhs-meningitis] [nhs-headaches] [nhs-dv] [nhs-covid] [nhs-tension] [nhs-migraine] |
| 8 | `headache_with_neuro_signs` | a) headache + confusion · b) headache + drowsiness · c) headache + vision_loss · d) headache + seizure · e) headache + head_injury · f) headache + speech_problem · g) headache + memory_problem · h) headache + arm_or_side_weakness · i) headache + numbness · j) headache + severe_pain + red_eye | "A headache with these symptoms needs emergency care. Call {emergency_number} or go to the emergency department now." | tension_headache, migraine | [nhs-headaches] [nhs-tension] [nhs-migraine] |
| 9 | `anaphylaxis` | a) face_lip_swelling + sudden_onset · b) throat_swelling_or_tightness · c) hives + breathing_struggle · d) hives + wheezing · e) hives + dizziness · f) hives + rapid_breathing | "This could be a severe allergic reaction (anaphylaxis). Use an adrenaline auto-injector if you have one and call {emergency_number} now." | food_allergy, urticaria, angioedema | [nhs-anaphylaxis] [nhs-food-allergy] [nhs-hives] [nhs-angioedema] |
| 10 | `possible_sepsis` | a) fever + confusion · b) fever + rapid_breathing · c) fever + mottled_skin · d) fever + no_urine · e) fever + speech_problem | "These can be signs of sepsis, a life-threatening reaction to an infection. Call {emergency_number} or go to the emergency department now." | urinary_tract_infection | [nhs-sepsis] [nhs-uti] [nhs-kidney] |
| 11 | `sudden_confusion` | a) confusion + sudden_onset · b) drowsiness | "Sudden confusion or unusual drowsiness needs emergency care. Call {emergency_number} now." | gastroenteritis, dehydration, acute_bronchitis, urinary_tract_infection, pneumonia | [nhs-uti] [nhs-kidney] [nhs-bronchitis] [nhs-pneumonia] [nhs-dehydration] [nhs-dv] |
| 12 | `severe_dehydration_shock` | a) thirst + cold_skin · b) dark_urine + confusion · c) reduced_urination + drowsiness · d) dry_mouth + mottled_skin · e) thirst + rapid_breathing | "Signs of dehydration with these symptoms can mean shock. Call {emergency_number} now." | gastroenteritis, dehydration | [nhs-dehydration] [nhs-dv] |
| 13 | `gi_bleeding` | a) vomit_blood · b) black_tarry_stool · c) heavy_rectal_bleeding | "Vomiting blood, black sticky poo or heavy bleeding from the bottom needs emergency care. Call {emergency_number} or go to the emergency department now." | gastroenteritis, peptic_ulcer | [nhs-ulcer] [nhs-dv] [nhs-vomit-blood] [nhs-rectal] [nhs-stomach-ache] |
| 14 | `acute_abdomen` | a) abdominal_pain + sudden_onset + severe_pain · b) abdominal_pain + cannot_pass_stool_or_wind · c) abdominal_pain + cannot_pee · d) green_vomit | "Severe or sudden tummy pain like this needs emergency care. Call {emergency_number} or go to the emergency department now." | gastroenteritis, constipation, gallstones, peptic_ulcer | [nhs-stomach-ache] [nhs-gallstones] [nhs-ulcer] [nhs-appendicitis] [nhs-dv] |
| 15 | `biliary_emergency` | a) abdominal_pain + jaundice · b) abdominal_pain + pain_spreading_to_back + vomiting · c) right_upper_abdominal_pain + fever | "Tummy pain with yellow skin or eyes, a high temperature, or pain going into your back with vomiting needs emergency care. Call {emergency_number} or go to the emergency department now." | gallstones | [nhs-gallstones] |
| 16 | `loss_of_consciousness` | a) unresponsive | "If someone has passed out and is not responding normally, call {emergency_number} now." | covid_19, food_allergy, heart_failure | [nhs-hf] [nhs-heart-attack] [nhs-anaphylaxis] [nhs-fainting] [nhs-covid] |
| 17 | `first_seizure` | a) seizure | "A first seizure (fit) needs emergency care. Call {emergency_number} now." | covid_19, migraine | [nhs-covid] [nhs-meningitis] [nhs-migraine] [nhs-headaches] |
| 18 | `acute_red_eye_emergency` | a) red_eye + vision_loss · b) red_eye + blurred_vision + sudden_onset · c) red_eye + photophobia · d) red_eye + headache + nausea · e) very_dark_red_eye · f) eye_injury_or_foreign_body · g) chemical_in_eye · h) red_eye + unequal_pupils | "A red eye with these symptoms needs emergency care. Go to the emergency department or call {emergency_number} now. Do not drive yourself." | conjunctivitis, dry_eye, subconjunctival_haemorrhage | [nhs-red-eye] [nhs-dry-eyes] [nhs-glaucoma] |
| 19 | `new_droopy_eyelid_or_unequal_pupil` | a) droopy_eyelid + sudden_onset · b) unequal_pupils + sudden_onset | "A newly drooping eyelid or one pupil smaller than the other needs emergency assessment, even if you have cluster headaches. Go to the emergency department now." | cluster_headache | [nhs-cluster] |
| 20 | `upper_airway_obstruction` | a) sore_throat + cannot_swallow · b) drooling + sore_throat · c) stridor · d) sore_throat + difficulty_opening_mouth · e) swelling_in_mouth_or_throat + sore_throat · f) sore_throat + breathing_struggle | "A sore throat with difficulty swallowing, drooling, noisy breathing or trouble opening your mouth needs emergency care. Call {emergency_number} now and stay upright." | strep_throat, tonsillitis | [nhs-sore-throat] [nhs-tonsillitis] [nhs-epiglottitis] |
| 21 | `palpitations_with_red_signs` | a) palpitations + chest_pain · b) palpitations + shortness_of_breath · c) palpitations + fainting · d) fast_heartbeat + chest_pain · e) irregular_pulse + fainting | "Palpitations with chest pain, breathlessness or fainting need emergency care. Call {emergency_number} now." | atrial_fibrillation, ectopic_beats | [nhs-palpitations] [nhs-af] [nhs-fainting] |
| 22 | `vertigo_with_neuro_signs` | a) vertigo + vision_loss · b) vertigo + speech_problem · c) vertigo + arm_or_side_weakness · d) vertigo + numbness · e) vertigo + hearing_loss (see §8) | "Vertigo with these symptoms needs emergency care. Call {emergency_number} or go to the emergency department now." | bppv, labyrinthitis | [nhs-vertigo] [mlp-bppv] |
| 23 | `severe_asthma_attack` | a) asthma_attack + inhaler_not_helping · b) asthma_attack + no_inhaler · c) asthma_attack + breathing_struggle | "If your reliever inhaler is not helping or you do not have one during an asthma attack, call {emergency_number} now." | asthma | [nhs-asthma] |
| 24 | `severe_psoriasis_flare` | a) widespread_red_skin_with_pustules · b) widespread_red_skin_with_pustules + fever | "Skin that quickly turns red with pus-filled bumps needs emergency care. Go to the emergency department or call {emergency_number} now." | psoriasis | [nhs-psoriasis] |
| 25 | `unresponsive_child` | a) floppy_child · b) young_infant + drowsiness | "A child who is floppy, will not wake or is not responding normally needs emergency care. Call {emergency_number} now." | strep_throat, acute_bronchitis, pneumonia, food_allergy | [nhs-strepa] [nhs-bronchitis] [nhs-pneumonia] [nhs-food-allergy] [nhs-sob] |

### General red flags (referenced by no condition)

| # | id | Variants | Draft emergency message | Sources |
|---|---|---|---|---|
| 26 | `pulmonary_embolism` | a) shortness_of_breath + sudden_onset · b) chest_pain + sudden_onset + shortness_of_breath · c) cough_up_blood + shortness_of_breath · d) shortness_of_breath + fast_heartbeat · e) calf_swelling_or_pain + shortness_of_breath | "Sudden breathlessness or chest pain, especially with a swollen leg or coughing up blood, can mean a blood clot in the lungs. Call {emergency_number} now." | [nhs-pe] [nhs-cough-blood] |
| 27 | `suicidal_crisis` | a) self_harm_done · b) suicidal_intent | "If you have harmed yourself or feel you might act on thoughts of ending your life, call {emergency_number} or go to the emergency department now. You can also call a crisis line such as Samaritans 116 123 (UK)." | [nhs-suicide] |
| 28 | `diabetic_ketoacidosis` | a) thirst + frequent_urination + fruity_breath · b) thirst + frequent_urination + drowsiness · c) high_ketones | "These can be signs of diabetic ketoacidosis. Call {emergency_number} or go to the emergency department now." | [nhs-dka] |
| 29 | `ruptured_ectopic_pregnancy` | a) abdominal_pain + sudden_onset + fainting · b) abdominal_pain + sudden_onset + pregnant_or_missed_period + dizziness | "Sudden severe tummy pain with fainting or feeling very dizzy, especially if you could be pregnant, needs emergency care. Call {emergency_number} now." | [nhs-ectopic-preg] |
| 30 | `cauda_equina_syndrome` | a) back_pain + saddle_numbness · b) back_pain + new_bladder_or_bowel_problem · c) back_pain + both_legs_weak_or_numb | "Back pain with numbness around your bottom or genitals, new bladder or bowel problems, or weakness in both legs needs emergency care. Go to the emergency department now." | [nhs-back] |
| 31 | `febrile_young_infant` | a) young_infant + fever | "A baby under 3 months with a temperature of 38°C or more needs urgent medical assessment. Call {emergency_number} if they are also unwell." | [nhs-meningitis] [nhs-sepsis] [nhs-covid] |

**Totals:** 31 red flags, 25 referenced by conditions and 6 general. `possible_sepsis` and `febrile_young_infant` overlap with `meningitis_signs` through the non-blanching rash and young-infant fever, so their findings deliberately share ids.

---

## 8. Fact-check: does the Manchester Triage System use ~50 presentation charts?

**Mostly right, but imprecise. The 3rd edition (2014) has 53 presentational flow charts. The 2nd edition had 52.**

- **Primary source:** *Emergency Triage: Manchester Triage Group*, 3rd edition, edited by Mackway-Jones, Marsden and Windle (Wiley/BMJ Books, 2014). In the publisher's reading sample, chapter 1 says triage places each patient *"into one of 265 slots in a 53×5 presentation–priority matrix"* (53 presentations × 5 priorities = 265). The sample also shows the "Presentational flow chart index" (p. 62), which runs from "Abdominal pain in adults" to "Wounds" and includes "Major incidents primary/secondary" [mts-sample].
- **Second edition:** a 2010–2012 validation study that used the official translations of the MTS **2nd edition** says the system *"consists of 52 flowcharts"* [mts-pmc].
- **UNVERIFIED:** whether the later printings (Version 3.7/3.8, 2023) still have 53 charts. Only retailer listings confirm that "Version 3.8, 2023" exists; I found no primary source giving its count.
- **Relevance to ADR 0002:** the MTS mixes general discriminators (pain, airway, consciousness) with presentation-specific ones [mts-sample]. That is the same split as our general versus condition-specific red flags.

---

## 9. Gaps, conflicts and points for human review

**UNVERIFIED items (5):**
1. `dry_eye` ICD-11. 9A79 "Keratoconjunctivitis sicca" is the best title match, but I could not confirm that "dry eye syndrome" is indexed to it. Check in the ICD-11 browser search [icd11-browser].
2. `blepharitis` ICD-11. There is no generic blepharitis category in MMS 2026-01. The candidates are 9A02.1 and 9A01.3 [icd11-file].
3. `angioedema` ICD-11. The category depends on the cause. Candidates: EB04, 4A85.21, 4A00.14, 4A00.15 [icd11-file].
4. `cluster_headache` ICD-11. 8A82 "Trigeminal autonomic cephalalgias" is a leaf in the MMS tabulation and has no "cluster headache" child. I could not confirm whether cluster headache is an index term there or needs postcoordination [icd11-file].
5. MTS Version 3.8 chart count (§8).

Every other code was checked by code and title against WHO sources. The ICD-11 codes were checked against the release tabulation, not the JS-rendered browser UI, and index terms were not checked.

**Source conflicts:**
- **Coughing up blood.** The flu, COVID-19 and pneumonia pages say coughing up blood means call 999 [nhs-flu] [nhs-covid] [nhs-pneumonia]. The bronchitis page and the coughing-up-blood symptom page say an *urgent GP* appointment is enough for streaks or spots [nhs-bronchitis] [nhs-cough-blood]. `coughing_up_blood` fires on any mention, which is the safer reading. Review the near-miss question wording.
- **Red eye.** The conjunctivitis and blepharitis pages say eye pain, light sensitivity or vision changes need an *urgent GP* [nhs-conjunctivitis] [nhs-blepharitis]. The red-eye and dry-eyes pages say red eye with vision changes or light sensitivity means *999/A&E* [nhs-red-eye] [nhs-dry-eyes]. The catalogue follows the stricter pages.
- **Vertigo with hearing loss.** The vertigo page says vertigo with hearing loss means 999 [nhs-vertigo]. The labyrinthitis page lists hearing loss as a common symptom and treats sudden one-sided hearing loss as *urgent GP* [nhs-labyrinthitis]. As drafted, variant 22e will fire on most labyrinthitis presentations. Either remove 22e or accept the false positives.
- **Febrile young infant.** The meningitis and sepsis pages say 999/A&E for a baby under 3 months with a temperature of 38°C or more [nhs-meningitis] [nhs-sepsis]. The COVID-19 page says urgent GP/111 [nhs-covid]. Doctor Advisor's patients may or may not include children; decide whether paediatric red flags are in scope.

**False-positive risks (accepted under ADR 0002, but worth an eval):**
- `stroke_fast` (a) will always fire for Bell's palsy, because face droop is its core symptom. This matches NHS advice to rule out stroke first [nhs-bells].
- `possible_heart_attack` (c) chest_pain + shortness_of_breath will often fire for bronchitis, pneumonia and asthma.
- `sudden_confusion` (b) drowsiness alone is broad. Consider requiring an infection or dehydration context finding.

**Other judgement calls:**
- **Speciality assignments.** Tension headache, strep throat and bronchitis could go to neurology, ENT or pulmonology respectively. They are assigned to general_practitioner because the NHS routes them to self-care, a pharmacist or a GP. Hay fever, hives and angioedema go to allergist, although the NHS sends them to a GP first.
- **Urgency labels** are my mapping of NHS tiers, not NHS terminology.
- **Synonyms and lay phrasings** are author-generated, as are the "c/o" frequencies where NHS separates "main" from "may also" symptoms. MedlinePlus uses "common" versus "other".
- **No condition is sourced from NICE CKS,** because of the CKS licence [nice-open]. Cross-checking against CKS is possible for internal clinical review only, and needs separate permission.
- **MedlinePlus `/ency/` text is A.D.A.M.-copyrighted** [mlp-using]. Re-word it; do not paste it into YAML.
- **NHS pages show "next review due" dates,** and some were already past due when retrieved (e.g. vertigo: next review due 2 May 2026). NHS terms recommend refreshing every 24 hours [nhs-terms]. Plan a periodic re-verification job.

---

## References

[icd11-file]: https://icdcdn.who.int/static/releasefiles/2026-01/SimpleTabulation-ICD-11-MMS-en.zip
[icd11-browser]: https://icd.who.int/browse/2026-01/mms/en
[icd10-browser]: https://icd.who.int/browse10/2019/en
[icd11-licence]: https://icd.who.int/en/docs/ICD11-license.pdf
[who-class-licence]: https://www.who.int/about/licensing/classifications/en/
[who-icd10-faq]: https://cdn.who.int/media/docs/default-source/publishing-policies/copyright/who-faq-licensing-icd-10.pdf
[nhs-terms]: https://www.nhs.uk/our-policies/terms-and-conditions/
[mlp-using]: https://medlineplus.gov/about/using/usingcontent/
[nice-open]: https://www.nice.org.uk/reusing-our-content/nice-uk-open-content-licence
[nice-terms]: https://www.nice.org.uk/terms-and-conditions
[snomed-get]: https://www.snomed.org/get-snomed
[mts-sample]: https://content.e-bookshelf.de/media/reading/L-4033541-3f8b45baf4.pdf
[mts-pmc]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5289484/
[nhs-cold]: https://www.nhs.uk/conditions/common-cold/
[nhs-flu]: https://www.nhs.uk/conditions/flu/
[nhs-covid]: https://www.nhs.uk/conditions/covid-19/covid-19-symptoms-and-what-to-do/
[mlp-strep]: https://medlineplus.gov/ency/article/000639.htm
[nhs-strepa]: https://www.nhs.uk/conditions/strep-a/
[nhs-sore-throat]: https://www.nhs.uk/symptoms/sore-throat/
[mlp-gastro]: https://medlineplus.gov/ency/article/000252.htm
[nhs-dv]: https://www.nhs.uk/symptoms/diarrhoea-and-vomiting/
[nhs-dehydration]: https://www.nhs.uk/conditions/dehydration/
[nhs-insomnia]: https://www.nhs.uk/conditions/insomnia/
[nhs-motion]: https://www.nhs.uk/conditions/motion-sickness/
[nhs-tension]: https://www.nhs.uk/conditions/tension-headaches/
[nhs-bronchitis]: https://www.nhs.uk/conditions/bronchitis/
[nhs-uti]: https://www.nhs.uk/conditions/urinary-tract-infections-utis/
[nhs-kidney]: https://www.nhs.uk/conditions/kidney-infection/
[nhs-asthma]: https://www.nhs.uk/conditions/asthma/
[nhs-copd]: https://www.nhs.uk/conditions/chronic-obstructive-pulmonary-disease-copd/
[nhs-copd-symptoms]: https://www.nhs.uk/conditions/chronic-obstructive-pulmonary-disease-copd/symptoms/
[nhs-pneumonia]: https://www.nhs.uk/conditions/pneumonia/
[nhs-osa]: https://www.nhs.uk/conditions/sleep-apnoea/
[nhs-reflux]: https://www.nhs.uk/conditions/heartburn-and-acid-reflux/
[nhs-ibs]: https://www.nhs.uk/conditions/irritable-bowel-syndrome-ibs/
[nhs-ibs-symptoms]: https://www.nhs.uk/conditions/irritable-bowel-syndrome-ibs/symptoms/
[nhs-constipation]: https://www.nhs.uk/conditions/constipation/
[nhs-gallstones]: https://www.nhs.uk/conditions/gallstones/
[nhs-ulcer]: https://www.nhs.uk/conditions/stomach-ulcer/
[nhs-coeliac]: https://www.nhs.uk/conditions/coeliac-disease/
[nhs-conjunctivitis]: https://www.nhs.uk/conditions/conjunctivitis/
[nhs-dry-eyes]: https://www.nhs.uk/symptoms/dry-eyes/
[nhs-stye]: https://www.nhs.uk/conditions/stye/
[nhs-blepharitis]: https://www.nhs.uk/conditions/blepharitis/
[nhs-red-eye]: https://www.nhs.uk/symptoms/red-eye/
[mlp-sch]: https://medlineplus.gov/ency/article/001616.htm
[nhs-hayfever]: https://www.nhs.uk/conditions/hay-fever/
[nhs-food-allergy]: https://www.nhs.uk/conditions/food-allergy/
[nhs-hives]: https://www.nhs.uk/conditions/hives/
[nhs-angioedema]: https://www.nhs.uk/conditions/angioedema/
[nhs-bp]: https://www.nhs.uk/conditions/high-blood-pressure/
[nhs-af]: https://www.nhs.uk/conditions/atrial-fibrillation/
[nhs-angina]: https://www.nhs.uk/conditions/angina/
[nhs-hf]: https://www.nhs.uk/conditions/heart-failure/
[nhs-palpitations]: https://www.nhs.uk/symptoms/heart-palpitations/
[mlp-ectopic]: https://medlineplus.gov/ency/article/001100.htm
[nhs-migraine]: https://www.nhs.uk/conditions/migraine/
[nhs-cluster]: https://www.nhs.uk/conditions/cluster-headaches/
[nhs-cts]: https://www.nhs.uk/conditions/carpal-tunnel-syndrome/
[nhs-bells]: https://www.nhs.uk/conditions/bells-palsy/
[nhs-rls]: https://www.nhs.uk/conditions/restless-legs-syndrome/
[nhs-eczema]: https://www.nhs.uk/conditions/atopic-eczema/
[nhs-psoriasis]: https://www.nhs.uk/conditions/psoriasis/
[nhs-acne]: https://www.nhs.uk/conditions/acne/
[nhs-contact]: https://www.nhs.uk/conditions/contact-dermatitis/
[nhs-athletes]: https://www.nhs.uk/conditions/athletes-foot/
[nhs-shingles]: https://www.nhs.uk/conditions/shingles/
[nhs-sinusitis]: https://www.nhs.uk/conditions/sinusitis-sinus-infection/
[nhs-tonsillitis]: https://www.nhs.uk/conditions/tonsillitis/
[nhs-ear]: https://www.nhs.uk/conditions/ear-infections/
[mlp-oe]: https://medlineplus.gov/ency/article/000622.htm
[nhs-earwax]: https://www.nhs.uk/conditions/earwax-build-up/
[nhs-vertigo]: https://www.nhs.uk/conditions/vertigo/
[mlp-bppv]: https://medlineplus.gov/ency/article/001420.htm
[nhs-labyrinthitis]: https://www.nhs.uk/conditions/labyrinthitis/
[nhs-chest-pain]: https://www.nhs.uk/symptoms/chest-pain/
[nhs-heart-attack]: https://www.nhs.uk/conditions/heart-attack/
[nhs-sob]: https://www.nhs.uk/symptoms/shortness-of-breath/
[nhs-cough-blood]: https://www.nhs.uk/symptoms/coughing-up-blood/
[nhs-stroke]: https://www.nhs.uk/conditions/stroke/symptoms/
[nhs-tia]: https://www.nhs.uk/conditions/transient-ischaemic-attack-tia/
[nhs-sah]: https://www.nhs.uk/conditions/subarachnoid-haemorrhage/
[nhs-headaches]: https://www.nhs.uk/symptoms/headaches/
[nhs-meningitis]: https://www.nhs.uk/conditions/meningitis/
[nhs-anaphylaxis]: https://www.nhs.uk/conditions/anaphylaxis/
[nhs-sepsis]: https://www.nhs.uk/conditions/sepsis/
[nhs-stomach-ache]: https://www.nhs.uk/symptoms/stomach-ache/
[nhs-vomit-blood]: https://www.nhs.uk/symptoms/vomiting-blood/
[nhs-rectal]: https://www.nhs.uk/symptoms/bleeding-from-the-bottom-rectal-bleeding/
[nhs-appendicitis]: https://www.nhs.uk/conditions/appendicitis/
[nhs-fainting]: https://www.nhs.uk/symptoms/fainting/
[nhs-glaucoma]: https://www.nhs.uk/conditions/glaucoma/
[nhs-epiglottitis]: https://www.nhs.uk/conditions/epiglottitis/
[nhs-pe]: https://www.nhs.uk/conditions/pulmonary-embolism/
[nhs-suicide]: https://www.nhs.uk/mental-health/feelings-symptoms-behaviours/behaviours/help-for-suicidal-thoughts/
[nhs-dka]: https://www.nhs.uk/conditions/diabetic-ketoacidosis/
[nhs-ectopic-preg]: https://www.nhs.uk/conditions/ectopic-pregnancy/
[nhs-back]: https://www.nhs.uk/conditions/back-pain/
