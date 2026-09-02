---
workflow: <slug>
subject: <one line — the job this routes>
date: <YYYY-MM-DD>
---

# <slug> — <the job in a phrase>

## Use when

- <A job this fits, named the way a request arrives.>
- <The near-miss it does not fit, and the slug that does.>

## Steps

| # | atomic | why | on failure |
|---|--------|-----|------------|
| 1 | `<slug>` | <what this step buys the job> | `stop` |
| 2 | `<slug>` | <…> | `→ 1` |
