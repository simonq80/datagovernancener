To prepare data for BRAT annotation, ensure it is in .csv format, 1 column, 1 message per row, no column title.

Run ./prep_data.sh {input_file.csv}
This will output tok0.txt - tokN.txt, each containing 400 tokenized messages

INPUT:
```
"An update documentation needed of the characteristic selection screen with:
- Steward
- Data Usage (Complex Relationship)
- Synonym (Alternate view for a relationship.)"
TODO: What happens when we remove Acronyms as a type from the PDs? Will this view be gracefully degraded to a view with all assets? Will it be deleted?
This is part of the name. Don't pay any attention to them. It's a pure copy of data from presales instance.
"TODO: Add a metrics page for tasks. Take the metrics from ""Data Stewardship"" that apply."
"Hi <@U039FC8LD> / <@U02ACFJ4F> and <@U02ACDYEV> / <@U02ADABV4>  äóî can I have your feedback on the data/time format suggestions?
<https://docs.collibra.com/pages/viewpage.action?pageId=18556967>"
```

OUTPUT(Tokenized, one message per line):
```
An update documentation needed of the characteristic selection screen with : - Steward - Data Usage ( Complex Relationship ) - Synonym ( Alternate view for a relationship . )
TODO : What happens when we remove Acronyms as a type from the PDs ? Will this view be gracefully degraded to a view with all assets ? Will it be deleted ?
This is part of the name . Do n't pay any attention to them . It 's a pure copy of data from presales instance .
TODO : Add a metrics page for tasks . Take the metrics from `` Data Stewardship '' that apply .
Hi <@U039FC8LD> / <@U02ACFJ4F> and <@U02ACDYEV> / <@U02ADABV4> äóî can I have your feedback on the data/time format suggestions ? <https://docs.collibra.com/pages/viewpage.action?pageId=18556967>
```
