import argparse
import pathlib
import shutil
import tarfile
import glob
import os

from sklearn.model_selection import train_test_split

class DataOrganizer:

    def create_paths(self, paths):
        for path in paths:
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    def copy_files(self, input_dir, files, output_dir):
        for file in files:
            fpath = input_dir + file
            shutil.copy(fpath, output_dir)

    def archive(self, dir):
        output_file = dir + '.tar.gz'
        print(f'    Output archive at {output_file}')
        with tarfile.open(output_file, 'w:gz') as t:
            t.add(dir)

    def Module4(self, input_dir, output_dir, dataset):
        input_images = input_dir+'/Images/data/'
        input_masks = input_dir +'/Masks/data/'
        for dset in dataset:
            dset_path = output_dir + '/' + dset
            images_train = dset_path +'/Train/Images/data/'
            masks_train = dset_path + '/Train/Masks/data/'
            images_test = dset_path + '/Test/Images/data/'
            masks_test = dset_path + '/Test/Masks/data/'

            self.create_paths([images_train, masks_train, images_test, masks_test])

            images_for_set = input_dir + '/Images/data/'+dset+"*.*"
            images_list = [os.path.basename(file) for file in glob.glob(images_for_set)]
            X_train, X_test = train_test_split(images_list)
            Y_train = ['mask_'+file for file in X_train]
            Y_test = ['mask_'+file for file in X_test]

            self.copy_files(input_images, X_train, images_train)
            self.copy_files(input_masks, Y_train, masks_train)
            self.copy_files(input_images, X_test, images_test)
            self.copy_files(input_masks, Y_test, masks_test)

        self.archive(output_dir)


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required = True,
                    help = 'Input directory where consolidated data is present')
parser.add_argument('-m', '--module', required = True, type = int,
                    help = 'Module # for which the data needs organized')
parser.add_argument('-s', '--dataset', required = True, nargs='+')

args = parser.parse_args()

organizer = DataOrganizer()

if args.module == 4:
    print("# Creating data for Module 4")
    organizer.Module4(args.input, 'Data_Module_4', args.dataset)
