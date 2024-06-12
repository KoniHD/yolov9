## Disclaimer

Currently (May 3rd, 2024) this works but as this is cutting edge technology it might not work in 6 months. \
It is a personal guidance including tips and tricks of how I got access and used the LRZ AI system.
This is by no means perfect and probably error prone so don't hold me responsible if anything goes wrong :smiley:.
In case of questions please refer to the official [documentation](https://doku.lrz.de/lrz-ai-systems-11484278.html) provided by the LRZ. \
Also the links of the documentation page of LRZ seem to change quite regularly so if one of these links doesn't work please google it yourself, I suspect the keywords given here to remain unchanged.

# Prerequisits

* Access to LRZ Linux Cluster &rarr; can only be granted by Master User of your institution
  (at TUM probably every chair has one Master User so just ask around :smiley: )
    * By getting access to the Linux Cluster you obtain a new "LRZ-Kennung" which you will have to use going further
    * **IMPORTANT** Access to Linux Cluster and its services already falls under [German export regulations](https://www.lrz.de/wir/regelwerk/exportkontrollverordnungen_en/) so you will have to add your citizenship to the account in question. And sign somehting
* Access to LRZ AI Systems &rarr; at the current state of writing this you need to request it yourself by submitting a request at [LRZ service desk](https://servicedesk.lrz.de/en/selfservice#). However, I was told this might change in the future such that the master user can give you access directly. So if you cannot request the access yourself anymore ask you master user.
* Nvidia NGC account to pull desired NCG container images
* *Optional* (but probably makes sense): access to AI Systems DSS (Data Science Storage)

### Access to LRZ AI Systems

Currently you need submit a reuqest at [LRZ service desk](https://servicedesk.lrz.de/en/selfservice#) for
access:
1. Login in with the "LRZ-Kennung" that already has Linux Cluster permission ( *Note:* It doesn't work with your regular old "TUM-Kennung" or whatever you have. Hence the need for Linux Cluster permissions.)
2. Click **create new incident**
3. Under **High performance computing** select **AI Systems**
4. Select something along the lines of **Access AI Systems**
5. Describe the usecase briefly so that they can approve your need of GPU resources (Don't worry if you need more resources later on I was given all possible graphics resources eventough I never asked for the best :grinning: )
6. Once you access is granted you can login to the LRZ AI node via `ssh <lrz-userid>@login.ai.lrz.de` which will later ask you for your LRZ password

*Optional* If you don't like the default shell you can switch that in the [IDM Portal](https://idmportal2.lrz.de) and select
a different shell (I'm using zsh :smiley:)

### Nvidia NGC Containers

In order to later pull the desired NGC container image you need a Nvidia account. To do this:
1. Visit [NGC Container](https://catalog.ngc.nvidia.com)
2. Create an account and sign in
3. On your account badge go to **Setup**
4. At the state of this instruction you need to **Generate Personal Key**
5. Copy the key value
6. On the LRZ AI system (inside your personal `$HOME` directory) create a `enroot` directory containing a `.credentials` file
7. Inside the `.credentials` file copy the following lines where `<KEY>` is substituted with the previously copied key
```
machine nvcr.io login $oauthtoken password <KEY>
machine authn.nvidia.com login $oauthtoken password <KEY>
```
**STILL WORKING**
&rarr; Now you are set up to import NGC containers using the `enroot` command, which however does not work on the login nodes!

### Access to AI Systems DSS

According to [Storage on LRZ Systems](https://doku.lrz.de/2-storage-on-the-lrz-ai-systems-10746646.html) you should use the DSS to store your dataset which offers quicker access than your standard `$HOME` directory on the AI System
since it uses SSD for storage. The Data Science Storage (DSS) provided by LRZ has a seperate [documentation page](https://doku.lrz.de/data-science-storage-10745685.html) which you should briefly checkout before going further. At least the [user documentation](https://doku.lrz.de/dss-documentation-for-users-11476038.html) is helpful to know. \
To get access you need to contact a so-called 'data curator', which likely (at most TUM chairs) is also the master user of your project or at least part of the it-helpdesk@\<yourchair>.tum.de as DSS access is also related to the LRZ project you are assigned to.
This is because you personally don't have permissions to create a directory in `/dss/dssfs04`. 

So the steps are:
1. Find the 'data curator' fitting to your of the LRZ Project you are part of
2. Request access and wait for a confirmation email from the LRZ
3. Klick the link received in the Email and accept the terms and conditions. &rarr; Now you have to wait a couple of hours until you get the access
4. Test your access by login in via `ssh <lrz-userid>@login.ai.lrz.de` and then `cd /dss/dssfs04/<your_dir_path>`. If you are able to create files here you are good to go for uploading your data and the ML model. 

# Working on the LRZ AI System

**Important** note that after `ssh` login you are on a *login node*. This means you can use the command line to execute commands mostly meant to set up your work for later, i.e., downloading a dataset. On this *login node* you cannot perform command involving `sudo` or download packages via `apt install`.

You can see that you are on the login node because your command line looks something like this:
```
<lrz-userid>@login-04 $ >
```

*Note* if you have access to the previously described DSS I'd recommend creating a symbolic link from your DSS storage to your `$HOME` directory for easier use. \
This can be done via
`ln -s /dss/dssfs04/<your_dir_path> <link_name>`

### Working with YOLOv9 on the LOCO dataset
<details><summary> <b>Infos on how to use the given scripts for automatically downloading data</b> </summary>

For eas of use, and because it is necessary to always download the data again when using Google's Colab, I wrote the `get_loco.sh` and the `transform_to_yolo_format.py` script which automatically download the LOCO dataset and transform it to fit YOLO standards. \
To use it perform the following command in the lcoation you want the dataset to be downloaded to.
```
./scripts/get_loco.sh
```
*Hint:* If you cloned the repo you will have to make the script executable first with `chmod +x ./scripts/get_loco.sh`

After the dataset is downloaded it is ready to be used by an object detection model using the 'MSCOCO' data anotation format. However, if needed it can be transformed using the `transform_to_yolo_format.py` (which btw can also be used if you just want to get rid of the subdirectory structure the LOCO dataset naturally comes with or if you only want to convert the anotation) \
For parameter explanation just use 
```
python3 ./scripts/transform_to_yolo_format.py --help
```
If you want to use it for further usage with the YOLOv9 model use these parameters
```
python3 ./scripts/transform_to_yolo_format.py -d ./<path_to_loco_dir> -c2y -cI
```

Both these scripts are already included in the Jupyter Notebook `train-yolov9.ipynb` which is meant for use with Google Colab. \
If you want to train the model on the LRZ Systems I'd recommend to execute both of these scripts once on a login node and then copy the resulting `./loco` directory into your DSS for training purposes later.

</details>

## Work with command line

**DID NOT WORK YET**

* uses slurm for job scheduling (Documentation can be found here: [SLURM Doc](https://slurm.schedmd.com/documentation.html)
  with the most important commands and options being here: [SLURM Commands](https://slurm.schedmd.com/pdfs/summary.pdf)
* You can do it manually or maybe easier define a `.sbatch` file where you specify what program to run. \
**REMEMBER** to be resourceful with this as the GPU resources are shared over the whole LRZ network between different projects!
* Needs to do here: choose fitting NGC container image & mount the program plus data needed for the container

## Work with website interface

*NOTE* Might be the easiest option for most tasks so refer to this please! :smiley:\
Also currently it is the only working way of accessing the LRZ computing resources.
1. Login to [LRZ AI](https://login.ai.lrz.de)
2. Go to **Interactive Apps**
3. Select **Jupyter Notebook** and chose the resources needed (they are specified very well here!!) and specify the time this notebook will be up. **Careful** after the time runs up the notebook plus data aparently will be shutdown (I don't know if you also loose your data too yet)
4. You can select between 2 possible default *enroot* container images to let your Jupyter Notebook run in: One uses Tensorflow the other uses PyTorch. \
*Maybe custom images can be used here too if previously downloaded*
5. Like above mount the program plus data that is needed for execution \
**DID NOT WORK FOR ME YET**
6. After that your request will be automatically queued in the to LRZ AI System and once it's the resources are free the website will automatically provide you with a link to a Jupyter Notebook.