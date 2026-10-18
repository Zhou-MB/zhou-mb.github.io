# Challenge-led research film

Duration: 165 seconds. 24 shots, each 6–7 seconds. Original off-white/navy/blue palette. English captions; no audio. Earlier edits and homepage remain unchanged.

## Source and interpretation

Based on the user-provided ICSOC_Symposium.pdf (Towards Time-Critical Scheduling in Distributed Digital Twin Systems), particularly Introduction pp. 1–2, Related Work p. 3, Research Questions p. 4, and Methodology/Progress p. 5.

- Temporal requirements concern service execution AND the timeliness/usefulness of digital states.
- Communication limits motivate selective state updates; task relevance is distinct from age alone.
- Heterogeneous workloads and resource constraints create differing scheduling objectives.
- Existing approaches provide foundations; the film does not claim all existing methods fail or that selective updating is new.
- Knowledge transfer for generative algorithm design is ongoing research. Candidate generation must be followed by constraint checks and evaluation.
- Agentic adaptive scheduling is explicitly marked as a future direction.
- The completed Pace study concerns energy-constrained blockchain support-service configuration, not demonstrated end-to-end digital twin improvements. The film includes an energy-constraint illustration but does not present it as a Pace experiment, benchmark, or integrated deployment.

The bus/flood scenario and graphics are explanatory illustrations, not an implemented application or experimental results. No numerical performance improvements are asserted.

## Causal structure

1. A route is computed in time.
2. The physical road changes, but the digital state stays old.
3. Sending every update creates contention at a limited communication channel.
4. Compare a remote old update against a task-relevant road change.
5. Updated information still competes for execution resources, communication, and energy.
6. Existing algorithm choices must respect different problem formulations.
7. A changed constraint can invalidate an otherwise suitable method.
8. Reusing scheduling knowledge motivates AI-assisted candidate design.
9. Test feasibility and evaluate candidates; iterate rather than treating generation as success.
10. Future adaptation closes a continuing physical–digital feedback loop.

## Re-render

Run research_vision_challenges_source.py with Python, Pillow, NumPy, and imageio-ffmpeg (or system FFmpeg). Use --preview for two storyboard sheets. The source exports MP4, VTT captions, and a poster. The video is H.264 1280×720 at 24 fps with fast-start metadata.
