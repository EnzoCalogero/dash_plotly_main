#!/bin/bash
cd /home/enzo/tech_view
mkdir benchmark
cd benchmark
cp /home/enzo/tech_view/var/log/enzo/server/*.* ./
gunzip *.log.*.gz
cat *.log* |grep benchmark> benchmark.enzo

cat benchmark.enzo |grep WARNING > benchmark_warn.enzo
cat benchmark.enzo |grep INFO > benchmark_info.enzo
cat benchmark.enzo |grep ERROR > benchmark_err.enzo

rm *.log.*
rm *.log
# Cleaning the files from sporiuus entries
sed -i 's/[^[:print:]]//;s/'\''//g;s/&apos;//g' benchmark_err.enzo
sed -i 's/[^[:print:]]//;s/'\''//g;s/&apos;//g' benchmark_warn.enzo


rm benchmark.enzo
# Tasks benchmark side

cp /home/enzo/tech_view/var/log/enzo/tasks/*.* ./.
rm system*.* 
gunzip *.log.*.gz
cat *.log* |grep benchmark> benchmark_tasks.enzo
rm *.log.*
rm *.log

cp /home/enzo/tech_view/var/log/enzo/tasks/system*.* ./.
gunzip *.log.*.gz
cat *.log* |grep benchmark> benchmark_tasks_sys.enzo
rm *.log.*
rm *.log


