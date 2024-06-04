# Neurobooster processing
Process neurobooster array files


## Getting Started

### Installation

Clone this repository, add it to your sys path, and import the modules. 

  ```
    git clone https://github.com/neuron23-ds/neurobooster-processing.git
  ```
  ```python
    sys.path.insert(1, 'neurobooster-processing/processing')
    from neurobooster import NeuroBoosterManifest
  ```

### How to use

1. Load manifest
   ```python
   manifest = NeuroBoosterManifest('MA00000', raw_data_root='path/to/genotype/raw')
   ```
2. Inspect
   ```python
   display(manifest.barcode_association_table)
   ```
3. Process to plink
   ```python
   manifest.process_to_plink(out_dir='path/to/genotype/plink/individual', plink='path/to/plink')
   ```

Also see example notebook [here](https://colab.research.google.com/drive/1jcY7O8HVs4RIIxwQ5YoMJiXEe7-gb_2d?usp=sharing).
