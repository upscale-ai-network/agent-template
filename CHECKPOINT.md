# CHECKPOINT — session handoff

**When:** 2026-06-16 (post scale-up team meeting) · **Phase:** in orbit — execute / SDK delivery · **twice-weekly** Guru team cadence  
**Authority:** git HEAD + this file · chat/canvas not authoritative

---

## Mandate (Guru sync — closed)

| Topic | Direction |
|-------|-----------|
| **Technical wedge** | **Queuing** · static buffer carving · port speed bifurcation · TDM calendar |
| **Hard deliverable** | **SDK** (SAI/USDK surface, demonstrable) — rest is enablement |
| **Your lane (Guru scale-up)** | **Queuing guy** — peer W DRIs · **Srikanth = QoS DRI** · **Shrawan = ACL** · etc. |
| **Peers** | **W co-build** — you DRI; they help flesh code · SDK · test framework · HW-arch-aligned design |
| **Srikanth** | **QoS DRI** · **qos-CCC (arch CCC)** — primary peer; upstream reqs after carve doc |
| **Guru interface** | **High-level sync only** — no unsolicited detailed status unless he asks |
| **Delivery** | Peer-reviewed docs → SharePoint · code · tests · DV parity with HW layer |

**Shared artifact:** `bugatti-csb-buffer-carving.pptx` (SharePoint · Guru unicast preview).

---

## Static carve — two layers (customer / service-provider)

| Layer | Who | Role | Status |
|-------|-----|------|--------|
| **Customer** | **Prabhu** | Consumes static buffer carving · port-speed **SDK API** (YAML, etc.) | Talked · subscribed · **not blocked on you** · parallel vertical (Girish lane) |
| **Service-provider (upstream)** | **Ranjit Parmar** | **DV HW** — static carving + port-speed **HW-validated** | **Aligned** · Vinesh **aligned** · fixed configs incoming |

**Ranjit sync (from invite ingest — Copilot 2026-06):**

