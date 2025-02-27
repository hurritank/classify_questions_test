prompt = """
You are an Adult-Geriatric Acute Care Nurse Specialist.
You will be provided the definition of Domain, Subdomain, and Third-level category of question in the examination, the question ID, the question and the answer.
Your task is to use the definition and the answer to classify the question into which domain, subdomain,  third-level category it belongs and the probability or confidence score for your classification, and explain why is that probability.

- Step 1: Classify which domain the question belongs to out of the 3 domains provided in the definition(Core Competencies, Clinical Practice or Professional Role)
- Step 2: When the you founded the domain, depend on the domain, classify which subdomain the question belongs to. 
    For example, if the domain of question is Professional Role then the subdomain must is Knowledge or Skill.
- Step 3: When you founded the domain and subdomain, depend on that, classify which third-level category the question belongs to.
    For examplse, if the domain of question is Professional Role, and the subdomain is Skill then the third-level category must is Research and evidence-based practice or Educational strategies and health literacy or Relationship development (e.g., patient, family, inter-professional)
- Step 4: When you done classify, calculate the probability score(the confident score for you final output).

Let's think step by step.

Here is the definition of Domain, Subdomain, and Third-level category:
{definition_data}

Here is the question ID:
{question_id}

Here is the question:
{question}

Here is the answer:
{answer}
"""

definition_data = """
    Domain: I. Core Competencies
        Subdomain: A. Knowledge
            Third-level category: 1. Advanced pathophysiology
            Third-level category: 2. Advanced pharmacology
        Subdomain: B. Skill
            Third-level category: 1. Advanced physical assessment
    Domain: II. Clinical Practice
        Subdomain: A. Knowledge
            Third-level category: 1. Standards of care and clinical guidelines
            Third-level category: 2. Standardized assessment tools
            Third-level category: 3. Psychosocial factors (e.g., emotional, cultural, spiritual)
            Third-level category: 4. Cost-effective care
            Third-level category: 5. Health promotion and disease prevention
        Subdomain: B. Skill
            Third-level category: 1. Risk stratification (e.g., physiologic, vulnerable populations)
            Third-level category: 2. Diagnostic testing and procedures
            Third-level category: 3. Non-pharmacologic and pharmacologic treatments and procedures
    Domain: III. Professional Role
        Subdomain: A. Knowledge
            Third-level category: 1. Scope and standards of professional practice
            Third-level category: 2. Health care policy and systems
            Third-level category: 3. Quality improvement processes
        Subdomain: B. Skill
            Third-level category: 1. Research and evidence-based practice
            Third-level category: 2. Educational strategies and health literacy
            Third-level category: 3. Relationship development (e.g., patient, family, inter-professional)
"""

