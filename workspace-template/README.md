# Interview workspace layout

`prepare-DA-interview` reads and writes candidate files from an **interview
workspace that lives outside this repo**. Candidate data is personal and
confidential and must never be committed here. Later skills in this kit use
the same workspace, so the layout below leaves room for them.

This folder is the empty skeleton to copy. It is a template only: no real
candidate ever goes in it.

## Setting it up

Copy the skeleton to wherever you keep your own interview files:

```bash
cp -R workspace-template ~/qubika-da-interviews
```

The skills resolve the workspace as `$DA_INTERVIEWS_DIR` if set, else
`~/qubika-da-interviews/`. If you put it somewhere else, export the variable
in your shell profile:

```bash
export DA_INTERVIEWS_DIR="$HOME/path/to/your/workspace"
```

## Structure

```
<workspace>/
└── Candidates/
    └── <Candidate Name>/
        ├── <CV file>.pdf                      # input, optional
        ├── <recruiter screening notes>        # input, optional
        └── FirstnameLastname_InterviewPrep.md # prepare-DA-interview output
```

One folder per candidate, named for the candidate. The skill creates the
candidate folder itself when it does not exist yet, so `Candidates/` is the
only directory you need up front. Inputs can also be pasted straight into the
chat instead of dropped here; the folder matters when you want the prep to
persist.
