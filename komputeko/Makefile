KOMP=Komputeko-ENEO
PDF=$(KOMP).pdf
TXT=$(KOMP).txt
PDFTOTEXT=pdftotext

all: $(TXT)
	python2 ./convert-to-js.py

$(PDF):
	wget http://www.komputeko.net/Komputeko-ENEO.pdf
	
$(TXT): $(PDF)
	$(PDFTOTEXT) -layout -eol unix -nopgbrk $(PDF) $(TXT)

clean:
	rm -f $(PDF) $(TXT) komputeko-en.js
