while read line; do
  echo $line | java -cp stanford-ner/stanford-ner.jar edu.stanford.nlp.process.PTBTokenizer >> temp.tok
  echo >> temp.tok
done < $1

perl -ne 'chomp; $_ =~ /^$/ ? print "\n" : print "$_\tO\n"' \
  temp.tok > $2

rm temp.tok
