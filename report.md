# The board that runs itself — where it stands

*2026-09-03*

A hundred and one of the hundred and fourteen requested pieces of work are
finished — eighty-eight percent. Eight landed in the last hour, and they had all
been finished for a day. What had stopped them was one thing, and it is now
gone.

## The thing that was wrong

The project keeps its own planning material in a folder beside the code. A day
ago that folder was renamed — the leading dot taken off its name — and a
shortcut left behind under the old name so that anything still spelling it the
old way kept working.

The shortcut is what broke everything. One folder answering to two names meant
the tools counted it as two projects. Every piece of work got handed out twice,
so two people worked the same job in the same place and overwrote each other —
one of them found edits in its own history that it had not made. And every
attempt to file a finished piece of work failed, because in a working copy the
two names are genuinely two different folders, one of them empty, so anything
looking for a file by the second name found nothing there.

Five finished, independently re-checked pieces of work sat behind that. Nothing
was damaged: the tooling refused cleanly every time rather than writing anything
half-done. But it was a jam, and it was costing a day at a time.

## What was done about it

You asked for the folder to be a real folder under its dotted name, with
everything inside it and no shortcut anywhere. That is what it now is. The
shortcut is gone, the folder is real, and its full history came with it — this
was a rename inside a repository, not a copy.

Thirty-three working copies scattered underneath it had to be re-pointed at the
new location, which the standard upgrade command does not yet do. It was done by
hand this time, and the fact that the upgrade command cannot do it is now a
piece of work in its own right.

There is a written decision record for all of this, with a one-line check anyone
can re-run to confirm the folder is still a real folder and the shortcut has not
come back.

## What went in behind it

With one name resolving, the queue emptied. Eight pieces of work were filed:

- The **written material rewrite** finished two more of its sections — the
  cross-project reference pages and the loose reference files, fifteen files and
  around seventeen thousand words rewritten to say the same things in fewer.
- One command was **renamed from a noun to a verb**, along with its script, its
  documentation page and its published skill.
- The project's **largest source file was cut into ten**, each named for the one
  thing it is responsible for, with nothing changed from the outside.
- Two **self-checks that claimed to measure a copy of the project they were not
  actually looking at** now measure the right one.

Four of those five needed re-measuring against the project as it stood after the
others landed, and one needed a genuine judgement call: a check was insisting on
words that a different piece of work had deliberately deleted. That was resolved
in favour of the deletion, and the reasoning is written down where the check is.

## What is waiting on you

Two pieces of work are stopped and only a person can start them.

**Two numbers need re-deciding.** One section of the written-material rewrite is
finished and correct, but two of its own targets cannot be met: they ask for a
ten-percent reduction while the arithmetic underneath them enforces eleven and a
half. The measured floor — the point past which cutting starts deleting facts
the work itself promises to keep — is ten percent. Either the two targets move
to what was measured, or a large glossary is ruled part of the same budget. The
finished work is sitting in place waiting on the answer.

**One approval.** A piece of work about self-checks has been at thirty of its
thirty-one conditions for four attempts. One condition asks for a change that is
now forbidden by a rule added since, and it also pins a count that has moved from
sixty to seventy-six, which no amount of work can make true again. The exact
replacement wording is written out and needs approving, nothing more.

## Worth knowing

Seven other projects on this machine carry exactly the folder-name problem that
was just fixed here, and none of them has been touched. Whether they should be
is a question nobody has asked you yet. The upgrade command that would move them
needs the working-copy repair added to it first.

## What is moving now

Six pieces of work are being planned as this is written: four of them finish the
folder rename properly — putting the name in one place instead of eight, teaching
the upgrade command to do the move safely, settling where the note-taking vault
should sit, and bringing the prose in line — plus a skills consolidation and one
small safety fix in how a session rolls back a failed rebase.
