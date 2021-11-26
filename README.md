# Set of examples with `symupy`

Just create the conda environment from 'env.yml'

```bash
conda env create -f env.yml
```

and launch the python file.

```bash
# This will run a single link simulation with fixed capacity
python 1-bottleneck_by_steps.py
```

```bash
# This will run a manhattan grid simulation of mid scale
python 2-performance-bysteps-trajs.py
```

```bash
# This will run the demo presented at the seminar LICIT-ECO7 2021/11/09
python Seminar_ECO7_LICIT_2021_11_09/run.py --type [free|control]
```

For special configurations see indications on each example.
