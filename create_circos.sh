#!/bin/bash
#  is not implemented yet
# the idea is to have a script that exsecutes eyerything nessecary to build circos plots
jupyter nbconvert --execute circos_plots.ipynb
circos -config ./circos/study_final/etc/circos.conf
circos circos/study_final/
circos circos/study_final/
