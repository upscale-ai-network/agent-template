#!/usr/bin/env python3
"""Build DT100 draft PPTX from manager-arch-vision-a3.md / b6 content. Regenerate after md edits."""

from pathlib import Path
from typing import List, Optional

from pptx import Presentation
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
CONF = "Confidential — Upscale AI, Inc."
PIPELINE_IMG = ROOT / "assets" / "logical-pipeline-boss-slide.png"


def _blank(prs: Presentation):
    return prs.slide_layouts[6]  # blank


def _add_title_slide(prs: Presentation, title: str, subtitle: str):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = title
    slide.placeholders[1].text = subtitle


def _add_bullet_slide(
    prs: Presentation,
    title: str,
    bullets: List[str],
    subtitle: Optional[str] = None,
    notes: Optional[str] = None,
):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    body = slide.placeholders[1].text_frame
    body.clear()
    if subtitle:
        p = body.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(18)
        p.font.italic = True
        p.level = 0
        first = 1
    else:
        first = 0
    for i, line in enumerate(bullets):
        p = body.paragraphs[first + i] if first + i < len(body.paragraphs) else body.add_paragraph()
        p.text = line
        p.level = 0
        p.font.size = Pt(20)
    if notes:
        slide.notes_slide.notes_text_frame.text = notes
    return slide


def _add_image_slide(
    prs: Presentation, title: str, image_path: Path, caption: Optional[str] = None
):
    slide = prs.slides.add_slide(_blank(prs))
    tx = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(0.8))
    tx.text_frame.text = title
    tx.text_frame.paragraphs[0].font.size = Pt(28)
    tx.text_frame.paragraphs[0].font.bold = True
    slide.shapes.add_picture(str(image_path), Inches(0.5), Inches(1.1), width=Inches(12.3))
    if caption:
        cap = slide.shapes.add_textbox(Inches(0.5), Inches(6.8), Inches(12), Inches(0.6))
        cap.text_frame.text = caption
        cap.text_frame.paragraphs[0].font.size = Pt(14)


def build_a3() -> Path:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    _add_title_slide(
        prs,
        "Arch vision hook (A3)",
        "DT100 · Gururaj · Draft for review\n" + CONF,
    )

    script = (
        "~15s: Three slides — yes I can run this, how I'll run it, what I need from you. "
        "B6 if premise holds. Fix slide 1 first; don't open long deck until premise is good."
    )

    _add_bullet_slide(
        prs,
        "I can align SW validation to product, datapath, and silicon",
        [
            "My commitment: drive the cross-team validation framework; DRI for QoS / resource management (RM).",
            "Your question: SW done and validated with product, mgmt plane, datapath/AV, SDK/SAI before tape-out (C-models → emulation → silicon).",
            "Peers: Shafi Mohammad (L2/L3/ACL) and Tippanna Hongal (ECMP/AV) stay DRIs on their slices; I facilitate alignment.",
            "Today: premise and operating model — not full architecture (exec read stays 2-pager, not a 50-page dump).",
            "Sponsor: Gururaj · DRI: Diwakar Tundlam",
        ],
        subtitle="Framework first · 2-pager discipline · QoS/RM is my wedge",
        notes=script,
    )

    _add_bullet_slide(
        prs,
        "Operating model → Cx 2-pager in ~2 weeks",
        [
            "Cadence: Product/AV ↔ datapath ↔ validation gates → Amazon-style 2-pager decisions.",
            "Near term: Cx — validation gate definitions + QoS RM HWv1 scope (~2 weeks).",
            "On your pipeline slide: I own QoSMAP and Queue/buffer carve; Shafi (L2/ACL), Tippanna (ECMP) on theirs — B6 §6.",
            "Stay aligned: Rupa Budhia (datapath/OCP weekly); Prasun Sinha (program mesh).",
            "If premise holds: walk B6 next — or reshape hook on Fri.",
        ],
    )

    _add_bullet_slide(
        prs,
        "Sponsor decisions",
        [
            "Premise — Does slide 1 answer your question? If not, what should change?",
            "DRI split — Me: arch-vision framework + QoS RM; Shafi / Tippanna: their domains.",
            "OCP / external — Rupa and I coordinate technically; you own company position.",
            "Format — Thu async PDF vs short live walk vs Fri iteration (expect edits).",
            "Escalation — You step in if cross-architect validation alignment stalls.",
        ],
    )

    out = ROOT / "manager-arch-vision-a3.pptx"
    prs.save(out)
    return out


