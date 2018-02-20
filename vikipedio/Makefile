EOLANG=eowiki-latest-langlinks.sql.gz
EOPAGE=eowiki-latest-page.sql.gz
EOFILES=$(EOLANG) $(EOPAGE)
EOWIKIDB=eowiki.db
MYSQLCONV=./mysql2sqlite
LANGLIST=langlist.txt

all: vikipedio
	python2 ./convert-to-js.py

$(EOLANG):
	wget https://dumps.wikimedia.org/eowiki/latest/eowiki-latest-langlinks.sql.gz

$(EOPAGE):
	wget https://dumps.wikimedia.org/eowiki/latest/eowiki-latest-page.sql.gz

$(MYSQLCONV):
	svn cat https://github.com/dumblob/mysql2sqlite.git/trunk/mysql2sqlite > $(MYSQLCONV)
	chmod +x $(MYSQLCONV)

$(EOWIKIDB): $(EOFILES) $(MYSQLCONV)
	gunzip -c $(EOPAGE) | $(MYSQLCONV) - | grep -v ",  UNIQUE (.page_namespace.,.page_title.)" | sqlite3 $(EOWIKIDB)
	gunzip -c $(EOLANG) | $(MYSQLCONV) - | grep -v ",  PRIMARY KEY (.ll_from.,.ll_lang.)" | sqlite3 $(EOWIKIDB)

$(LANGLIST): $(EOWIKIDB)
	sqlite3 $(EOWIKIDB) "SELECT ll_lang FROM langlinks GROUP BY ll_lang ORDER BY COUNT(ll_lang) DESC LIMIT 20;" > $(LANGLIST)

vikipedio-%.raw: $(LANGLIST) $(EOWIKIDB)
	sqlite3 $(EOWIKIDB) "SELECT REPLACE(p.page_title, '_', ' ') AS p_t, l.ll_title FROM page p, langlinks l WHERE p.page_id = l.ll_from AND l.ll_lang = '$*' AND l.ll_title NOT LIKE '%:%' AND REPLACE(p.page_title, '_', ' ') != l.ll_title AND ll_title != '';" > vikipedio-$*.raw
	
vikipedio-%.out: vikipedio-%.raw
	grep -v "[0-9]" $< > $@

vikipedio: $(LANGLIST)
	for l in $(shell cat ${LANGLIST}); do make vikipedio-$$l.out; done

clean:
	rm -f eowiki*.sql.gz $(MYSQLCONV) $(EOWIKIDB) $(MYSQLCONV) $(LANGLIST) vikipedio-*.raw vikipedio-*.out
