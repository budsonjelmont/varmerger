#!/bin/env bash

pyscript=/mnt/c/Users/judson.x.belmont/Documents/Code/varchemist/test/run/vcf_to_json.py
indir=/mnt/c/Users/judson.x.belmont/Documents/Code/varchemist/test/data/
outdir=/mnt/c/Users/judson.x.belmont/Documents/Code/varchemist/test/data/
genomicbuild=grch37 # Case-sensitive. Need to add aliases for 'GRCh37' support
indents=4
ntests=18

declare -A TEST # 1st dimension array. One per dataset.
declare -A TESTS # 2nd dimension array. Each key is of format [integer_id_of_1st_d_array],[array_key_from_ast_d_array]
i=1 # Test counter

# Call after each DATASET declaration to populate 2d-array
function populate_datasets(){
  for key in "${!TESTS[@]}"; do
    TESTS[$i,$key]=${TESTS[$key]}
  done
  ((i++))
}

# Build test array 
for j in $(seq 1 $ntests)
do
  vcfinfile=$indir/$infile/test_${j}.sort.vcf
  jsonoutfile=$outdir/$outfile/test_A$(printf "%03d\n" $j).json
  # Not in use--just create the files in the loop rather than creating array in separate step
  #TEST["INFILE"]=$vcfinfile
  #TEST["OUTFILE"]=$vcfoutfile
  #TEST["ASSEMBLY"]=$genomicbuild
  cmd="python3 $pyscript $vcfinfile $jsonoutfile --build $genomicbuild"
  echo $cmd
  $cmd
done

# Not in use--iterate through n-dimensional array and create each test 
#for k in $(seq 1 $ntests)
#do
#  cmd="python3 $pyscript ${TESTS[$k,"INFILE"]}  ${TESTS[$k,"OUTFILE"]} --build ${TESTS[$k,"ASSEMBLY"]}"
#  echo $cmd
#  $cmd
#done
