
To train this model, please make sure your training and validation data is saved into the folder structure needed for running flistCreator.py. The data we used
came from the Places2 dataset.

Once your images are in the correct file structure, run the following on the command line: python flistCreator.py

This model works with Tensorflow 1.X, and as such you will need to be running a Python version that supports this, so Python 3.7 or lower. We did this with a virtual
enviroment, but of course do this however you see fits.

Once you have successfully generated the flist files, refer to the READ ME of the Generative Inpainting model created by Jiahui Yu to train the model, or just type
the following on the command prompt: python train.py
