#/usr/bin/sh
# Build alyahmor package

default: all
# Clean build files
clean:
	
backup: 
	
#create all files 
all: 

# Publish to github
publish:
	git push origin main

md2rst:
	pandoc -s -r markdown -w rst README.md -o README.rst
md2html:
	pandoc -s -r markdown -w html README.md -o README.html

wheel:
	sudo python3 setup.py bdist_wheel
install:
	sudo python3 setup.py install
sdist:
	sudo python3 setup.py sdist
upload:
	echo "use twine upload dist/yarob-0.1-py2-none-any.whl"

doc:
	epydoc -v --config epydoc.conf

build_verb_inflect:OUTPUT=tests/output/verbs_conjug_const.py
build_verb_inflect:
	# build a const for verb conjugation inflection
	#Data file : data/verb.csv
	# print into stdout
	# saved into tests/output/verbs_conjug_const.py
	echo "# This Table is generated automaticly by yarob/tools/gen_verb_inflect.py" > $(OUTPUT)
	echo "# Based on yarob/data-source/verbs.csv" >> $(OUTPUT)
	cd tools; python3 gen_verb_inflect.py >> ../$(OUTPUT)
example_count:
	#
	awk 'BEGIN { FS="\n"; RS=""; OFS="\t"} {print $$1}END {}' data-source/examples  | wc -l

server:
	cd web; python3 yarob_flask.py
