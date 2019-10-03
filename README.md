# sparse-finder
A python script to retrieve "sparse" records (or any records) from WMS.

## Requirements
Python `requests` module.
[OCLC Python Authentication Library](https://github.com/OCLC-Developer-Network/oclc-auth-python)
WSKEY for Metadata API
pricipleID and principleIDNS
your registryID

## Usage
Modify sparse-finder.py with your authentication information.

With a file containing one OCLC number per line (e.g. oclc_numbers.txt):

```bash
python sparse-finder.py < oclc_numbers.txt
```

Output will go to stdout. To gather it in a file:

```bash
python sparse-finder.py < oclc_numbers.txt > output.txt
```

## TODO
* Error handling!
* Gathering info from LBD and LHR (requires Colleciton Manager API)
