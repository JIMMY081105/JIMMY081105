<div align="center">
  <img src="./assets/hero.svg" width="100%" alt="Ma Yixing (Jimmy) — Embodied AI, humanoid robotics and simulation-ready 3D scene generation">
</div>

<p align="center">
  <a href="https://github.com/JIMMY081105/Buildings-Generation"><img src="https://img.shields.io/badge/featured-Buildings--Generation-0d1117?style=flat-square&logo=github&logoColor=white" alt="Featured: Buildings-Generation"></a>
  <img src="https://img.shields.io/badge/focus-Embodied%20AI%20%C2%B7%20Humanoid%20Robotics-5fe0ff?style=flat-square&labelColor=0d1117" alt="Focus: Embodied AI and humanoid robotics">
  <a href="mailto:hfyym4@nottingham.edu.my"><img src="https://img.shields.io/badge/email-hfyym4%40nottingham.edu.my-ff5fd8?style=flat-square&labelColor=0d1117" alt="Email"></a>
  <a href="https://orcid.org/0009-0008-7246-7431"><img src="https://img.shields.io/badge/ORCID-0009--0008--7246--7431-A6CE39?style=flat-square&logo=orcid&logoColor=white&labelColor=0d1117" alt="ORCID"></a>
  <a href="https://scholar.google.com/citations?user=JTJBx_sAAAAJ&hl=en"><img src="https://img.shields.io/badge/Google%20Scholar-profile-4285F4?style=flat-square&logo=googlescholar&logoColor=white&labelColor=0d1117" alt="Google Scholar"></a>
</p>

## About

I'm **Ma Yixing (Jimmy)**, a Computer Science with AI student at the **University of Nottingham**.
I build **simulation-ready 3D environments for humanoid robots**: multi-storey buildings whose storeys,
stairs and colliders are checked to be walkable *before* a policy ever trains in them.

- **Research interests:** embodied AI, humanoid locomotion, procedural 3D scene generation, physics simulation
- **How I work:** every acceptance check ships with a negative control. If a gate cannot fail, it is not measuring anything.
- **Currently:** connecting generated buildings to humanoid motion training in ProtoMotions / PARC

## Featured research

### [Buildings-Generation](https://github.com/JIMMY081105/Buildings-Generation)

Turn a multi-storey building into one a simulated humanoid can actually walk through: find its storeys,
design and place a staircase that connects them, bake the result to a voxel cache, and run geometric
acceptance gates that are built to fail.

<p align="center">
  <img src="./assets/media/stair_ascent.gif" width="720" alt="A humanoid policy climbing a flight designed, placed and accepted by Buildings-Generation">
  <br>
  <sub>A humanoid policy climbing a flight this pipeline designed, placed, baked and accepted.
  Geometry from Buildings-Generation; policy trained separately in ProtoMotions / PARC.</sub>
</p>

<table>
  <tr>
    <td align="center" width="33%"><img src="./assets/media/stair_eyelevel_approach.jpg" alt="Eye-level approach to a generated staircase"><br><sub>eye-level approach</sub></td>
    <td align="center" width="33%"><img src="./assets/media/stair_l_shaped.jpg" alt="L-shaped staircase"><br><sub>L-shaped</sub></td>
    <td align="center" width="33%"><img src="./assets/media/stair_u_shaped.jpg" alt="U-shaped staircase"><br><sub>U-shaped</sub></td>
  </tr>
</table>

- **Any building type.** A house, a factory, a school and a warehouse differ in a YAML profile, not in the code path.
- **Gates that can fail.** Each check has a negative control. Applying the body radius to the whole
  reachability flood, not just to seed selection, took the same 50 buildings from 50/50 passing to 0/50.
- **One CLI.** `buildingsgen scan` finds storeys; `buildingsgen run` connects, bakes and accepts.

### [Humanoid-Training-Scene-Ready-Generation](https://github.com/JIMMY081105/Humanoid-Training-Scene-Ready-Generation)

