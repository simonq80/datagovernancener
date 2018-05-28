## Datasets & Trained NER model removed for confidentiality reasons

## Datasets
Datasets contains sets of unlabelled data, labelled data and models trained from the labelled data

## Labelling
Tokenise.sh takes line seperated sentences, tokenises them and labels them all as 'O'
```
./tokenise.sh /path/to/data /path/to/output
```

## Training
Trains and saves model to ner-model.ser.gz
```
java -cp stanford-ner/stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -trainFile {tokenise output} -prop config.prop
```

## Testing and Cross-Validation
Methods for split testing and cross-validation are contained in NERTesting.py
To run 5 fold cross-validation:
```
python3 NERTesting.py
```
(Datasets/v3/tok0_2_annotated.tsv is a small labelled dataset to test on)

Test options and paths to datasets and NER config files can be set in test_config.cfg

### Sample Output
```
5 FOLD CROSS VALIDATION

TEST FILES:
  Datasets/v3/tok0_2_annotated.tsv

CONFIG FILES:
  config.prop

CONFIG : config.prop
Fold 1
  P:0.4615 R:0.2069 F1:0.2857
Fold 2
  P:0.4615 R:0.2 F1:0.2791
Fold 3
  P:0.5385 R:0.1522 F1:0.2373
Fold 4
  P:0.3684 R:0.1111 F1:0.1707
Fold 5
  P:0.74 R:0.1806 F1:0.268
Average
  P:0.46997999999999995 R:0.17016 F1:0.24816000000000002

```

```
5 FOLD CROSS VALIDATION

TEST FILES:
  Datasets/v5/ner_data/ner-crf-training-data.tsv

CONFIG FILES:
  config.prop

CONFIG : config.prop
Fold 1
  P:0.4625 R:0.2387 F1:0.3149
Fold 2
  P:0.358 R:0.1559 F1:0.2172
Fold 3
  P:0.4524 R:0.2054 F1:0.2825
Fold 4
  P:0.4167 R:0.2557 F1:0.3169
Fold 5
  P:0.4773 R:0.3663 F1:0.4145
Average
  P:0.43338 R:0.2444 F1:0.3092
```

```
4 FOLD CROSS VALIDATION

TEST FILES:
  Datasets/v5/ner_data/ner-crf-training-data.tsv

CONFIG FILES:
  config.prop

CONFIG : config.prop
Fold 1
  P:0.4632 R:0.2222 F1:0.3003
Fold 2
  P:0.4386 R:0.2174 F1:0.2907
Fold 3
  P:0.4396 R:0.1688 F1:0.2439
Fold 4
  P:0.4651 R:0.3865 F1:0.4222
Average
  P:0.451625 R:0.24872500000000003 F1:0.31427499999999997
```

(This isn't working correctly I think)
```
BOOTSTRAP

TEST FILES:
  Datasets/v5/ner_data/ner-crf-training-data.tsv

CONFIG FILES:
  config.prop

CONFIG : config.prop
P:0.2254 R:0.0748 F1:0.1123
```

### Entity Statistics
P, R, F-Beta are given for each entity as well.
Example from 4-Fold CV:
```
Entity Statistics

Bus

Annotated: 196
Unique Word Count: 141
Average Length: 1.6752136752136753
Length Standard Deviation: 1.2664578763754841

Predicted: 36
Precision: 0.3611111111111111
Recall: 0.0663265306122449
F-1.0: 0.11206896551724138

Data

Annotated: 503
Unique Word Count: 217
Average Length: 1.7964285714285715
Length Standard Deviation: 1.4459258385588953

Predicted: 404
Precision: 0.6138613861386139
Recall: 0.49304174950298213
F-1.0: 0.5468577728776185

Dmtask

Annotated: 144
Unique Word Count: 93
Average Length: 1.170731707317073
Length Standard Deviation: 0.5053746428591886

Predicted: 61
Precision: 0.4918032786885246
Recall: 0.20833333333333334
F-1.0: 0.2926829268292683

Gov

Annotated: 182
Unique Word Count: 114
Average Length: 3.7916666666666665
Length Standard Deviation: 3.2207551736958977

Predicted: 19
Precision: 0.3684210526315789
Recall: 0.038461538461538464
F-1.0: 0.06965174129353234

Issue

Annotated: 311
Unique Word Count: 175
Average Length: 3.49438202247191
Length Standard Deviation: 2.356552402312613

Predicted: 54
Precision: 0.3888888888888889
Recall: 0.06752411575562701
F-1.0: 0.11506849315068494

Role

Annotated: 14
Unique Word Count: 9
Average Length: 1.5555555555555556
Length Standard Deviation: 0.8314794192830981

Predicted: 0
Precision: 1
Recall: 0.0
F-1.0: 0.0

Tech

Annotated: 236
Unique Word Count: 129
Average Length: 1.4936708860759493
Length Standard Deviation: 0.9727088330854748

Predicted: 123
Precision: 0.6422764227642277
Recall: 0.3347457627118644
F-1.0: 0.44011142061281333

User

Annotated: 153
Unique Word Count: 44
Average Length: 3.1875
Length Standard Deviation: 1.8891824730995856

Predicted: 154
Precision: 0.8831168831168831
Recall: 0.8888888888888888
F-1.0: 0.8859934853420196

```

## Manual Testing
Test trained model on a labelled test dataset
```
java -cp stanford-ner/stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ner-model.ser.gz -testFile {labelled test data}
```

## Relation extractor
Run the relation extractor with
```
java -cp stanford-corenlp/stanford-corenlp-3.9.1.jar edu.stanford.nlp.ie.machinereading.MachineReading --arguments relationship-extractor.properties
```
The properties file is set to run 5 fold cross validation on Dataset/v3/tok0_2_relations.corp
