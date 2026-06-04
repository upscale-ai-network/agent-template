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
DT100 = ROOT / "dt100"
sys.path.insert(0, str(ROOT / "scripts"))
from pptx_util import (  # noqa: E402
    assert_pptx_valid,
    fill_content_slide,
    fill_cover_slide,
    save_presentation,
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
        save_presentation(self.prs, self.path)
        assert_pptx_valid(self.path)
        print(f"OK: {self.path.name}")
        return self.path


def build_a3() -> Path:
    out = DT100 / "manager-arch-vision-a3.pptx"
    deck = StyledDeck(out, num_content_slides=4)

    notes_before = (
        "BEFORE SLIDE 1 (~20 s)\n"
        "Sponsor is you — name not on deck. I am Diwakar. Align: done and validated bar + "
        "my Dynamic Switch-Buffer Management (DBM) at CSB — ESUN analogy to DLB; not Rupa datapath arch). "
        "If slides 1-2 wrong, fix before B6. Flow: 1-2 → B6 → 3-4."
    )
    notes_cover = (
        "COVER (if asked)\n"
        "Arch vision review. Four slides + B6 backup. Confidential — Upscale AI."
    )
    notes_s1 = (
        "SLIDE 1 — do not read bullets\n"
        "His words: no one has looked at CSB + buffer carving — complex, needs datapath depth. "
        "He trusts I deliver CSB/carve by understanding datapath; Rupa owns datapath arch.\n\n"
        "DBM (your label, ESUN-world pair to DLB) = dynamic Switch-Buffer management at CSB: carve, queues, "
        "PFC, WRED/ECN/Pause via SDK/SAI. Rupa owns datapath arch; her pipeline slide in B6 is her seed.\n\n"
        "Story A on slide: done and validated · product · mgmt · AV · SDK/SAI · C-model→silicon. "
        "Today: scope only."
    )
    notes_s2 = (
        "SLIDE 2 — do not read bullets\n"
        "Program: SW done and validated — product, AV, SDK/SAI, path to silicon.\n\n"
        "Lane: QoS RM — QoSMAP, Queue, buffer carving. Peers: L2/L3 Shafi, ECMP Tippanna, SDK, Rupa.\n\n"
        "If OK → open B6 (his pipeline slide — Rupa seed; point CSB + carve)."
    )
    notes_s3 = (
        "SLIDE 3 — close after B6\n"
        "Outcome: Cx 2-pager ~2 weeks — decisions + validation gates, not 50-page dump.\n\n"
        "Instill closed-loop SW-HW validation (use-case → models → tape-out) — tactical verbal only; "
        "see dt100/README.md Private prep.\n\n"
        "Thin read usable upward. Fri edits. CSB/carve HWv1 inside Cx, not headline."
    )
    notes_s4 = (
        "SLIDE 4\n"
        "1-2 right? Who owns slices (B6 names).\n\n"
        "Optional spoken: who chairs done-and-validated program — he Sponsor or I drive?\n\n"
        "OCP: I coordinate datapath; he owns external. Format + escalate on gates."
    )
    notes_b6_in = "INTO B6 (~5 s): his pipeline map — CSB + carve; do not own Rupa framing."
    notes_b6_out = "AFTER B6 (~5 s): slides 3-4 — outcomes and Sponsor asks."

    deck.add_cover(
        "Arch vision",
        "Dynamic Switch-Buffer Management",
        "Executive review",
        "Confidential — Upscale AI",
        notes=notes_cover,
    )

    deck.add_content(
        "Dynamic Switch-Buffer Management",
        [
            "done and validated · product · management plane · AV",
            "SDK/SAI · C-model → emulation → silicon",
            "CSB buffer carving — not datapath architecture",
            "Align today",
        ],
        subtitle="Buffer carving at CSB",
        notes=notes_before + "\n\n" + notes_s1 + "\n\n" + notes_b6_in,
    )

    deck.add_content(
        "SW done and validated before tape-out",
        [
            "QoSMAP · Queue · buffer carving",
            "Layer 2 / Layer 3 · ECMP — peer DRIs",
            "Backup deck — logical pipeline walk",
        ],
        notes=notes_s2,
    )

    deck.add_content(
        "What you get",
        [
            "Cx two-pager · validation gates (~two weeks)",
            "done and validated · before tape-out",
            "AV · milestone decisions",
            "Friday · your edits",
        ],
        notes=notes_s3 + "\n\n" + notes_b6_out,
    )

    deck.add_content(
        "What I need from you",
        ["Scope aligned?", "Program chair?", "Backup deck · OCP"],
        notes=notes_s4,
    )

    return deck.save()


def build_b6() -> Path:
    out = DT100 / "manager-arch-vision-b6.pptx"
    # Walk order: transition → discipline → machine → owners → wedge → pipeline → defer → Cx → boundaries
    deck = StyledDeck(out, num_content_slides=11)

    deck.add_cover(
        "Arch vision plan (B6)",
        "Walk: machine → owners → pipeline → defer → Cx",
        "Open after Yes on A3",
        "Confidential — Upscale AI",
    )

    walk = [
        (
            "Define task — after A3 slides 1–2",
            [
                "Assumption: situation and task on A3 slides 1–2 are aligned.",
                "This walk: define the task — validation machine, owners, QoS wedge on pipeline — deferrals and Cx.",
                "After walk: A3 slides 3–4 — result and sponsorship (not repeated here).",
            ],
            "Beat 1 · ~1 min",
        ),
        (
            "Document discipline",
            [
                "Thu: A3 slides 1–2, then this deck (~6 beats).",
                "Next: Cx 2-pager — decisions, gates, open issues (~2 weeks).",
                "Not Thu: 50-page dump, full HW catalog.",
            ],
            "Beat 2 · thin",
        ),
        (
            "Validation framework (I draft v0; peers align)",
            [
                "Product / customer use cases",
                "Arch validation (AV) ↔ datapath arch",
                "Mgmt plane — SONiC / FBOSS lands",
                "SW validation: C-models → emulation / FPGA → silicon",
                "SDK + SAI done with explicit gates before tape-out",
                "I socialize v0 of done per gate for group review — not unilateral mandate.",
            ],
            "Beat 2 · ~3 min",
        ),
        (
            "Who owns what (don't read every row)",
            [
                "Sponsor (Gururaj): exec alignment — external narrative",
                "Validation program + QoS RM: Diwakar Tundlam",
                "L2/L3 / ACL: Shafi Mohammad · ECMP / AV: Tippanna Hongal",
                "SDK / SAI: SDK leads — consult, not my R",
                "Program mesh: Prasun Sinha · HW datapath / OCP: Rupa Budhia",
            ],
            "Beat 3 · ~2 min",
        ),
        (
            "My wedge — QoS / RM (HWv1)",
            [
                "VLAN-PRI, TOS/DSCP → queues → schedulers",
                "Buffer management and carving (resource manager)",
                "Port speed + queue/port policy coherence",
                "ESUN — align buffer/TM with standardization (OCP)",
                "HWv1 now: no MPLS EXP, no IPv6 priority mapping yet · HWv2: EXP + IPv6 pri",
            ],
            "Beat 4 · before pipeline",
        ),
    ]

    for title, bullets, sub in walk:
        deck.add_content(title, bullets, subtitle=sub)

    if PIPELINE_IMG.exists():
        deck.add_image_slide(
            "Your pipeline slide — my wedge (center of walk)",
            PIPELINE_IMG,
            "Beat 4 · QoSMAP + Queue/buffer carve (me) · Shafi (L2/ACL) · Tippanna (ECMP) · Rupa (parse/datapath)",
        )
    else:
        deck.add_content(
            "Your pipeline slide — my wedge",
            ["See assets/logical-pipeline-boss-slide.png"],
        )

    tail = [
        (
            "On the picture — blocks and validation tie-in",
            [
                "Ingress / Parser — align parse correctness with Rupa before OCP/BCM calls",
                "L2 — Shafi · Forward: ECMP (Tippanna), QoSMAP (me) · Egress Queue/carve (me)",
                "Each block: AV done + SW proof (C-model → emulation) before silicon — I draft cross-block gates",
            ],
            "Beat 4 · optional detail",
        ),
        (
            "Defer on Thu (do not merge)",
            [
                "Rupa SDK/SAI/datapath layout — related, different plan; weekly sync, not on Thu",
                "OCP ESUN: coordinate with Rupa before vendor calls; company position through Sponsor",
                "Prabu execution mesh / bs-2 — round 2 unless you redirect",
            ],
            "Beat 5 · ~1 min",
        ),
        (
            "~2 weeks — Cx 2-pager",
            [
                "Decision: validation gate definitions (C-model / emu / pre-tapeout) v0",
                "Decision: QoS RM HWv1 scope sign-off with HW datapath DRI",
                "Open: access to models, lab, repos · Actions: cadence with Shafi, Tippanna, Rupa, Prasun",
                "If asked who must be in the room — offer here (not on A3)",
            ],
            "Beat 6",
        ),
        (
            "What Thu is not",
            [
                "Not C40 / full HW digest · Not SDK program ownership day one",
                "Not AI/token policy · Not a second 50-pager — walkable backup only",
                "Whiteboard backup: assets/dt100-whiteboards.md (only if asked)",
            ],
            "Beat 5–6",
        ),
    ]
    for title, bullets, sub in tail:
        deck.add_content(title, bullets, subtitle=sub)

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