def build_b6() -> Path:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    _add_title_slide(
        prs,
        "Arch vision plan (B6)",
        "Companion to A3 · Walk if Yes · Draft\n" + CONF,
    )

    _add_bullet_slide(
        prs,
        "The question — and my answer (A3 slide 1 expanded)",
        [
            "Your question: SW done and validated with product, mgmt plane, datapath/AV, SDK/SAI proof before tape-out.",
            "My answer: drive 2-pager + validation-gate machine; DRI on arch-vision + QoS/RM (QoSMAP, queue/buffer carve).",
            "Peers: Shafi (L2/L3/ACL) and Tippanna (ECMP/AV) stay DRIs; I align the shared story, not their ownership.",
        ],
    )

    _add_bullet_slide(
        prs,
        "Document discipline (AWS-style)",
        [
            "Thu: A3 (2–3 slides) + this B6 (walkable, ≤6 sections in spirit).",
            "Next: Cx 2-pager — decisions, gates, open issues (~2 weeks).",
            "Not Thu: 50-page arch dump, full HW catalog digest.",
            "Exec read stays thin; full truth can exist later.",
        ],
    )

    _add_bullet_slide(
        prs,
        "End-to-end validation framework (I drive draft; peers align)",
        [
            "Product / customer use cases",
            "Arch validation (AV) ↔ datapath arch",
            "Mgmt plane — deployment-shaped (SONiC / FBOSS lands)",
            "SW validation ↔ C-models → emulation / FPGA → silicon",
            "SDK + SAI done with explicit gates before tape-out",
            "I socialize v0 of done per gate for group review — not unilateral mandate.",
        ],
    )

    _add_bullet_slide(
        prs,
        "DRI map",
        [
            "Sponsor / exec alignment: Gururaj",
            "Arch vision + validation program: Diwakar Tundlam",
            "QoS / buffer / queue / scheduler / RM carve: Diwakar Tundlam",
            "L2/L3 / ACL pipeline: Shafi Mohammad",
            "Arch validation / use-case framing: Tippanna Hongal",
            "SDK / SAI implementation: SDK leads (e.g. Girish, Shravan) — consult, not my R",
            "Program / sprint mesh: Prasun Sinha",
            "HW datapath / OCP ESUN: Rupa Budhia — weekly align before Thu OCP calls",
        ],
    )

    _add_bullet_slide(
        prs,
        "My wedge — QoS resource management (RM)",
        [
            "Classification: VLAN-PRI, TOS/DSCP → queues → schedulers",
            "Buffer management and carving (traffic / resource manager)",
            "Port speed and queue/port policy coherence",
            "ESUN — align buffer/TM design with standardization (OCP context)",
            "HWv1: mapping above; no MPLS EXP, no IPv6 priority mapping yet.",
            "HWv2: EXP + IPv6 pri — planned extension.",
        ],
    )

    if PIPELINE_IMG.exists():
        _add_image_slide(
            prs,
            "Logical pipeline (boss slide context)",
            PIPELINE_IMG,
            "My wedge: QoSMAP + Queue/buffer carve · Peers: Shafi (L2/ACL), Tippanna (ECMP), Rupa (parse/datapath)",
        )
    else:
        _add_bullet_slide(
            prs,
            "Logical pipeline (boss slide context)",
            ["See assets/logical-pipeline-boss-slide.png — export missing from repo."],
        )

    _add_bullet_slide(
        prs,
        "Pipeline DRIs on the picture (summary)",
        [
            "Ingress: Port → Parser → MyMAC · VLAN — parse correctness with Rupa",
            "L2: L2-FBD · UFH — Shafi Mohammad",
            "L3: VRF · Intf · L3-FIB · ESUN FDB — L3/ESUN peers + Rupa",
            "Forward + QoS: ECMP (Tippanna) · QoSMAP (me)",
            "Egress: NH · LAG · IACL · Queue · ports — Queue/carve: me · ACL: Shafi",
            "Validation: each block needs AV done + SW proof (C-model → emulation) before silicon.",
        ],
    )

    _add_bullet_slide(
        prs,
        "Whiteboards — RM / SDK context (§6a)",
        [
            "arch-vision: buffer carving (200G/400G/800G→SDK); lossy/lossless→PFC→Queues; WRED/ECN/PFC APIs; TC→queues; ESUN-QoS",
            "first-1-1: SONiC/FBOSS→SAI→SAI Adapter→USDK→ASIC; ties validation pyramid to SDK delivery",
            "Full annotations: manager-arch-vision-whiteboards.md · assets/pics/",
            "Your correction pass on whiteboard doc still open.",
        ],
    )

    _add_bullet_slide(
        prs,
        "Parallel track (out of Thu scope)",
        [
            "This B6: how I run DE role + QoS RM + validation framework (Gururaj 2-pager).",
            "Rupa thread: SDK/SAI/datapath-variant layout — related, different plan.",
            "Weekly sync with Rupa; do not merge the two plans on Thu.",
        ],
    )

    _add_bullet_slide(
        prs,
        "External / OCP ESUN",
        [
            "Attend OCP ESUN as directed; coordinate with Rupa before Thu 8AM BCM/vendor calls.",
            "SW architect on QoS/TM/ESUN — not full network-arch owner.",
            "Company position through Sponsor until redirected.",
        ],
    )

    _add_bullet_slide(
        prs,
        "~2 weeks → Cx 2-pager (draft outline)",
        [
            "Decision: validation gate definitions (C-model / emu / pre-tapeout) v0",
            "Decision: QoS RM HWv1 scope sign-off with HW datapath DRI",
            "Open issues: access to models, lab, repos",
            "Actions: cadence with Shafi, Tippanna, Rupa, Prasun",
            "Non-goals: full C40-class HW digest in Cx",
        ],
    )

    _add_bullet_slide(
        prs,
        "Execution mesh (hook — detail round 2)",
        [
            "Align task intake with SDK/ASIC milestones and SONiC/FBOSS release cadence",
            "Prasun Sinha — program touchpoint for sprint planning",
            "Prabu brainstorm (qos api, HW DR/DV ↔ SW UR/AV) — not Thu center unless asked",
            "Not Thu: full PM design or AI-scale GPU diagrams unless redirected",
        ],
    )

    _add_bullet_slide(
        prs,
        "Asks for Gururaj — delta beyond A3 slide 3",
        [
            "Premise, DRI, OCP, format, escalation are on A3 — detail only if needed.",
            "Thu package: A3 hook + optional B6 walk; Cx 2-pager ~2 weeks — OK?",
            "Cx scope v0: validation gates + QoS RM HWv1 sign-off — who must be in the room?",
            "Step in if validation-gate consensus stalls beyond normal peer DRI friction.",
        ],
    )

    _add_bullet_slide(
        prs,
        "What Thu is not",
        [
            "Not finished C40 or full HW-doc digest",
            "Not claiming SDK/SAI program ownership day one",
            "Not AI tooling / token policy (separate thread)",
            "Not a 50-page substitute — B6 is walkable backup, not a second 50-pager",
        ],
    )

    out = ROOT / "manager-arch-vision-b6.pptx"
    prs.save(out)
    return out


def main():
    a3 = build_a3()
    b6 = build_b6()
    print(f"Wrote {a3}")
    print(f"Wrote {b6} ({len(Presentation(b6).slides)} slides)")


if __name__ == "__main__":
    main()
