# !/bin/bash

echo
echo "Running default preprocess script for dmri."
echo

# set subject dir
subj_dir=$1

# set atlas dir
atlas_path=$2

# set preprocess dir
preprocess_dir=$subj_dir/preprocess

# check if preprocess dir exists and create it if not
if [ ! -d $preprocess_dir ]; then
    mkdir $preprocess_dir
fi

# step 1
dsi_studio --action=src --source=$subj_dir/dmri.nii.gz --bval=$subj_dir/bvals.txt --bvec=$subj_dir/bvecs.txt --output=$preprocess_dir/dmri.src.gz

# step 2
dsi_studio --action=rec --source=$preprocess_dir/dmri.src.gz --method=7 --param0=1.25 --record_odf=1 --output=$preprocess_dir/dmri.fib.gz

# step 3
dsi_studio --action=trk --source=$preprocess_dir/dmri.fib.gz --connectivity=$atlas_path --connectivity_threshold=0.0001 --output=no_file --thread_count=4 --seed_count=10000000

#set preprocess result dir
preprocess_result_dir=$subj_dir/preprocess_result

# check if preprocess result dir exists and create it if not
if [ ! -d $preprocess_result_dir ]; then
    mkdir $preprocess_result_dir
fi

# copy result files to preprocess result dir
cp $preprocess_dir/*.mat $preprocess_result_dir/connectivity_matrix.mat

# remove preprocess dir
# rm -rf $preprocess_dir

# print finish message
echo
echo "Preprocess script for dmri finished."
echo