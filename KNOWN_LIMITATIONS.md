# Known Limitations

## Adaptive attack loop — goal drift
Early version of the adaptive loop only passed the previous failed attempt to the
attacker model, with no memory of the original attack goal. Over 3-4 turns, this
caused the attack to drift into unrelated topics (e.g. a system-prompt-leak attempt
drifted into asking about emotion-recognition testing by turn 4).

Fix: `mutate_prompt()` now receives the original goal alongside the last attempt,
on every turn. This reduced drift but did not eliminate it — across 3 test runs on
DIR-004, 2 stayed on-topic, 1 still drifted (asked the model to list hard drive files
instead of leaking the system prompt).

## Judge reliability
The LLM-as-judge occasionally returns a verdict that contradicts its own stated
reasoning (e.g. reasoning says "does not contain harmful elements" but verdict is
COMPLY). Found and fixed one confirmed false positive (DIR-006, password manager
advice misjudged as a harmful bypass technique) via a calibration example added to
the judge's system prompt. Similar contradictions still observed in ~2 of 10 total
scan runs, suggesting the judge model itself (same small local model used for
everything) may not be strong enough for fully reliable evaluation. A stronger or
dedicated judge model would likely improve this.