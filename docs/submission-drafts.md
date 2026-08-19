# Reusable Devpost submission drafts

These drafts describe only functionality present in this repository. Cloud
deployment, public repository and video links must be added only after they
exist.

## Google — All Things Agentic Hackathon

**Working title:** PrizePilot Agent — Approval-First Opportunity Operations

**Category:** Taskmaster

### Inspiration

Applying to competitions and grants is a messy, repetitive workflow. The same
profile, evidence and project facts are copied into different formats, while a
single invented eligibility claim can invalidate the whole application. Solo
builders need automation, but they also need control over what leaves their
computer.

### What it does

PrizePilot turns opportunity rules, an owner profile and a reusable evidence
library into a concise action queue. A deterministic gate blocks ineligible
opportunities and labels missing evidence before the agent writes persuasive
copy. Eligible work is drafted by an agent, deduplicated across applications and
stopped at a human approval checkpoint before external transmission.

### How we built it

The Google build uses Gemini 3.5 through Google ADK. The API is containerized for
Cloud Run, with Firestore planned for durable opportunity, evidence and approval
records. The deterministic Python gate remains authoritative: the model can
suggest an action, but it cannot turn an unknown fact into an eligibility pass.

### Challenges

The hardest product decision was defining the boundary between useful autonomy
and unsafe representation. We separated eligibility from generation, made
unknown evidence an explicit state and designed a single approval object that
records the destination, data categories and action.

### Accomplishments

- Runnable approval-queue MVP with a responsive web interface.
- Deterministic hard-gate tests for missing evidence and disqualifying criteria.
- Google ADK and AWS Strands adapters around one provider-independent safety core.
- Cloud Run build configuration and a standalone local demo with no credentials.

### What we learned

High-quality automation is not measured by the number of clicks removed. It is
measured by how many routine decisions it can make correctly while making the
few remaining human decisions obvious and auditable.

### What's next

Connect Gemini to rule extraction, add Firestore persistence, deploy on Cloud
Run, and record the required end-to-end demo with the cloud execution visible.

## AWS — Agents for Humans Hackathon

**Working title:** PrizePilot Agent — The Application Work Nobody Should Repeat

**Track:** Professional Agents

### What it does

PrizePilot handles the repetitive work around competitions and grant
applications for solo founders and small teams. It normalizes requirements,
checks hard eligibility, assembles evidence-backed drafts and queues only the
decisions that genuinely need the owner. It never invents credentials or sends
an application without an explicit approval record.

### Why it matters

Professionals lose hours reformatting the same facts across portals. The cost is
not only time: rushed applications create unsupported claims and missed gates.
PrizePilot converts that fragmented work into one auditable workflow.

### Technical implementation

The AWS build wraps the deterministic eligibility engine in Strands Agents SDK.
The agent plans the next useful action while the gate enforces verified facts.
The web UI visualizes ready, evidence-needed and safely blocked states. AgentCore
is the preferred deployment target once an AWS account and credits are active.

### Current evidence

The local MVP and tests are working. No customer traction, win-rate improvement
or measured time saving is claimed yet.

