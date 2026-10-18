# Research vision — narrative revision

## Direction

Preserve the original palette: off-white #F7F9FC, navy #1F2A44, blue #4F7DF3, pale blue #DCE7FF, and warm accent #E8C8A8. Preserve the 90-second duration and English presentation.

The reference video's sampled frames show a concrete question (tomorrow's weather), an expanding computational problem, a bottleneck, an explanation of parallel work and coordination, and a return to the original question. The original research film introduces concepts in sequence but does not give them a single shared problem to resolve.

This revision follows one illustrative bus-route decision during heavy rain. The same route, junction, and warm-colored urgent task recur, so the viewer can connect the deadline problem to scheduling and coordination. This is an explanatory scenario, not a claim about a deployed system or measured results. No reference footage or audio is reused.

## Story beats

| Time | Beat | Purpose |
|---|---|---|
| 00–08 | A bus approaches a decision point while heavy rain threatens its route. | Introduce a concrete question and stakes. |
| 08–17 | Road, weather, and bus observations feed a digital twin. | Explain the twin through its inputs. |
| 17–25 | A simulation explores an alternative route. | Establish what the computation is for. |
| 25–34 | The answer crosses the decision deadline. | Reveal why correctness alone is insufficient. |
| 34–44 | Tasks queue across edge and cloud resources. | Explain the obstacle. |
| 44–54 | The urgent decision is assigned separately from background work. | Introduce time-critical scheduling. |
| 54–63 | Local agents exchange information. | Connect distributed coordination to the same task. |
| 63–73 | A connection slows and planning adapts. | Add a second challenge, rather than a list of features. |
| 73–82 | Propose → simulate → evaluate → refine. | Position AI-driven algorithm design as research. |
| 82–90 | Return to the original road; the bus follows the alternative route. | Resolve the opening question visually. |

## Deliverables

- `research_vision_story_90s.mp4`: 1280×720, 24 fps, H.264, 90 seconds, browser-friendly fast-start MP4. Silent, matching the original research video; English captions are burned in.
- `research_vision_story_source.py`: editable self-contained rendering source.
- `research_vision_story_90s.vtt`: English caption transcript with timings. Avoid displaying this track by default when burned-in captions are visible.
- `research_vision_storyboard.jpg`: overview of ten shots.
- `research_vision_preview.html`: standalone comparison player, not linked into the homepage.

The existing `research_vision_90s.mp4` and its source are preserved. The homepage is not changed by this revision.

## Re-render

Python 3 with Pillow, numpy, and imageio-ffmpeg (or FFmpeg on PATH):

```sh
python research_vision_story_source.py --preview
python research_vision_story_source.py
```

The source automatically uses Arial on macOS or DejaVu Sans on Linux. Output paths are relative to the source file, replacing the original script's environment-specific `/mnt/data` path.

## Further editorial opportunity

A recorded English voiceover could add emphasis and pacing like the reference's audio track. This version is intentionally caption-led and contains no generated or borrowed voice.
