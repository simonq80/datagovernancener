python3 multiline_format.py $1 format.temp
java edu.stanford.nlp.process.PTBTokenizer -preserveLines -options normalizeParentheses=false,normalizeOtherBrackets=false format.temp tok.temp
python3 cleanup.py tok.temp tok
rm format.temp
rm tok.temp
