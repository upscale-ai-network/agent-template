#!/usr/bin/env python3
"""
Educational MLX demo for Apple Silicon (UMA + lazy eval).

Watch: Activity Monitor → Window → GPU History
  Flat line  = GPU idle (graph built but not executed)
  Spike      = mx.eval() materialized work on the GPU

Run: uv run python demo.py
Fast: uv run python demo.py --quick
"""

from __future__ import annotations

import argparse
import sys
import time


def pause(seconds: float, label: str | None = None) -> None:
    if seconds <= 0:
        return
    if label:
        print(label, flush=True)
    time.sleep(seconds)


def banner() -> None:
    print()
    print("=" * 72)
    print("  APPLE SILICON MLX DEMO — what to watch")
    print("=" * 72)
    print()
    print("  OPEN NOW: Activity Monitor → Window → GPU History")
    print()
    print("  On a CUDA machine you expect:")
    print("    tensor.cuda()  →  PCIe copy host → device  →  then compute")
    print()
    print("  On Apple Silicon (MLX + unified memory):")
    print("    • Same RAM for CPU and GPU — no copy step in your code")
    print("    • Building tensors is LAZY — cheap until you call mx.eval()")
    print("    • mx.eval() is the moment the GPU should wake up in the graph")
    print()
    print("  This demo runs in 4 acts (~2–3 min). Read each act aloud to the room.")
    print("=" * 72)
    print()


def act1_lazy_gpu(quick: bool) -> tuple[float, float]:
    import mlx.core as mx

    n = 12288 if not quick else 8192
    mx.set_default_device(mx.gpu)

    print("-" * 72)
    print(f"  ACT 1 — Build graph on GPU (lazy) · {n}×{n} tensors")
    print("-" * 72)
    print("  SAY: “We’re defining math on the GPU device — but MLX hasn’t run it yet.”")
    print("  LOOK: GPU History should stay mostly FLAT.")
    print()

    pause(5 if not quick else 0, "  (5s — confirm Activity Monitor is visible)")

    t0 = time.perf_counter()
    a = mx.random.uniform(shape=(n, n))
    b = mx.random.uniform(shape=(n, n))
    # Touch shapes only — still lazy
    _ = a.shape, b.shape
    build_s = time.perf_counter() - t0

    print(f"  Built a, b on {mx.default_device()} in {build_s:.3f}s (lazy — not the real work yet)")
    print("  LOOK: Still flat? Good — that’s the point of act 1.")
    print()

    pause(4 if not quick else 0)
    return build_s, float(n)


def act2_materialize_gpu(quick: bool, n: float) -> float:
    import mlx.core as mx

    n = int(n)
    mx.set_default_device(mx.gpu)
    a = mx.random.uniform(shape=(n, n))
    b = mx.random.uniform(shape=(n, n))

    print("-" * 72)
    print(f"  ACT 2 — Materialize on GPU · mx.eval(a @ b)  ← THE IMPORTANT MOMENT")
    print("-" * 72)
    print("  SAY: “This one line forces the GPU to actually compute.”")
    print("  LOOK: GPU History should SPIKE NOW — and stay busy for a second or two.")
    print()

    pause(3 if not quick else 0, "  (3s — eyes on GPU graph)")

    t0 = time.perf_counter()
    c = a @ b
    mx.eval(c)
    gpu_s = time.perf_counter() - t0

    print(f"  GPU matmul done in {gpu_s:.2f}s")
    print("  VALUE: No .cuda(), no memcpy — same memory pool, you only pick device + eval.")
    print()

    pause(5 if not quick else 0, "  (5s — let the room see the spike settle)")
    return gpu_s


def act3_cpu_contrast(quick: bool) -> float:
    import mlx.core as mx

    # Sized so wall clock is clearly slower than act 2 GPU (~1s at 12288²)
    n = 10240 if not quick else 8192
    mx.set_default_device(mx.cpu)

    print("-" * 72)
    print(f"  ACT 3 — Same API, different engine · CPU {n}×{n} matmul")
    print("-" * 72)
    print("  SAY: “Same code path — we only changed the default device to CPU.”")
    print("  LOOK: GPU graph may dip; CPU fans may spin — wall clock is the lesson.")
    print()

    pause(2 if not quick else 0)

    a = mx.random.uniform(shape=(n, n))
    b = mx.random.uniform(shape=(n, n))
    t0 = time.perf_counter()
    mx.eval(a @ b)
    cpu_s = time.perf_counter() - t0

    print(f"  CPU matmul done in {cpu_s:.2f}s")
    print("  VALUE: Apple ML is routing — which engine runs the op — not shipping bytes over PCIe.")
    print()

    pause(3 if not quick else 0)
    return cpu_s


def act4_summary(gpu_s: float, cpu_s: float, build_s: float, quick: bool) -> None:
    print("=" * 72)
    print("  ACT 4 — Takeaways (read this)")
    print("=" * 72)
    print()
    print("  1. LAZY  — Building tensors ≠ running them. Watch for flat GPU until mx.eval().")
    print("  2. UMA   — No host→device copy in code; CPU/GPU share physical RAM.")
    print("  3. ROUTE — mx.set_default_device(gpu|cpu) is engine selection, like picking NIC vs GPU")
    print("           in a cluster — different layer, same systems instinct.")
    print("  4. NEXT  — Core ML + Instruments: compiler may route subgraphs to ANE instead of GPU.")
    print()
    if not quick:
        print(f"  Timing recap: lazy build ~{build_s:.3f}s | GPU matmul ~{gpu_s:.2f}s | CPU matmul ~{cpu_s:.2f}s")
    print()
    print("  Discussion: Where would you put always-on VAD (ANE) vs LLM tokens (GPU)?")
    print("=" * 72)
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Educational Apple Silicon MLX demo")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Short run for testing (no pauses, smaller matrices)",
    )
    args = parser.parse_args()

    try:
        import mlx.core as mx  # noqa: F401
    except ImportError:
        print("MLX not installed. Run: uv sync", file=sys.stderr)
        return 1

    banner()
    pause(2 if not args.quick else 0)

    build_s, n = act1_lazy_gpu(args.quick)
    gpu_s = act2_materialize_gpu(args.quick, n)
    cpu_s = act3_cpu_contrast(args.quick)
    act4_summary(gpu_s, cpu_s, build_s, args.quick)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
