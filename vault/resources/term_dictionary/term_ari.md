---
tags:
  - resource
  - terminology
  - team
  - operations
keywords:
  - ARI
  - Abuse Risk Investigation
  - manual investigation
  - account closure
  - concessions abuse
  - quantity limit
  - claims abuse
topics:
  - buyer abuse prevention
  - operations
  - investigation
language: markdown
date of note: 2026-01-24
status: active
building_block: concept
---

# ARI - Abuse Risk Investigation

**Status**: ✅ Active

**Full Name**: Abuse Risk Investigation

**Category**: Operations Team / Manual Investigation

**Former Name**: Concessions Investigation Specialist (CIS)

## Overview

ARI (Abuse Risk Investigation) is the manual investigation team primarily responsible for **protecting the profitability, brand, and reputation of Amazon businesses exposed to customer abuse while maintaining a high bar of customer experience**. The team handles complex abuse cases that require human judgment and performs account closure actions when automated systems are insufficient.

ARI formerly known as Concessions Investigation Specialist (CIS), is responsible for investigating and taking enforcement actions on customers who systematically and consistently violate Amazon's terms and conditions across any Amazon business.

## Key Responsibilities

ARI investigates and enforces on the following abuse types:

1. **Concessions Abuse** - Repeated false claims for refunds, replacements, and returns
2. **Quantity Limit Abuse (QL)** - Circumventing purchase limits on discounted/limited items
3. **Claims Abuse** - False A-to-Z claims on MFN orders
4. **Rejects Abuse** - Inventory hold through false package rejections
5. **Digital Content Abuse** - Kindle and digital content refund abuse
6. **Prime Abuse** - Commercial use of Prime memberships, multiple free trials

## Mission & Vision

**Mission**: Protect Amazon's profitability, brand, and reputation from customer abuse while maintaining high customer experience standards

**Vision**: "Abuse Risk Investigations provide outstanding investigation quality to build an Abuse free Amazon. We always value our people, encourage their development and reward their performance"

**Investigation Principle**: "Investigate Abusers, Not Customers" - ARI focuses on systematic, repeated violations rather than isolated incidents

**Scale**: ARI investigators review approximately **~25M cases/year** to detect and enforce bad actors across **21 stores globally**, with **+1,000 investigators** across 3 geographical locales playing a critical role in preventing abuse

## ARI Tenets (Operating Principles)

1. **Presume customer innocence** where there is lack of evidence
2. **Automate wherever possible** to keep false positives low and customer experience high
3. **Silent investigations** wherever possible to reduce negative customer experience impact
4. **Clear, consistent communication** with customers through every point in the workflow
5. **Advocate for clear policies** in terms and conditions with systematic enforcement
6. **Business isolation** - Account closure in one business shouldn't impact other businesses
7. **Graduated enforcement** - Always warn customers before more extreme actions (Three-Strike Policy: Solicit → Warn → Close)
8. **Build accurate automation** to reduce investigator overhead; err towards investigation when uncertain

## Global Coverage

- **Marketplaces**: 12 marketplaces globally
- **Investigation Sites**: 7 sites worldwide
  - **HYD (Hyderabad)**: US, UK, CA, IN, DE, JP
  - **BLR (Bangalore)**: IN
  - **LHR (London)**: DE, FR, IT, ES (EU4)
  - **SEA (Seattle)**: JP, CN
  - **CTS (Chitose)**: JP
  - **HND (Tokyo)**: JP
  - **PEK (Beijing)**: CN
  - **SHA (Shanghai)**: CN
  - **SJO (San Jose, Costa Rica)**: DE, IT, ES, BR, MX

## Key Metrics & Goals

### Operational Metrics
- **SIPH (Solves per Investigator Hour)** - Productivity measure: total investigations completed & average handle time
- **PAR (Policy Adherence Rate)** - Decision quality: impact of investigator decisions on customer experience
- **SLA (Service Level Agreement)** - Timely resolution of investigations
  - Fast Track (FT): 4 hours
  - Email contacts: 12 hours
  - APS sync investigations: 12 hours
  - Claims abuse: 36 hours
  - Reseller cluster: 24-36 hours
- **First Contact Resolution** - Contacts reinstated in first contact

