import os
import glob
import shutil
import pandas as pd
import subprocess
import time
import ast



def convert_idat_to_plink(idat_dir, 
                          out_dir,
                          iaap = 'utils/iaap-cli-linux-x64-1.1.0-sha.80d7e5b3d9c1fdfc2e99b472a90652fd3848bbc7/iaap-cli/iaap-cli',
                          bpm = 'utils/NeuroBooster_20042459_A2.bpm',
                          egt = 'utils/NBSCluster_file_n1393_011921.egt'):
  
    os.system(f'chmod 777 {iaap}')
    
    start = time.time()
    cmd = f'{iaap} gencall {bpm} {egt} {out_dir} -f {idat_dir} -p'
    print(cmd)
    
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in iter(process.stdout.readline, ''):
        print(line.strip())
    process.wait()
    
    print(f'finished {idat_dir} in {round(time.time() - start, 2)} seconds')
    print('='*100,'\n\n\n')


def copy_map_file(subject, out_dir, map_file):
    ped = os.path.join(out_dir, f'{subject}.ped')
    map = os.path.join(out_dir, f'{subject}.map')
    if os.path.isfile(map):
        print(f'{map} already exists')
        return
    if os.path.isfile(ped):
        shutil.copyfile(src=map_file, dst=map)
        print(f'cretaed {map}')
    else:
        print(f'{ped} does not exist')
        print(f'{map} creation cancelled')


def ped_to_bed(prefix, plink='utils/plink'):
    subprocess.run(['chmod', '777', plink])
    cmd = f'{plink} --file {prefix} --make-bed --out {prefix}'
    print(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    for stdout_line in iter(process.stdout.readline, ""):
        print(stdout_line, end="")  # Print each line of stdout in real time

    for stderr_line in iter(process.stderr.readline, ""):
        print(stderr_line, end="")  # Print each line of stderr in real time

    process.stdout.close()
    process.stderr.close()
    return_code = process.wait()

    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


class NeuroBoosterManifest():
    def __init__(self, manifest, raw_data_root='mounted/lrrk2-clinical-trials/genotype/raw'):
        self.manifest = manifest
        self.raw_data_root = raw_data_root

        self.barcode_association_table = pd.read_csv(os.path.join(raw_data_root, manifest, 'barcodeAssociationTable.csv'))
        self.chip_id = self.barcode_association_table.ExternalChipId[0]
        self.subjects = list(self.barcode_association_table.ExternalChipId.astype(str) + '_' + self.barcode_association_table.RowColIdx)

        self.idat_dir = os.path.join(raw_data_root, manifest, f'LibraryData_{self.manifest}_{self.chip_id}')

    def process_to_plink(self, out_dir='mounted/lrrk2-clinical-trials/genotype/plink/individual'):
        print(f'Processing manifest {self.manifest} to plink')
        convert_idat_to_plink(self.idat_dir, out_dir)
        for subject in self.subjects:
            copy_map_file(subject, out_dir=out_dir, map_file=f'{out_dir}/NeuroBooster_20042459_A2.map')
            subject_prefix = os.path.join(out_dir, subject)
            ped_to_bed(subject_prefix, plink='utils/plink_linux_x86_64_20231211/plink')
