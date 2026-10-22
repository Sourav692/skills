---
name: career-docs
description: "Write, tailor, and polish job-search documents: resumes, academic CVs, executive resumes, cover letters, and job application form answers. Covers tailoring to a job posting, ATS optimization and keyword match, rewriting weak bullets into metric-driven achievements, resume layout and formatting, building individual sections, C-suite/VP resumes, academic CVs with publications and grants, cover letters, and copy-pasteable answers for Greenhouse/Lever/Ashby/Workday fields. Use whenever the user mentions a resume, CV, cover letter, job application, ATS, 'tailor my resume', 'improve my bullets', 'not getting interviews', 'what do I write here', or pastes a job description alongside their experience."
---

# Career docs

One skill for every job-search document. Pick the mode, read its reference file, follow it.
Read only the reference the request needs; read a second one only when the task spans two modes.

## Pick the mode

| The user wants to... | Mode | Read |
|---|---|---|
| Fit a resume to one job posting | Tailor | `references/tailor.md` |
| Pass ATS screening, check keyword match, find out why there are no callbacks | ATS | `references/ats.md` |
| Rewrite bullets into achievements with metrics | Bullets | `references/bullets.md` |
| Fix layout, fonts, spacing, a messy or unreadable resume | Format | `references/format.md` |
| Build or fix one section (summary, skills, experience, education) | Sections | `references/sections.md` |
| Write a C-suite, VP, or Director resume (15+ years, strategic leadership) | Executive | `references/executive.md` |
| Build an academic CV (faculty, postdoc, research; publications, grants, teaching) | Academic CV | `references/academic-cv.md` |
| Write a cover letter | Cover letter | `references/cover-letter.md` |
| Answer fields on an application form | Application form | `references/application-form.md` |

Common combinations:
- "Apply to this job" with a resume and job description: Tailor, then ATS check, then Cover letter if asked.
- "Make my resume stronger" with no target job: Bullets, then Format.
- Executive or academic candidates: use Executive or Academic CV in place of Sections and Format.

## Rules for every mode

- **Truth first.** Reword, reorder, and emphasize real experience. Never invent employers, titles, dates, degrees, metrics, or skills. If a number is missing, ask for it or mark it `[X]` for the user to fill.
- **Inputs.** Work from the user's actual CV and, when there is one, the actual job description. Ask for the missing one only when the mode needs it (Tailor, ATS, Cover letter, Application form).
- **Job description first.** When a posting is given, pull out its must-have requirements, keywords, and seniority signals before writing anything.
- **ATS-safe by default.** Standard section headings, no tables or text boxes for core content, no text in images, keywords written the way the posting writes them.
- **Copy-pasteable output.** Deliver text the user can paste directly: no commentary inside the document, and notes and assumptions listed after it.
