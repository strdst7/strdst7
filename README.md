<div align="center">

<img src="stardust-banner.svg" alt="Nur Amirah Mohd Kamil — AI Systems Engineer and Founder of MI4 Inc." width="840">

<br>

### I build AI systems that remain useful after the demo.

Governed agents · reliable RAG · containerized delivery · privacy-first creative tools

<br>

[![Portfolio](https://img.shields.io/badge/Portfolio-aimirah.com-E9C46A?style=for-the-badge&labelColor=0A0908)](https://www.aimirah.com)
[![MI4 Inc.](https://img.shields.io/badge/Founder_%26_CEO-MI4_Inc.-D9AE55?style=for-the-badge&labelColor=0A0908)](https://github.com/MI4-inc)
[![Open to collaboration](https://img.shields.io/badge/Status-Open_to_collaboration-A6C8FF?style=for-the-badge&labelColor=0A0908)](https://www.aimirah.com)

</div>

## Signal

I'm **Nur Amirah Mohd Kamil (Mia)**, an AI Systems Engineer and the Founder & CEO of **MI4 Inc.**, based in Kuala Lumpur, Malaysia. I work where applied AI meets systems thinking: designing agent architectures, governance layers, retrieval systems, and human-centered products that are stable, explainable, and genuinely useful.

My projects move between enterprise AI reliability and public-good technology, with one constant: intelligence should be engineered as a dependable system—not added as a decorative feature.

> *“Code is how stardust remembers it was once a star.”*

## Currently in orbit

- 🪞 Building **[Trueframe](https://strdst7.github.io/true-frame/)**, a private, on-device studio that makes AI imagery feel more photographic.
- 🛰️ Developing **[AI-OS](https://github.com/strdst7/ai-os)** and the **[AI-OS Framework](https://github.com/strdst7/ai-os-framework)** for measurable deployment stability and multi-agent governance.
- 🇲🇾 Exploring AI for public access through **[BantuRakyat-AI](https://github.com/strdst7/BantuRakyat-AI)** and simulation-led automation for Malaysian SMEs.

## Selected systems

| Project | Domain | What it does |
| --- | --- | --- |
| [**Trueframe**](https://github.com/strdst7/true-frame) · [Live](https://strdst7.github.io/true-frame/) | `CREATIVE AI` | Six browser-native tools for skin repair, upscaling, film grading, prompt design, and batch processing—with no uploads |
| [**AI-OS**](https://github.com/strdst7/ai-os) | `AI GOVERNANCE` | Introduces ADSI, a composite stability model for monitoring and governing production AI deployments |
| [**AI-OS Framework**](https://github.com/strdst7/ai-os-framework) | `MULTI-AGENT` | Converts operational telemetry into stability scores, risk tiers, anomaly signals, and governance decisions |
| [**CCAM for Malaysian SMEs**](https://github.com/strdst7/CCAM-for-Malaysian-SMEs) | `DIGITAL TWIN` | Validates automation workflows inside a deterministic simulation before they reach real operations |
| [**BantuRakyat-AI**](https://github.com/strdst7/BantuRakyat-AI) · [Live](https://bantu-rakyat-ai.vercel.app) | `AI FOR GOOD` | Helps Malaysians discover government assistance programs and understand their eligibility |
| [**ReadyTensor RAG Assistant**](https://github.com/strdst7/readytensor-rag-assistant) | `RAG` | A FastAPI, LangChain, and Streamlit assistant for context-aware publication discovery |

## Containers

Everything I ship leaves the notebook in an image — eight Dockerfiles in public repos, thirteen across all my repositories. Each one solves a packaging problem rather than copying a template.

| Repo | The problem it solves |
| --- | --- |
| [**ai-os**](https://github.com/strdst7/ai-os) | Two-stage Python build; the runtime layer carries installed packages and source only. Restart, recreate-on-same-volume and backup/restore run in CI — see the [lifecycle report](https://github.com/strdst7/ai-os/blob/main/docs/operational-readiness-005c.md) |
| [**Fieldwork**](https://github.com/strdst7/Fieldwork) | Node build → nginx runtime, with a `HEALTHCHECK` on `/healthz` that can actually fail a deploy. Debian base because Rollup's native parser breaks under musl |
| [**miva-studio**](https://github.com/strdst7/miva-studio) | CUDA 11.8 / cuDNN runtime for GPU inference, plus a slim preview image for hosts without a GPU |
| [**midnight-counter**](https://github.com/strdst7/midnight-counter) | Compose devnet with a deliberately pinned indexer and a distroless proof-server that can't be healthchecked from inside, so the wait moves to the host |
| [**CCAM for Malaysian SMEs**](https://github.com/strdst7/CCAM-for-Malaysian-SMEs) | `uv`-based Python build with a `.dockerignore` that keeps tests and helm charts out of the image |
| [**ReadyTensor RAG Assistant**](https://github.com/strdst7/readytensor-rag-assistant) | Streamlit-first image sized for a Render deploy |

Multi-stage builds by default · healthchecks that can fail a deploy · image tags pinned with the reason written next to them · container lifecycle tested instead of assumed.

## Constellation loadout

<div align="center">
<img src="constellation-loadout.svg" alt="AI specializations and technology stack" width="840">
</div>

### Core tools

`Python` · `TypeScript` · `JavaScript` · `FastAPI` · `React` · `LangChain` · `Streamlit` · `Docker` · `Docker Compose` · `GitHub Actions` · `Google Cloud`

### Systems focus

`Multi-agent architectures` · `RAG pipelines` · `AI governance` · `Digital twins` · `Containerization` · `Evaluation` · `Observability` · `Privacy-first applications`

## Engineering principles

- **Reliability is a product feature.** AI systems need measurable behavior, recovery paths, and operational guardrails.
- **Validate before reality pays the price.** Simulation and deterministic checks belong before deployment.
- **Privacy should be architectural.** When a task can run locally, user data should stay local.
- **Useful beats impressive.** The best system solves a real problem clearly and survives contact with its users.

## Field notes

I write up the traps, not the highlight reel — container failures included.

- [**dev.to/miii**](https://dev.to/miii) — build notes and what broke on the way
- [**aimirah.com**](https://www.aimirah.com) — the longer learning log

## Stellar telemetry

<div align="center">

<img src="stellar-progress.svg" alt="GitHub contribution and stellar progress chart" width="840">

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=strdst7&show_icons=true&theme=dark&hide_border=true&title_color=E9C46A&icon_color=E9C46A&text_color=f4f2dd&bg_color=0A0908" />
  <img alt="GitHub stats" src="https://github-readme-stats.vercel.app/api?username=strdst7&show_icons=true&theme=default&hide_border=true&title_color=22230F&icon_color=B0492C&text_color=22230F&bg_color=F5F4E4" />
</picture>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-streak-stats.herokuapp.com?user=strdst7&theme=dark&hide_border=true&stroke=0A0908&ring=E9C46A&fire=E9C46A&currStreakLabel=E9C46A&background=0A0908" />
  <img alt="GitHub streak" src="https://github-readme-streak-stats.herokuapp.com?user=strdst7&theme=default&hide_border=true&stroke=22230F&ring=B0492C&fire=B0492C&currStreakLabel=22230F&background=F5F4E4" />
</picture>

<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=strdst7&layout=compact&theme=dark&hide_border=true&title_color=E9C46A&text_color=f4f2dd&bg_color=0A0908" />
  <img alt="Top languages" src="https://github-readme-stats.vercel.app/api/top-langs/?username=strdst7&layout=compact&theme=default&hide_border=true&title_color=22230F&text_color=22230F&bg_color=F5F4E4" />
</picture>

</div>

## Open a channel

I'm open to conversations about **dependable AI systems**, **agent governance**, **applied RAG**, **container packaging**, **creative technology**, and **mission-driven products**.

<div align="center">

[![Website](https://img.shields.io/badge/visit-aimirah.com-E9C46A?style=for-the-badge&labelColor=0A0908&logo=safari&logoColor=E9C46A)](https://www.aimirah.com)
[![GitHub](https://img.shields.io/badge/follow-@strdst7-F0D48A?style=for-the-badge&labelColor=0A0908&logo=github&logoColor=F0D48A)](https://github.com/strdst7)
[![MI4 Inc.](https://img.shields.io/badge/company-MI4_Inc.-D9AE55?style=for-the-badge&labelColor=0A0908&logo=github&logoColor=D9AE55)](https://github.com/MI4-inc)

<br>

✦ &nbsp; *Building useful intelligence from the Orion arm.* &nbsp; ✦

</div>
