# sparse-finder
A python script to retrieve "sparse" records (or any records) from WMS.

## Requirements
Python `requests` module.

[OCLC Python Authentication Library](https://github.com/OCLC-Developer-Network/oclc-auth-python)

WSKEY for Metadata API

principleID and principleIDNS

your registryID

## Usage
Modify sparse-finder.py with your authentication information.

With a file containing one OCLC number per line (e.g. oclc_numbers.txt):

```
1108665268
1108669635
1108672386
1108673639
1108670448
1108673988
1108670391
1108671693
1108674507
...
```


```bash
python sparse-finder.py < oclc_numbers.txt
```

Output will go to stdout. To gather it in a file:

```bash
python sparse-finder.py < oclc_numbers.txt > output.txt
```

Concordia's output presently looks like this:

```

access token:  tk_cgvxvR7S0o7sP3SAUV9cF12C280yvzDeTRJd
expires_in:    1199
expires_at:    2019-10-03 16:19:12Z
type:          bearer
1108665268 .b30074587 MAIN What's in your wallet /
1108669635 .b35939242 MAIN INTRODUCTORY INORGANIC CHEMISTRY I-WET LABS (Coursepack).
1108672386 .b27525272 MAIN Systematic Harmonic Substitution /
1108673639 .b37226824 MAIN LABORATORY MANUAL - INTRODUCTORY BIOLOGY (Coursepack).
1108670448 .b31714547 MAIN Vanier Equipment -- Headphones: Sony ZX100.
1108673988 .b22483469 MAIN Chance meeting
...
```

## TODO
* Error handling!
* Gathering info from LBD and LHR (requires Colleciton Manager API)
