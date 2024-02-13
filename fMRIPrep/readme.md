# fMRIPrep

#### Executing fMRIPrep on BIDS formatted data.

| File              | Description                                                                          | Usage                                                |
| ----------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------- |
| **setup.sh**      | Create initial fMRIPrep conda environment.                                           | `sh setup.sh`                                        |
| **single_sub.sh** | Run fMRIPrep locally on a single subject. Computationally intense. Do not recommend. | `sh single_sub.sh -d path/to/bids -s <subject name>` |
