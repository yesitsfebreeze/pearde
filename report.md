# The board that runs itself — where it stands

*2026-09-02*

Ninety-nine percent of the requested work is finished: seventy of seventy-one
items are done, and four more landed today. What is left is one finished piece
of work that cannot be filed yet, because another line of work has the same
file open and has not put it down. Nothing is wrong with either; they simply
cannot both write at once, and the one that finishes first will free the other
within the hour.

The interesting result today was not the work itself. Every finished item was
checked by a second reader before it was accepted, and that reader rejected
three of the four on the first pass — each time for the same underlying reason:
a test that had stopped being able to fail. All three were sent back and all
three came back better, so the checks now standing behind this work are ones
that have been shown going red as well as green.

## Planned

- **Scoring how healthy each file is, and naming the unhealthy ones up front**
  — so whoever picks up a piece of work is told which files they are about to
  touch are in poor shape, before they start rather than after. This is the
  highest-priority remaining item and it is ready to start; it is waiting only
  because it needs the same files the unfiled work below is holding.

## In work

- **Stopping background services from outliving the tests that started them**
  — finished, checked, and proven. It fixes a real hazard: a routine startup
  and a routine cleanup could each destroy what the other had just done. While
  proving it, it also found that the cleanup would crash outright the moment a
  neighbouring feature now being built went live, which would have switched the
  whole protection off silently. That is fixed too. It is written and verified
  but not yet filed, because filing it would mean either committing a
  colleague's half-finished work or splitting this work in half and breaking
  it. Neither is acceptable, so it waits.

## Undecided or failing

- **Nothing is waiting on you.** No question is open, and the standing
  instruction — that work the board finds for itself runs alongside the work
  you asked for — is still being followed.
- **Three sessions were running this same board at once today**, and one of
  them overwrote another's working notes before it was noticed. The notes were
  reconstructed and nothing was lost, but it is worth knowing that starting
  several of these at once on one project is not currently safe. Two of the
  three stopped themselves once they noticed.
- **One piece of work claims more than it can prove, and now says so.** A set
  of expert profiles is meant to be built from real, cited practitioners. The
  automatic check can confirm the citations are well-formed and internally
  consistent, but nothing in the project can tell a real citation from a
  convincing invention — the actual research sits in the notes alongside. Its
  description was corrected to say exactly that rather than imply a guarantee
  it does not have. Closing that gap properly would be a small piece of work of
  its own; it has not been started, deliberately, because the board is already
  doing more work it found for itself than work you asked for.
