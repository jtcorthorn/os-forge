# Bounded automation

## Inputs
A recurring task requested by the owner and a real available executor.

## Work
Use the loop-design skill. Check accessible existing schedules for the same owner and purpose before creating one. Reuse an existing executor within its approval and record any inventory gaps. Define the trigger, authoritative input, item ID, permitted actions, owner, retry and cost limits, output destination, failure route and stop condition. Reconcile prior attempts and actual outcomes before retrying an external action.

## Outputs
Approved spec using ../../_templates/automation/AUTOMATION.md; activation receipt only after executor verification.

## Human boundary
Activate or expand only when authorized. Verify a real run and the intended readers' access to its report. Record no new events, failed collection and incomplete coverage as distinct outcomes.
