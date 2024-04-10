Dan's explanation of the code.

"It's about text searching and the hint bit algorithms hypercard uses, which is more formally called "superimposed coding". It's really about indexing and compressing text which is useful on stacks with thousands of cards of text where you want fast search..."

The stack is currently stored as using ZODB, so you must have ZODB installed to try this sample. I plan to change the code to pickle or shelve the data instead.

The Import Stack menu option is intended for importing stacks of the format described in:
  Managing Gigabytes
  Compressing and Indexing Documents and Images
  Second Edition, 1999
  http://www.cs.mu.oz.au/mg/
  source at:
  http://www.cs.mu.oz.au/mg/mg-1.2.1.tar.gz

If you attempt to Import a ZODB stack it will corrupt the data.
