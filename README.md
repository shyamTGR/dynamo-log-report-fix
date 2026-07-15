# Dynamo assessment — fixed Terminal-Bench 2 task: `log-report`

Repaired version of the broken `fix-task-broken.tar.gz` task. The task itself: parse `/app/access.log` (Apache-style) and write a JSON summary to `/app/report.json` with `total_requests`, `unique_ips`, and `top_path`.

## How to run

```bash
harbor run -p log-report -a oracle     # reference solution -> reward 1.0
harbor run -p log-report --agent nop   # no-op agent       -> reward 0.0
```

## Calibration results (Harbor 0.18.0)

| Check | Result |
|---|---|
| `oracle` | reward **1.0** (run twice — repeatable) |
| `nop` | reward **0.0** |
| Verifier outputs | `reward.txt` + `ctrf.json` written to `/logs/verifier/` |
| Artifact | `/app/report.json` = `{"total_requests": 6, "unique_ips": 3, "top_path": "/index.html"}` |
| Image cleanliness | `find / -name solve.sh -o -name test.sh -o -name solution_hint.py ...` inside the built image → no output; `/app` contains only `access.log` |

## Defects found and fixed

1. **`task.toml` — `artifacts` was a string and pointed at the wrong file.** `artifacts = "/app/out.json"` fails Harbor's `TaskConfig` schema (`Input should be a valid list`), so Harbor did not recognize the directory as a task at all (`ValueError: Either datasets or tasks must be provided`), and the declared artifact didn't match what the task produces. Fixed to `artifacts = ["/app/report.json"]` (top level, above the first `[section]`).
2. **`environment/Dockerfile` — base image was `python:latest`.** Floating `:latest` is never allowed and isn't reproducible. Fixed to the approved base pinned by digest: `public.ecr.aws/docker/library/python:3.13-slim-bookworm@sha256:01f42367…`.
3. **Leaked solution in the agent image.** `environment/solution_hint.py` (a copy of the reference solution) was `COPY`ed to `/app/solution_hint.py`, so any agent could pass by running it. Removed the `COPY` line and deleted the file.
4. **`tests/test.sh` — reward written to the wrong path.** It wrote `/app/reward.txt`; Harbor reads `/logs/verifier/reward.txt` (and `/app` is agent-writable, i.e. tamperable). Even a passing oracle recorded no reward. Fixed to write `1`/`0` to `/logs/verifier/reward.txt`.
5. **`tests/test.sh` — no CTRF report.** pytest ran without `--ctrf`, so `ctrf.json` was never produced. Fixed: `pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA`.
6. **`tests/test_outputs.py` — verifier checked existence, not the outcome.** It only asserted that `report.json` exists and is non-empty, so `echo garbage > /app/report.json` would score reward 1. Rewritten as six tests asserting the actual values (`total_requests == 6`, `unique_ips == 3`, `top_path == "/index.html"`), the exact key set, value types, and an input-integrity check (`/app/access.log` unchanged, verified by SHA-256) — 1:1 with the instruction's numbered success criteria, each docstring naming the criterion it verifies. Expected values are constants derived by hand from the fixed input log (tamper-independent — nothing is re-read from agent-writable ground truth).
7. **`instruction.md` — unverifiable prompt.** It never named the output path, format, keys, or any success criterion ("Save your findings so they can be reviewed"), so the verifier graded rules the agent was never told (the classic undisclosed-verifier-convention failure). Rewritten prompt-style (no title/headers) with exact absolute paths, the exact three keys and their semantics, six numbered success criteria consistent with the verifier (the "do not modify the input" constraint is now criterion 6 and is verified), a no-ties disclosure for `top_path`, and the required closing line "You have 120 seconds…" matching `[agent].timeout_sec`.
8. **`task.toml` — placeholder explanations (minor).** `verification_explanation = "Check the report file."` described nothing; `difficulty_explanation`/`solution_explanation` were one-liners. Filled in with accurate descriptions of the approach and of exactly what the verifier asserts. All template metadata fields kept; taxonomy labels (`category`/`subcategory`/`task_objective`/`artifact_type`) were already valid lowercase snake_case values and are unchanged.

**Four-way consistency after the fix:** instruction output path == `task.toml` `artifacts` == what the verifier asserts == what `solution/solve.sh` writes — all `/app/report.json`.
