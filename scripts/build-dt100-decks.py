#!/usr/bin/env python3
"""
Build DT100 A3/B6 PPTX using Upscale company slide chrome from Bugatti CCC deck.
Clones decorated slides (logo, footer, colors) and replaces text only.
"""

import shutil
import sys
from pathlib import Path
from typing import List, Optional

from pptx import Presentation
from pptx.util import Inches

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from pptx_util import (  # noqa: E402
    check_zip_duplicates,
    fill_content_slide,
    fill_cover_slide,
    trim_to_slides,
)
PIPELINE_IMG = ROOT / "assets" / "logical-pipeline-boss-slide.png"

# Company style source (32-slide CCC deck — keep local; optional copy under assets/templates)
STYLE_DOWNLOAD = Path.home() / "Downloads" / "Mirror-Sflow-Bugatti-ASIC-CCC.pptx"
STYLE_REF = ROOT / "assets/templates/upscale-ccc-style-reference.pptx"

IDX_COVER = 0       # UP upscale ai cover + footer
IDX_CONTENT = 2     # title + body bullets (standard inner slide)
IDX_BLANK = 31      # blank by design (fallback)


def ensure_style_reference() -> Path:
    if STYLE_REF.exists():
        return STYLE_REF
    if STYLE_DOWNLOAD.exists():
        STYLE_REF.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(STYLE_DOWNLOAD, STYLE_REF)
        return STYLE_REF
    raise FileNotFoundError(
        f"Company style deck not found. Download CCC PPTX to {STYLE_DOWNLOAD} "
        f"or copy to {STYLE_REF}"
    )


class StyledDeck:
    """Copy CCC deck, trim to cover + N real content slides (no XML duplicate)."""

    def __init__(self, out_path: Path, num_content_slides: int):
        ref = ensure_style_reference()
        shutil.copy2(ref, out_path)
        self.path = out_path
        self.prs = Presentation(str(out_path))
        keep = [IDX_COVER] + list(range(IDX_CONTENT, IDX_CONTENT + num_content_slides))
        if keep[-1] >= len(self.prs.slides):
            raise ValueError(f"CCC deck needs {keep[-1] + 1} slides, has {len(self.prs.slides)}")
        trim_to_slides(self.prs, keep)
        self._slide_i = 1

    def add_cover(self, headline, subline, meta, tag, notes=None):
        fill_cover_slide(self.prs.slides[0], headline, subline, meta, tag)
        if notes:
            self.prs.slides[0].notes_slide.notes_text_frame.text = notes

    def add_content(self, title, bullets, subtitle=None, notes=None):
        slide = self.prs.slides[self._slide_i]
        self._slide_i += 1
        fill_content_slide(slide, title, bullets, subtitle=subtitle)
        if notes:
            slide.notes_slide.notes_text_frame.text = notes
        return slide

    def add_image_slide(self, title, image_path: Path, caption: Optional[str] = None):
        slide = self.add_content(title, [caption] if caption else [])
        slide.shapes.add_picture(str(image_path), Inches(0.55), Inches(1.35), width=Inches(12.0))
        return slide

    def save(self):
        self.prs.save(str(self.path))
        dups = check_zip_duplicates(self.path)
        if dups:
            print(f"WARNING {self.path.name}: duplicate zip parts: {dups}")
        else:
            print(f"ZIP OK: {self.path.name}")
        return self.path