An automation, benchmarking and quality-gate layer on top of [SceneSmith](https://github.com/nepfaff/scenesmith),
run on a SLURM HPC cluster. It adds per-room quality gates, gated scene assembly, a benchmark of Codex CLI as a
VLM/agent backend, and a memory-safe headless Blender renderer. Only my own layer is published; changes to
upstream files ship as reviewable diffs.

## Projects

| Project | What it is | Stack |
|---|---|---|
| [Buildings-Generation](https://github.com/JIMMY081105/Buildings-Generation) | Storey detection, staircase placement, voxel baking and acceptance gates for multi-storey buildings | Python · OpenUSD |
| [Humanoid-Training-Scene-Ready-Generation](https://github.com/JIMMY081105/Humanoid-Training-Scene-Ready-Generation) | Quality gates and HPC automation for SceneSmith scene generation | Python · SLURM · Blender |
| [Scientific-Machine-Learning-Peking-Module](https://github.com/JIMMY081105/Scientific-Machine-Learning-Peking-Module) | Peking University SciML module: numerical solving, optimisation, autodiff, physics-informed networks | Julia · Jupyter |
| [Intrusion-Detection-System-IDS-](https://github.com/JIMMY081105/Intrusion-Detection-System-IDS-) | Metaheuristic feature selection and hyper-parameter tuning for intrusion detection | Python |
| [Algorithm-comparisons-between-optimized-and-greedy-algorithms](https://github.com/JIMMY081105/Algorithm-comparisons-between-optimized-and-greedy-algorithms) | Smart waste-clearance routing: optimised vs greedy algorithms | C++ |
| [Car-Warehouse-Management-System-using-C-](https://github.com/JIMMY081105/Car-Warehouse-Management-System-using-C-) | Warehouse management system for a car enterprise | C++ |
| [ReadVault](https://github.com/JIMMY081105/ReadVault) | Offline-first reading hub: ebook reader, library and reading calendar as an installable PWA | React · TypeScript · Vite |
| [Tetris-using-Java](https://github.com/JIMMY081105/Tetris-using-Java-.) | Tetris in Java | Java |

<sub>Also: [Farmer-Buddy](https://github.com/JIMMY081105/Farmer-Buddy) (team mobile app, fork) ·
[Agriculture chatbot](https://github.com/JIMMY081105/Agriculture-chatbot-using-gemini-flash) ·
[Rice-type classification](https://github.com/JIMMY081105/Rice-type-classification) ·
[SceneSmith](https://github.com/JIMMY081105/Scenesmith) (fork of the ICML 2026 code release)</sub>

## Tech stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,cpp,c,java,ts,js,julia,bash&theme=dark" alt="Python, C++, C, Java, TypeScript, JavaScript, Julia, Bash"><br><br>
  <img src="https://skillicons.dev/icons?i=pytorch,blender,linux,git,githubactions,react,vite,tailwind&theme=dark" alt="PyTorch, Blender, Linux, Git, GitHub Actions, React, Vite, Tailwind CSS"><br><br>
  <img src="https://img.shields.io/badge/NVIDIA-Isaac%20Sim%20%C2%B7%20Isaac%20Gym-76B900?style=flat-square&logo=nvidia&logoColor=white" alt="NVIDIA Isaac Sim and Isaac Gym">
  <img src="https://img.shields.io/badge/OpenUSD-scene%20description-5fe0ff?style=flat-square&labelColor=0d1117" alt="OpenUSD">
  <img src="https://img.shields.io/badge/ProtoMotions%20%2F%20PARC-humanoid%20RL-ff5fd8?style=flat-square&labelColor=0d1117" alt="ProtoMotions and PARC">
  <img src="https://img.shields.io/badge/SLURM-HPC%20clusters-8b949e?style=flat-square&labelColor=0d1117" alt="SLURM">
</p>

## Live on GitHub

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/JIMMY081105/JIMMY081105/output/stats-dark.svg">
  <img src="https://raw.githubusercontent.com/JIMMY081105/JIMMY081105/output/stats-light.svg" width="100%" alt="GitHub stats: public repositories, stars, followers and languages">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/JIMMY081105/JIMMY081105/output/github-snake-dark.svg">
  <img src="https://raw.githubusercontent.com/JIMMY081105/JIMMY081105/output/github-snake.svg" width="100%" alt="Contribution graph being eaten by a snake">
</picture>

**Recently active**

<!-- LIVE:RECENT:START -->
- `2026-10-17` [**Buildings-Generation**](https://github.com/JIMMY081105/Buildings-Generation) — Generate, connect and accept multi-storey simulation-ready buildings of any type — geometric storey…
- `2026-09-14` [**Grand-Library**](https://github.com/JIMMY081105/Grand-Library)
- `2026-07-23` [**Scientific-Machine-Learning-Peking-Module**](https://github.com/JIMMY081105/Scientific-Machine-Learning-Peking-Module) — Julia-based scientific machine learning course materials from Peking University: lecture notes, notebooks…
- `2026-07-21` [**Sustainability-Theory-and-Practices**](https://github.com/JIMMY081105/Sustainability-Theory-and-Practices) — The module is about understanding complex sustainability problems and developing practical, evidence-based…
- `2026-07-15` [**Humanoid-Training-Scene-Ready-Generation**](https://github.com/JIMMY081105/Humanoid-Training-Scene-Ready-Generation)
<!-- LIVE:RECENT:END -->

<p align="center"><sub>Header is a hand-built animated SVG (<code>scripts/build_hero.py</code>).
Stats, the contribution snake and the recent list refresh daily via GitHub Actions.</sub></p>