### Quality Metrics
- **UE (Under Enforcement)** - Investigations where enforcement action was missed, leading to negative impact
- **OE (Over Enforcement)** - Customer accounts reinstated/cleared after incorrect enforcement
- **Abuse Loss** - Financial loss due to policy abuse as percentage of GMS (Gross Merchandise Sales)

## Tools & Systems

### Primary Investigation Tools
1. **Investigation Workbench (IW)** - Main investigation platform for queue management and case handling
2. **Nautilus** - Buyer-side investigation platform for account attributes, order information, and investigation actions
3. **Customer Service Central (CSC/Texas)** - View customer account details, order information, edit feedback

### Supporting Systems
- **HULK (Heartbeat Bulk)** - Mass operations tool for emails, cancellations, annotations
- **LEADS** - Jupiter extension for viewing/editing buyer and seller account details
- **AbuseVCS** - Variable computation service for risk evaluation
- **AbuseSIL** - Workflow system processing investigator actions
- **APWS (Abuse Prevention Workflow Service)** - Workflow orchestration for investigations

## Enforcement Actions

ARI follows graduated enforcement approach:

1. **Solicit (Inquiry)** - Initial contact to gather information
2. **Warn (Formal Warning)** - Official warning about policy violations
3. **Close (Account Closure)** - Permanent account suspension for continued abuse

**Note**: TRMS does not cancel Amazon accounts for Prime abuse alone - only Prime memberships are revoked without refund and customer is banned from Prime

## Evolving Role in the Era of AI/ML

As Buyer Abuse Prevention evolves toward more automated detection and enforcement systems powered by LLMs and advanced ML models, ARI's role is transforming:

**Traditional Role** (Reactive):
- Manual investigation of queued cases
- Primary decision-makers for enforcement actions
- Focus on individual case evaluation

**Evolving Role** (Proactive):
- **Critical feedback providers** - Implant reasoning into systems by providing chain-of-thought prompts to LLMs
- **Model output reviewers** - Monitor system outputs to ensure they are unbiased and not hallucinating
- **Customer experience protectors** - Focus on proving automated systems wrong and discovering false positives
- **Pattern discoverers** - Identify new abuse patterns (MOs) to feed automation systems
- **Quality gatekeepers** - Shift from detecting guilt to detecting innocence in automated enforcement decisions

**Future Vision**: "Enforcements must be primarily automated, and abuse risk investigators will focus on proving the system wrong and discovering new patterns to feed our automations." This represents a paradigm shift from rule-based evaluation to AI-powered automation with human-in-the-loop oversight.

**New Investigation Dimensions**:
- **Micro-level**: Individual transactions and accounts (Helene tool)
- **Mid-level**: Clusters of related accounts (Tattletale/TTUX tool)
- **Macro-level**: Emerging abuse trends across the globe (Chronographer tool - in development)

## Relationship to Other Teams

### Partner Teams
- **[BAP](term_bap.md) (Buyer Abuse Prevention)** - Engineering and ML team building detection systems and prevention workflows
- **[CAP](term_cap.md) (Concessions Abuse Prevention)** - Customer Service team handling high-risk customer contacts with RSPR guidance
- **[BRI](term_bri.md) (Buyer Risk Investigations)** - Fraud investigation team focusing on payment fraud vs concessions abuse
- **Abuse Risk Mining (ARM)** - Analyzes fraud patterns to identify system misses and create mitigation mechanisms

### Escalation Path
- **BRI → ARI**: Payment fraud investigators can refer concessions abuse cases to ARI
- **CAP → ARI**: High-risk contacts requiring deeper investigation
- **ARM ← ARI**: ARI submits MO (Modus Operandi) tips for pattern analysis

## Investigation Process

1. **Detection** - Automated systems (APS, Fortress, PFOC) or manual referrals queue customers
2. **Investigation** - ARI investigators review evidence using Nautilus, IW, and supporting tools
3. **Decision** - Take enforcement action based on evidence: Pass, Warn, or Close
4. **Communication** - Clear communication to customer about decision and next steps
5. **Appeal** - Customers can appeal decisions; ARI reviews appeals with appropriate stakeholders

## Main GPO Contact

**Amresh Kumar** (kamresh) - Global Process Owner for ARI

## Key Wiki Pages