def build_a3() -> Path:
    out = ROOT / "manager-arch-vision-a3.pptx"
    deck = StyledDeck(out, num_content_slides=3)
    script = (
        "~15s: Three slides — yes I can run this, how I'll run it, what I need from you. "
        "B6 if premise holds. Fix slide 1 first; don't open long deck until premise is good."
    )

    deck.add_cover(
        "Arch vision hook (A3)",
        "DT100 · Gururaj",
        "Draft for review",
        "Confidential — Upscale AI",
    )

    deck.add_content(
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

    deck.add_content(
        "Operating model → Cx 2-pager in ~2 weeks",
        [
            "Cadence: Product/AV ↔ datapath ↔ validation gates → Amazon-style 2-pager decisions.",
            "Near term: Cx — validation gate definitions + QoS RM HWv1 scope (~2 weeks).",
            "On your pipeline slide: I own QoSMAP and Queue/buffer carve; Shafi (L2/ACL), Tippanna (ECMP) on theirs — B6 §6.",
            "Stay aligned: Rupa Budhia (datapath/OCP weekly); Prasun Sinha (program mesh).",
            "If premise holds: walk B6 next — or reshape hook on Fri.",
        ],
    )

    deck.add_content(
        "Sponsor decisions",
        [
            "Premise — Does slide 1 answer your question? If not, what should change?",
            "DRI split — Me: arch-vision framework + QoS RM; Shafi / Tippanna: their domains.",
            "OCP / external — Rupa and I coordinate technically; you own company position.",
            "Format — Thu async PDF vs short live walk vs Fri iteration (expect edits).",
            "Escalation — You step in if cross-architect validation alignment stalls.",
        ],
    )

    return deck.save()


def build_b6() -> Path:
    out = ROOT / "manager-arch-vision-b6.pptx"
    deck = StyledDeck(out, num_content_slides=14)

    deck.add_cover(
        "Arch vision plan (B6)",
        "Companion to A3",
        "Walk if Yes · Draft",
        "Confidential — Upscale AI",
    )

    sections = [
        (
            "The question — and my answer (A3 slide 1 expanded)",
            [
                "Your question: SW done and validated with product, mgmt plane, datapath/AV, SDK/SAI proof before tape-out.",
                "My answer: drive 2-pager + validation-gate machine; DRI on arch-vision + QoS/RM (QoSMAP, queue/buffer carve).",
                "Peers: Shafi (L2/L3/ACL) and Tippanna (ECMP/AV) stay DRIs; I align the shared story, not their ownership.",
            ],
            None,
        ),
        (
            "Document discipline (AWS-style)",
            [
                "Thu: A3 (2–3 slides) + this B6 (walkable).",
                "Next: Cx 2-pager — decisions, gates, open issues (~2 weeks).",
                "Not Thu: 50-page arch dump, full HW catalog digest.",
                "Exec read stays thin; full truth can exist later.",
            ],
            None,
        ),
        (
            "End-to-end validation framework (I drive draft; peers align)",
            [
                "Product / customer use cases",
                "Arch validation (AV) ↔ datapath arch",
                "Mgmt plane — deployment-shaped (SONiC / FBOSS lands)",
                "SW validation ↔ C-models → emulation / FPGA → silicon",
                "SDK + SAI done with explicit gates before tape-out",
                "I socialize v0 of done per gate for group review — not unilateral mandate.",
            ],
            None,
        ),
        (
            "DRI map",
            [
                "Sponsor / exec alignment: Gururaj",
                "Arch vision + validation program: Diwakar Tundlam",
                "QoS / buffer / queue / scheduler / RM carve: Diwakar Tundlam",
                "L2/L3 / ACL pipeline: Shafi Mohammad",
                "Arch validation / use-case framing: Tippanna Hongal",
                "SDK / SAI: SDK leads (e.g. Girish, Shravan) — consult, not my R",
                "Program / sprint mesh: Prasun Sinha",
                "HW datapath / OCP ESUN: Rupa Budhia — weekly align before Thu OCP calls",
            ],
            None,
        ),
        (
            "My wedge — QoS resource management (RM)",
            [
                "Classification: VLAN-PRI, TOS/DSCP → queues → schedulers",
                "Buffer management and carving (traffic / resource manager)",
                "Port speed and queue/port policy coherence",
                "ESUN — align buffer/TM design with standardization (OCP context)",
                "HWv1: mapping above; no MPLS EXP, no IPv6 priority mapping yet.",
                "HWv2: EXP + IPv6 pri — planned extension.",
            ],
            None,
        ),
    ]

    for title, bullets, sub in sections:
        deck.add_content(title, bullets, subtitle=sub)

    if PIPELINE_IMG.exists():
        deck.add_image_slide(
            "Logical pipeline (boss slide context)",
            PIPELINE_IMG,
            "My wedge: QoSMAP + Queue/buffer carve · Peers: Shafi (L2/ACL), Tippanna (ECMP), Rupa (parse/datapath)",
        )
    else:
        deck.add_content("Logical pipeline (boss slide context)", ["See assets/logical-pipeline-boss-slide.png"])

    more = [
        (
            "Pipeline DRIs on the picture (summary)",
            [
                "Ingress: Port → Parser → MyMAC · VLAN — parse correctness with Rupa",
                "L2: L2-FBD · UFH — Shafi Mohammad",
                "L3: VRF · Intf · L3-FIB · ESUN FDB — L3/ESUN peers + Rupa",
                "Forward + QoS: ECMP (Tippanna) · QoSMAP (me)",
                "Egress: NH · LAG · IACL · Queue · ports — Queue/carve: me · ACL: Shafi",
                "Validation: each block needs AV done + SW proof (C-model → emulation) before silicon.",
            ],
        ),
        (
            "Whiteboards — RM / SDK context (§6a)",
            [
                "arch-vision: buffer carving; lossy/lossless→PFC→Queues; WRED/ECN/PFC; ESUN-QoS",
                "first-1-1: SONiC/FBOSS→SAI→USDK→ASIC; ties validation pyramid to SDK delivery",
                "Annotations: manager-arch-vision-whiteboards.md · assets/pics/",
            ],
        ),
        (
            "Parallel track (out of Thu scope)",
            [
                "This B6: DE role + QoS RM + validation framework (Gururaj 2-pager).",
                "Rupa thread: SDK/SAI/datapath layout — related, different plan.",
                "Weekly sync with Rupa; do not merge the two plans on Thu.",
            ],
        ),
        (
            "External / OCP ESUN",
            [
                "Attend OCP ESUN as directed; coordinate with Rupa before Thu 8AM BCM/vendor calls.",
                "SW architect on QoS/TM/ESUN — not full network-arch owner.",
                "Company position through Sponsor until redirected.",
            ],
        ),
        (
            "~2 weeks → Cx 2-pager (draft outline)",
            [
                "Decision: validation gate definitions (C-model / emu / pre-tapeout) v0",
                "Decision: QoS RM HWv1 scope sign-off with HW datapath DRI",
                "Open issues: access to models, lab, repos",
                "Actions: cadence with Shafi, Tippanna, Rupa, Prasun",
                "Non-goals: full C40-class HW digest in Cx",
            ],
        ),
        (
            "Execution mesh (hook — detail round 2)",
            [
                "Align task intake with SDK/ASIC milestones and SONiC/FBOSS release cadence",
                "Prasun Sinha — program touchpoint for sprint planning",
                "Prabu brainstorm — not Thu center unless asked",
            ],
        ),
        (
            "Asks for Gururaj — delta beyond A3 slide 3",
            [
                "Thu package: A3 hook + optional B6 walk; Cx 2-pager ~2 weeks — OK?",
                "Cx scope v0: validation gates + QoS RM HWv1 — who must be in the room?",
                "Step in if validation-gate consensus stalls beyond normal peer DRI friction.",
            ],
        ),
        (
            "What Thu is not",
            [
                "Not finished C40 or full HW-doc digest",
                "Not claiming SDK/SAI program ownership day one",
                "Not AI tooling / token policy (separate thread)",
                "Not a 50-page substitute — B6 is walkable backup",
            ],
        ),
    ]
    for title, bullets in more:
        deck.add_content(title, bullets)

    return deck.save()


def main():
    ref = ensure_style_reference()
    print(f"Style reference: {ref}")
    a3 = build_a3()
    b6 = build_b6()
    print(f"Wrote {a3} ({len(Presentation(a3).slides)} slides, company chrome)")
    print(f"Wrote {b6} ({len(Presentation(b6).slides)} slides, company chrome)")


if __name__ == "__main__":
    main()
