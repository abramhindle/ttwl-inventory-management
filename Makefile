#IDIR=/opt/hindle1/SteamLibrary/steamapps/compatdata/397540/pfx/drive_c/users/steamuser/My\ Documents/My\ Games/Borderlands\ 3/Saved/SaveGames/76561198082336040
IDIR=./my-save-files
SDIR="savcache"
INPUTS=$(wildcard ${IDIR}/[0-9]*.sav)
TTWLOUTPUTS=$(subst .sav,.csv,$(subst ${IDIR},ttwl,${INPUTS}))
TTWLANOUTPUTS=$(subst .sav,.csv,$(subst ${IDIR},ttwl-annoints,${INPUTS}))
TTWLPAOUTPUTS=$(subst .sav,.csv,$(subst ${IDIR},ttwl-parts,${INPUTS}))
TTWLSOUTPUTS=$(subst .sav,.csv,$(subst ${IDIR},save-summary,${INPUTS}))
# $(SDIR)/%.csv : $(IDIR)/%.sav
#	echo python3 myttwlrporet.py $< tee $@

DEFAULT: all

ttwl/%.csv: $(IDIR)/%.sav
	python3 myttwlreport.py $< > $@
ttwl-annoints/%.csv: $(IDIR)/%.sav
	python3 myttwlreport.py --annoints $< > $@
ttwl-parts/%.csv: $(IDIR)/%.sav
	python3 myttwlreport.py --parts $< > $@
save-summary/%.csv: $(IDIR)/%.sav
	python3 myshortttwlreport.py $< > $@

#ttwl/1.csv: $(IDIR)/1.sav
#	echo python3 myttwlreport.py "$(IDIR)"/1.sav

ttwl.csv: ${TTWLOUTPUTS}
	cat $^ | sort > $@
ttwl-annoints.csv: ${TTWLANOUTPUTS}
	cat $^ | sort > $@
ttwl-parts.csv: ${TTWLPAOUTPUTS}
	cat $^ | sort > $@

ttwl-everyitem.csv: ttwl.csv ttwl-everyitem.csv
	bash update-items.sh

saves.csv: ${TTWLSOUTPUTS}
	cat $^ | sort -n > $@

all: ttwl.csv ttwl-annoints.csv ttwl-parts.csv ttwl-everyitem.csv saves.csv
