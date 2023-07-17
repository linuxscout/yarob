# Convert I3rab examples records to json format
# The json has format:
# {
# phrase_unvocalized:{ 
#   phrase_vocalized:"",
# "inflection":""},
#   }
# refereces:
# https://unix.stackexchange.com/questions/654859/can-i-use-awk-to-distribute-parameters-inside-a-json-file
BEGIN {
    RS = ""
    FS = "\n"
    printf "SAMPLES = {"
}
{
    gsub(/"/,"\\\\&")

    phrase = $1
#    phrase_nm = phrase
    # remove numbers and symbols in begining and ending
    # remove tatweel every where
    gsub(/\xd9\x80/, "", phrase)
    # remove symbols every where
    gsub(/([=\+\*])+/, "", phrase)
    # clean phrase begingin and ending
    gsub(/^([0-9]|[-:\.;,_=\s ])+|([-:\.;,_\s ])+$/, "", phrase)

    phrase_nm = phrase
    # remove diacritics + tatweel
    gsub(/\xd9\x8b|\xd9\x8c|\xd9\x8d|\xd9\x8e|\xd9\x8f|\xd9\x90|\xd9\x91|\xd9\x92|\xd9\xb0/, "",phrase_nm)
    inflection  = $2
    for (i=3; i<=NF; i++) {
        inflection = inflection "\\n" $i
    }

    print  (NR>1 ? "," : "")
    printf  "\"%s\": {\n", phrase_nm
    printf "        \"phrase\": \"%s\",\n", phrase
    printf "        \"inflection\": \"%s\",\n",   inflection
    printf "        \"checked\": True,\n"
    printf "        \"reference\": \"%s\",\n", ref
    printf "        \"type\": \"\",\n"
    printf "        \"date\": \"%s\",\n", date
    printf "    }"
}
END {
    print "\n}"
}