definition_data_v2 = """
#Domain: Core Competencies
This domain encompasses the foundational knowledge and skills that are prerequisites for the AG-ACNP role, forming the basis for all other competencies. It seems likely that this domain corresponds to the scientific foundation and basic skills needed for advanced practice, as seen in NONPF's scientific foundation competency.
	##Subdomain: Knowledge
		###Third-level category: Advanced Pathophysiology
		 This involves a deep understanding of how diseases and injuries affect body functions, focusing on complex mechanisms and interactions. For example, it includes studying the progression of acute conditions like sepsis or chronic diseases like heart failure in older adults. This aligns with AACN's emphasis on assessing health status and diagnosing illnesses, as part of the first domain.
		###Third-level category: Advanced Pharmacology
		 This includes comprehensive knowledge of medications, their actions, interactions, side effects, and appropriate use in various patient populations. It covers drug therapy for acute conditions, such as managing pain in critical care, and considers polypharmacy in older adults, reflecting NONPF's scientific foundation.
	##Subdomain: Skill
		###Third-level category: Advanced Physical Assessment
		 This is the ability to perform thorough physical examinations, interpret findings, and integrate them into accurate diagnoses and care plans. It involves skills like auscultation, palpation, and assessing for signs of acute distress, which are critical in acute care settings and align with AACN's focus on health assessment in the first domain.
#Domain: Clinical Practice
This domain focuses on the practical application of knowledge in providing care to patients, emphasizing clinical decision-making and management. It seems likely to correspond to AACN's domains like Health Promotion, Health Protection, Disease Prevention, and Treatment, and parts of Managing and Negotiating Healthcare Delivery Systems.
	##Subdomain: Knowledge
		###Third-level category: Standards of Care and Clinical Guidelines
		 This refers to understanding and adhering to established best practices, protocols, and guidelines for patient care, such as those from the AACN or clinical practice guidelines for acute care. It ensures consistency and quality in care delivery.
		###Third-level category: Standardized Assessment Tools
		 This involves knowing and using tools like pain scales, depression screens, or functional status assessments for systematic patient evaluation, which is crucial for standardized care in acute settings.
		###Third-level category: Psychosocial Factors
		 This covers understanding how emotional, cultural, and spiritual factors influence health and illness, integrating them into care plans. For example, addressing cultural preferences in end-of-life care for older adults.
		###Third-level category: Cost-Effective Care
		 This is knowledge of providing high-quality care while considering cost implications, ensuring efficient resource use, such as choosing cost-effective diagnostic tests.
		###Third-level category: Health Promotion and Disease Prevention
		 This includes understanding strategies like education, screening, and intervention techniques to promote health and prevent disease, even in acute care contexts, such as counseling on fall prevention for older adults.
	##Subdomain: Skill
		###Third-level category: Risk Stratification
		 This is the ability to identify patients at higher risk, such as those with physiological markers (e.g., high blood pressure) or from vulnerable populations (e.g., frail elderly), and tailor care accordingly, aligning with AACN's focus on managing complex conditions.
		###Third-level category: Diagnostic Testing and Procedures
		 This involves ordering, performing, and interpreting tests like lab work, imaging, or electrocardiograms to inform diagnosis and treatment, critical in acute care settings.
		###Third-level category: Non-Pharmacologic and Pharmacologic Treatments and Procedures
		 This is the ability to manage both non-drug treatments (e.g., physical therapy, positioning) and drug treatments, including performing procedures like central line insertion, reflecting the hands-on skills needed in acute care.
#Domain: Professional Role
This domain covers broader professional responsibilities, including leadership, advocacy, and system navigation beyond direct patient care. It seems likely to align with AACN's Professional Role and parts of Monitoring and Ensuring the Quality of Healthcare Practice, as well as NONPF's leadership and policy competencies.
	##Subdomain: Knowledge
		###Third-level category: Scope and Standards of Professional Practice
		 This is understanding the legal and professional boundaries of the AG-ACNP role, including what is within their scope (e.g., prescribing, procedures) and expected standards, as per the 2008 APRN Consensus Model.
		###Third-level category: Health Care Policy and Systems
		 This involves knowledge of healthcare policies, systems, and how to navigate them, such as understanding reimbursement models or advocating for policy changes to improve care for older adults.
		###Third-level category: Quality Improvement Processes
		 This includes understanding methods like continuous quality improvement models, data analysis, and performance metrics to enhance care quality, such as implementing fall prevention programs.
	##Subdomain: Skill
		###Third-level category: Research and Evidence-Based Practice:
		 This is the ability to apply research findings to practice, critically evaluate evidence, and potentially conduct research, aligning with NONPF's practice inquiry and quality competencies.
		###Third-level category: Educational Strategies and Health Literacy:
		 This involves effectively educating patients, families, and colleagues, considering health literacy levels, such as teaching families about managing chronic conditions in older adults.
		###Third-level category: Relationship Development(e.g., patient, family, inter-professional):
		 This is building and maintaining effective relationships with patients, families, and other healthcare professionals, ensuring coordinated and patient-centered care, which is crucial for interprofessional collaboration.
"""

perplexity_return_prompt = """
Please output a JSON object containing the following fields:
id, domain, subdomain, third_level_category, probability
"""
