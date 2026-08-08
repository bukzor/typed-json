---
managed-by: Skill(llm-subtask)
---

- [ ] Switch guards TypeGuard → TypeIs (PEP 742): TypeIs narrows both
  branches and requires the checked type be assignable to the argument
  type — the honest contract these guards already keep. Requires
  Python ≥3.13 or typing_extensions; weigh against the 3.12 floor.

## Later

We haven't (yet) decided where to place these in the task queue.
Please read and consider slotting them.

- (none)
