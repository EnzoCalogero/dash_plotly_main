copy on new folder...
Unzip all 
cat *.log* |grep benchmark> benchmark.enzo


cat benchmark.enzo |grep WARNING > benchmark_warn.enzo
cat benchmark.enzo |grep INFO > benchmark_info.enzo
cat benchmark.enzo |grep ERROR > benchmark_err.enzo

Create the mapping for the 3 sets.
 