| Field | Value |
|-------|-------|
| Subject | sync about DV \<-\> SDK |
| When | *Outlook calendar* — not in Copilot ingest; add datetime when copying event |
| Where | [Teams](https://teams.microsoft.com/meet/239750612616132?p=UtmXTWNxHL4q3wATsm) |
| Organizer | Diwakar Tundlam \<dtundlam@upscaleai.com\> |
| Invitee | Ranjit Parmar \<rparmar@upscaleai.com\> — **Accepted** |
| Start topic | Static buffer-carve **mapping** (SDK deliverable baseline) |

**Ranjit debrief (2026-06-13 — alignment done):**

- Ranjit **already talked to Guru** before meeting you
- You **sketched** buffer-carving block · upper interfaces · need **DV for lower-side interfaces**
- **Outcome:** aligned with **Ranjit’s view of Guru intent** — main win; rest is detail
- **Next:** chase names · replicate SW/HW/tools/code · get dirty
- **Blocker:** no **checkout** · no **runnable loop/script** — must hit **production orbit**, not planning layer
- **Referral:** **Vinesh Ambarish** — 1:1 **done** · aligned · **fixed configs** incoming
- **Pending:** **Venkatesh** — stop-by when convenient · same pod

**DV pod (Ranjit referral chain):**

| Person | Role / note |
|--------|-------------|
| **Ranjit Parmar** | Aligned · Guru picture · referrals |
| **Vinesh Ambarish** | **1:1 done** · aligned · fixed configs · whiteboard notes → digest after lunch |
| **Venkatesh** | Same pod · follow up as needed |
| **Dharmendra Patel** | **Manager** — all three report here · **co-located pod** |

**Hongal — N′ (2026-06-13):**

- Sync on walk/talk · **N′ for guidance** (stand-in N)
- **Repo path:** Hongal or **W** sets up **GitHub clone + build** to **parity in their layers** — then you insert **port-speed-management** + **buffer carving**
- **Sim gap (design issue):** those features **not emulated in HW or C models** — inherent difficulty simulating buffering in datapath
- **Implication:** you must **build the SDK layer that manages this anyway** — your hatch target
- **N ask:** design doc — **port speed mgmt** first (your 10GbE / port-speed background) → starting point for **static buffer carving arch**

**Vinesh Ambarish — debrief (1:1 done · aligned):**

- **Outcome:** aligned well · **fixed configs** (etc.) from Vinesh incoming
- **Whiteboard:** screenshot taken → **digest after lunch** → paste here for follow-up
- **Still need:** checkout + runnable loop when configs land (DT108/129)

**Homework stack (digest in flight):**

- Sampath block diagram · **Varsha intern report** — G-test testing docs
- Vinesh whiteboard notes (post-lunch)
- Hongal N′ → port-speed doc → static carve arch (DT127)

**Guru — Teams offline update (sent today):**

Low-intensity Qk update before possible **verbal status** in wider team meeting:

- Peer SDK DRIs: Hongal · Shrawan · Shafi (main) · Srikanth / Tilak via presentations
- Sampath — high-level guidance · block diagrams
- Varsha intern report — G-test testing docs (homework)
- Ranjit + Vinesh — 1:1 sync on DV support needed
- **Next:** digest → slides for **Shrawan / Shafi / Girish** review **early next week** — basic buffer carving SDK changes + testing plans
- **Ask:** aligns with expectations? steer / retune energy if needed

**Why sent (process):** Asked **Shafi** — formal vs verbal; he flagged **later meeting may go around for verbal**. Teams note = **5-min preview** so Guru hears nothing surprising · slightly long for skim but **complete** → avoids back-and-forth.

**Sampath Krishna — 1:30 PM (direct paste):**

| Field | Value |
|-------|-------|
| When | **1:30 PM** today · block 30 min · **~15 min** expected |
| Where | **Conference room** |
| **Why (Hongal)** | Guidance + high-level overview · Sampath helped bring up Hongal on **HW port-speed arch** |
| **Your mode** | **Listen · learn** — seek pointers · homework areas · strategic framing for **Ranjit (DV)** sync |
| **Goal** | Where your **SDK deliverable** sits in his mental model · how to engage **DV below** · **SDK SW above** |
| After | Follow up on **specific pointers** only — no status theater |

**Debrief (2026-06-13 — went well):**

- Drew **chip block diagram** — dies · D2D · CPU/host (PCI) · on-chip buffers · HW blocks (detail in **HW specs**)
- **Sampath** = Hongal-initiated path into detail **N expects you to work on**; cordial · learning mode · brief “where I fit” / deliverable alignment
- **His offer:** POC for **deeper HW-spec dive** — deferred today (time); you took **picture** → digest · verify vs specs later
- **Ranjit prep:** use diagram/spec context **internally** — **do not** anchor Ranjit call on “Sampath sent me” (peer trust · independent DV conversation)

**Ranjit conversation — framing (operational, not structural):**

| Do | Don't |
|----|--------|
| Peer DV sync · you as **SDK consumer** of validated baseline | Org-chart / HW arch vision / Guru “go figure” lecture |
| Ask: working **scripts · configs · static carve logic** already passing in DV | Collapse Sampath map into Ranjit lane |
| Learn their **working set · deliverables · handoff format** | Overplay “customer” role structurally |
| Build toward **SDK/SAI parity** with what DV already runs | Tie meeting to Hongal/Sampath narrative |

**Next hooks:** picture → notes · Sampath spec deep-dive · Ranjit names → **checkout + loop** (DT108/DT129).

**You (DRI):** ship SDK surface between Ranjit's validated HW config and Prabhu's subscribed API consumer path — **with W team filling in implementation detail** (not solo).

**Prabhu — walk sync (2026-06-14):**

- **Ask:** blocked on anything from you? (up to his customer — same obsession chain)
- **Answer:** not blocked · busy on **parallel path** (other vertical · **Girish** lane — IMHO) · let it run in parallel · not your lane
- **Purpose:** leg work / slice offering to **N** — clears path to **SDK buffer-carving doc spec** without customer-side stall

**Deliverable doc (immediate):**

- **Reference (existing):** `~/Downloads/SDK Architecture for Bugatti.docx` — 5.8 MB · 2026-06-16 · align buffer-carve spec · may **integrate with other verticals** in this overall doc
- **Template (blank):** `~/Downloads/Upscale AI Software Team Template - Copy and Use.docx` — 2.5 MB · 2026-06-16 15:01 · **copy-and-use basis** for carve spec draft → repo copy TBD
- Target: draft for **Shafi review early next week** (per Guru/N update · DT127/128)

---

## Scale-up team meeting (9 PM · Guru · first full team)

- **Verbal update:** given · bit **short/rushed** (last name · well past 30 min) — polish over time · **win for today**
- **Cadence:** **twice-weekly** team meetings · Guru-led · **firmly in orbit**
- **JIRA:** none assigned yet · **Guru:** create your own JIRAs and track them → **[DT132](TASKS.md)**
- **EOD today:** two JIRAs filed — **(1) queuing epic** + first-cut tasks · DV-aligned · **emulation goal** · **(2) Prabhu epic**
- **Office:** work with **Prabhu** on customer epic · queuing breakdown from DV/W homework

**Guru 1:1 (scheduled · verbal request · 1:35 PM today):**

**Format:** **no slides** · **whiteboard / raw sketch** · listen · guidance · feedback · spider-sense for **his pain point** (don't probe his private work — support via leg-work).

**Hypothesis (watch, don't assume):** HW **emulation completion** · **queuing feature at SDK layer** — he may be hands-on (**Verilator**, etc.); your job = enable that orbit, not diagnose his stack.

Walk-through of learnings:

| Source | Content |
|--------|---------|
| **DV** | Vinesh · Ranjit — sync · fixed configs · lower interfaces |
| **HW** | Sampath — high-level chip details |
| **W** | Shafi · **Thippanna** — overall guidance |

**EOD commit (sent to Guru):**

1. **Queuing epic** — first-cut task breakdown · align **DV status** · focused on **emulation goal**
2. **Prabhu epic** — customer / SAI layer item

**Scope (mandate recap):** queuing design · port speed bifurcation design doc · align **DV test systems** · workaround poor/missing **bandwidth/buffering sim** in HW/emulation · interface **datapath** on ports · feeds · tests

**W lane map (scale-up):**

| DRI | Lane |
|-----|------|
| **You** | Queuing · buffer carve · port speed |
| **Srikanth** | **QoS DRI** · qos-CCC arch |
| **Shrawan** | ACL |
| **Prabhu** | SAI layer · your **customer** for JIRA + API path |

---

## W co-build (static-buffer-carving-ccc)

**Model:** You own wedge + design doc + CCC narrative · **W helps you build** the parts you don't own alone.

| W lane | Typical help |
|--------|----------------|
| **Shafi** | SDK · SAI · code paths · integration detail |
| **Shrawan** | ACL · classify · SDK-adjacent datapath |
| **Srikanth** | **QoS DRI** · qos-CCC arch · primary queuing peer · downstream reqs (after v0) |
| **Hongal** | ECMP/AV · test methodology · peer review · **N′** · repo/build onboarding |
| **Tilak** | L2-SDK-CCC template · SDK CCC shape |
| **Others as needed** | Testing framework · YAML/API conventions · HW arch alignment |

**Artifact:** **static-buffer-carving-ccc** — design + details that **match HW arch** (Ranjit baseline) · peer-reviewed before SharePoint.

**Not:** solo spec in a vacuum · not Guru detail status · not relitigating launch decks.

---

## Immediate queue (P0)

| # | Task | Notes |
|---|------|-------|
| 0 | **Create + track JIRAs (EOD today)** | Queuing epic + Prabhu epic · Guru 1:35 PM walk-through first | [DT132](TASKS.md) |
| 1 | **Static carve design doc v0** | Queuing · port speed bifurcation · TDM · HW baseline | [DT127](TASKS.md) |
| 2 | **SDK buffer-carve-CCC deck** | Model after **Tilak L2-SDK-CCC** · W review next week | [DT128](TASKS.md) |
| 3 | **SDK/SAI static carve path** | **Ranjit** HW baseline → SDK/SAI · **Prabhu** API consumer | [DT129](TASKS.md) |
| 4 | **Srikanth alignment** | Req handoff line: SDK static carve → qos-CCC downstream | [DT130](TASKS.md) |

---

## Dev VM (Girish · 2026-06-17)

| Field | Value |
|-------|-------|
| **Host** | `sw-hq-runner4` |
| **User** | `vtundlam` (typo) → **`dtundlam`** (creating correct account) |
| **OS** | Ubuntu 24.04.4 LTS |
| **SSH** | migrate to `dtundlam@sw-hq-runner4` when ready |
| **Tools** | podman · cmake · make · git · git-lfs · emacs · vim · aptitude — **manually verified (crawl done)** |
| **Credentials** | **Not in git** — password manager · password rotated · authorized_keys · GitHub TBD |

**VM notes:** crawl → walk → run · explore/digest later if needed · else sits in git like `.bash_history`.

**Local linux VM (macOS):** `ssh diwakar@192.168.64.3` — key-based from iTerm2 · e.g. `ssh diwakar@192.168.64.3 date` · **ntpd-rs** · TZ `America/Los_Angeles`

**Corp runner:** `sw-hq-runner4` — see above · `dtundlam` account fix in progress

**Next on VM:** ~~SSH key~~ **authorized_keys** from macOS + linux-vm · password rotated · **GitHub** access for clone/push (later) · git identity · **bugatti-model** URL from Shafi/Hongal (DT108).

---

- **No 1:1 performance loop** — audition complete; execute on **W**
- **Sync at gates** — direction / steer only
- **Teams Qk update sent** (2026-06) — peer/DV homework · early-next-week W review target · explicit align/steer ask
- **Scale-up meeting (9 PM):** verbal update · **twice-weekly** cadence · **self-created JIRAs** required
- **1:35 PM 1:1 (today):** thoughts from DV · Sampath · Shafi/Thippanna · EOD = two epics filed
- **Do not** escalate to detailed unilateral status beyond this cadence unless he asks

---

## W interface

- Verbal update done: Shrawan · Shafi · Hongal (Guru sync + thank-you)
- **Mode:** **co-build** — pull W into code · SDK · testing framework · HW-arch-aligned design detail
- **Next:** **static-buffer-carving-ccc** — L2-SDK-CCC shape · W review next week
- **Build together:** design doc v0 · SW · tests · SharePoint after peer review

---

## Repo / Gluon mode

| Mode | Role |
|------|------|
| **Launchpad** | Closed — DT100 · DT122 · Guru walk |
| **Houston (steady)** | **Lower cadence** governance — CHECKPOINT/TASKS on debrief · human navigates parallel lanes |
| **Coding agent** | **Primary** — Cursor in product repo once checkout lands; implement · debug · loop |
| **PPTX** | Quasi-manual delivery OK · md/build pipeline secondary until reunified |

**Steady phase (2026-06-13):** executive seats filled or acting chairs seated · full **parallel task** work · you DRI navigation · Gluon = code + occasional checkpoint hygiene (not daily orchestration).

**Night state (2026-06-16):** in orbit · engines off · lattice cool · **DT132** first motion tomorrow (Prabhu · JIRAs).

**Build (when needed):** `uv run build-decks` · golden hashes in `tests/fixtures/published-deck-hashes.txt`

**Terms:** [assets/guru-terms-sot.md](assets/guru-terms-sot.md) — **CSB** = Central Scheduler Block (HW arch)

---

## Human — do not ask Gluon to

- Commit/push without explicit OK ([DT119](TASKS.md))
- Email Guru detailed status unsolicited
- Message W/E/sponsor directly ([CONSTITUTION.md](CONSTITUTION.md) Rule 8)
- Store VM passwords or credentials in git-tracked files

---

## Stale — ignore

Pre-2026-06-12 rows in this file about Hongal 3pm · Fri hold · zombie standby — superseded by mandate above.
