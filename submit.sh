#!/bin/bash

## Nombre del trabajo
#SBATCH --job-name=TestRLNPRandomPolicy
## Archivo de salida
#SBATCH --output=../ExpResults/salida-original.txt
### Partición (Cola de trabajo)
##SBATCH --partition=512x1024
## Solicitud de cpus
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
## Solicitud de memoria RAM en GB
#SBATCH --mem=32
#SBATCH --mail-user=econtreraslazcano@uc.cl
#SBATCH --mail-type=ALL

python scripts/run.py --num_steps_per_iter=8192 --vf_coef=0.1 --model=internal --ex_dir=../ExpResults --name=OriginalExp --actor_network_width=64 --critic_network_width=256 --actor_depth=1 --optimizer=adam --learning_rate=0.0003 --entropy_coef=0.03 --target_kl=0.005 --min_mean_distance=2.4 --max_mean_distance=3.1 --min_atomic_distance=2.4 --formulas=Au13 --canvas_size=13 --save_rollouts=eval --clip_ratio=0.25 --lam=1.0 --discount=1.0 --num_steps=10000000000 --eval_freq=50
