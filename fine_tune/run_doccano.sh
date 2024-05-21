#!/bin/bash

python doccano.py \
    --doccano_file data/aiStudioKE/aiStudioKE_doccano_ext.json \
    --task_type ext \
    --save_dir ./data/aiStudioKE \
    --negative_ratio 1 \
    --splits 0.9 0.1 0 \
    --schema_lang ch
