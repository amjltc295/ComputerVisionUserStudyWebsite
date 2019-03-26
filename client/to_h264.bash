ROOT_VIDEO_DIR="/tmp2/yaliangchang/Free_Form_Video_Inpainting_with_Gated_Convolution/comapre_videos_with_mask_20"
ROOT_OUTPUT_DIR="."
declare -a mask_types=("rand_curve" "object_like_middle")
declare -a percentages=("5" "15" "25" "35" "45" "55" "65")
for mask_type in "${mask_types[@]}"
do
    for percentage in "${percentages[@]}"
    do
        for file in $ROOT_VIDEO_DIR/$mask_type/$percentage/*
        do
            INPUT=$file
            OUTPUT=$ROOT_OUTPUT_DIR/$(basename "$INPUT")
            # echo "$INPUT $OUTPUT"
            ffmpeg -i "$INPUT" -c:v libx264 -crf 18 -preset slow -c:a copy "$OUTPUT"
        done
    done
done