- **[ARI Home Page](https://w.amazon.com/bin/view/ARI/)** - Main home page for Abuse Risk Investigation team
- **[Buyer Abuse Home Page](https://w.amazon.com/bin/view/BuyerAbuse/)** - Buyer Abuse Prevention team wiki home
- **[ARI Landing Page (TRMS)](https://w.amazon.com/bin/view/TRMS_Landing_Page/url%3ATRMS_OBX/url%3ATRMS_Process_Ops_Functions/url%3AARI_%28Abuse_Risk_Investigations%29/)** - Detailed reference with tenets, goals, tools, and contact information
- **[ARI Command Center](https://w.amazon.com/bin/view/TRMS_COMMAND_CENTER/ARI/)** - Operational monitoring dashboards
- **[Abuse Prevention Open Office Hours](https://w.amazon.com/bin/view/AbusePrevention/OpenOfficeHours/)** - Weekly office hours for questions and collaboration

## Contact & Support

- **SOP/Blurb Issues**: [Raise SIM](https://issues.amazon.com/issues/create?assignedFolder=89a45f52-2538-4720-9732-a1c18cea139a)
- **Training Issues**: [Raise SIM](https://issues.amazon.com/issues/create?assignedFolder=89a45f52-2538-4720-9732-a1c18cea139a)
- **Report Fraud**: [Raise SIM](https://issues.amazon.com/issues/create?assignedFolder=89a45f52-2538-4720-9732-a1c18cea139a)
- **Email**: ari-leads@amazon.com (for investigation requests)
- **Office Hours**: [Abuse Prevention Open Office Hours](https://w.amazon.com/bin/view/AbusePrevention/OpenOfficeHours/)

## Related Terms

### Financial Impact
- **[Bad Debt](term_bad_debt.md)** - ARI investigations lead to enforcements that prevent future Bad Debt by closing fraudulent accounts before they generate chargebacks

- [BAP](term_bap.md) - Buyer Abuse Prevention (Engineering team)
- [CAP](term_cap.md) - Concessions Abuse Prevention (Customer Service team)
- [BRI](term_bri.md) - Buyer Risk Investigations (Fraud team)
- [TSE](term_tse.md) - Trustworthy Shopping Experience (A-to-Z, product quality)
- [Nautilus](term_nautilus.md) - Primary investigation platform
- [Paragon](term_paragon.md) - Seller/Abuse investigation platform
- [MONRAD](term_monrad.md) - Investigation case/task management service
- [PFOC](term_pfoc.md) - Pre-Fulfillment Order Cancellation
- [QL](term_qla.md) - Quantity Limit Abuse
- [MAA](term_maa.md) - Multi-Account Abuse
- [DNR](term_dnr.md) - Delivered Not Received
- [MDR](term_mdr.md) - Materially Different Returns
- [Three-Strike Policy](#enforcement-actions) - Graduated enforcement approach
- [Holdout Analysis](term_holdout_analysis.md) - False positive measurement for account closures; holdout observation is separate from ARI investigation queues

## Historical Context

- **Original Name**: Concessions Investigation Specialist (CIS)
- **Current Organization**: Part of WW Selling Partner Services (SPS), formerly CTPS, originally TRMS
- **Evolution**: Expanded from concessions-only to cover multiple abuse vectors including QL, Claims, Rejects, and Digital Content

## Key Differentiators

**ARI vs BRI**:
- **ARI**: Concessions abuse (false claims, refunds, returns)
- **BRI**: Payment fraud (stolen credit cards, unauthorized charges)

**ARI vs CAP**:
- **ARI**: Deep investigations requiring account closure decisions
- **CAP**: Front-line contact handling with RSPR guidance for policy adherence

---

**References**:
- [ARI Home Page](https://w.amazon.com/bin/view/ARI/)
- [Buyer Abuse Home Page](https://w.amazon.com/bin/view/BuyerAbuse/)
- [ARI Landing Page](https://w.amazon.com/bin/view/TRMS_Landing_Page/url%3ATRMS_OBX/url%3ATRMS_Process_Ops_Functions/url%3AARI_%28Abuse_Risk_Investigations%29/)
- [ARI Command Center](https://w.amazon.com/bin/view/TRMS_COMMAND_CENTER/ARI/)
- [BRP Guardians Glossary](https://w.amazon.com/bin/view/BuyerRiskPrevention/AccountIntegrity/Guardians/Glossary/)

---

**Last Updated**: 2026-01-24  
**Status**: Active - Comprehensive documentation with wiki references
