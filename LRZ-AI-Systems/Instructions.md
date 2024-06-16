# Disclaimer

Currently (June 16th, 2024) this works but as this is cutting edge technology it might not work in 6 months. \
It is a personal guidance including tips and tricks of how I got access and used the LRZ AI system.
This is by no means perfect and probably error prone so don't hold me responsible if anything goes wrong :smiley:.
In case of questions please refer to the official [documentation](https://doku.lrz.de/lrz-ai-systems-11484278.html) provided by the LRZ. \
Also the links of the documentation page of LRZ seem to change quite regularly so if one of these links doesn't work please google it yourself, I suspect the keywords given here to remain unchanged.

# Contents

1. [Prerequisits](#prerequisits)
    * [Access to LRZ AI Systems](#access-to-lrz-ai-systems)
    * [Nvidia NGC Containers](#nvidia-ngc-containers)
    * [Access to AI Systems DSS](#access-to-ai-systems-dss)
2. [Working on the LRZ AI System](#working-on-the-lrz-ai-system)
   * [Basics on working on the LRZ AI System](#basics-on-working-on-the-lrz-ai-system)
       * [Working with YOLOv9 on the LOCO dataset](#work-with-yolov9-on-the-loco-dataset) 
    * [Work with command line](#work-with-command-line)
    * [Working with website interface](#work-with-website-interface)
        * [Work with YOLOv9 on IWS](#work-with-yolov9-on-iws)


# Prerequisits

* Access to LRZ Linux Cluster &rarr; can only be granted by Master User of your institution
  (at TUM probably every chair has one Master User so just ask around :smiley: )
    * By getting access to the Linux Cluster you obtain a new "LRZ-Kennung" which you will have to use going further
    * **IMPORTANT** Access to Linux Cluster and its services already falls under [German export regulations](https://www.lrz.de/wir/regelwerk/exportkontrollverordnungen_en/) so you will have to add your citizenship to the account in question. And probably sign somehting.
* [Access to LRZ AI Systems](#access-to-lrz-ai-systems) &rarr; at the current state of writing this you need to request it yourself by submitting a request at [LRZ service desk](https://servicedesk.lrz.de/en/selfservice#). However, I was told this might change in the future such that the master user can give you access directly. So if you cannot request the access yourself anymore ask you master user.
* *Optional?* [Nvidia NGC](#nvidia-ngc-containers) account to pull desired NCG container images
* *Optional* (but probably makes sense): [Access to AI Systems DSS](#access-to-ai-systems-dss) (Data Science Storage)

## Access to LRZ AI Systems

Currently you need submit a reuqest at [LRZ service desk](https://servicedesk.lrz.de/en/selfservice#) for
access:
1. Login in with the "LRZ-Kennung" that already has Linux Cluster permission ( *Note:* It doesn't work with your regular old "TUM-Kennung" or whatever you have. Hence the need for Linux Cluster permissions.)
2. Click **create new incident**
3. Under **High performance computing** select **AI Systems**
4. Select something along the lines of **Access AI Systems**
5. Describe the usecase briefly so that they can approve your need of GPU resources (Don't worry if you need more resources later on I was given all possible graphics resources eventough I never asked for the best. :grinning: )
6. Once you access is granted you can login to the LRZ AI node via `ssh <lrz-userid>@login.ai.lrz.de` which will later ask you for your LRZ password

*Optional* If you don't like the default shell you can switch that in the [IDM Portal](https://idmportal2.lrz.de) and select
a different shell (I'm using zsh :smiley:)

## Nvidia NGC Containers

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
The usage is discribed later in [Working on the LRZ AI Systems](#working-on-the-lrz-ai-system)

## Access to AI Systems DSS

According to [Storage on LRZ Systems](https://doku.lrz.de/2-storage-on-the-lrz-ai-systems-10746646.html) you should use the DSS to store your dataset which offers quicker access than your standard `$HOME` directory on the AI System
since it uses SSD for storage. The Data Science Storage (DSS) provided by LRZ has a seperate [documentation page](https://doku.lrz.de/data-science-storage-10745685.html) which you should briefly checkout before going further. At least the [user documentation](https://doku.lrz.de/dss-documentation-for-users-11476038.html) is helpful to know. \
To get access you need to contact a so-called 'data curator', which likely (at most TUM chairs) is also the master user of your project. Or at least he/she is part of the `it-helpdesk@\<yourchair>.tum.de` as DSS access is also related to the LRZ project you are assigned to.
This is because you personally don't have permissions to create a directory in `/dss/dssfs04`. 

So the steps are:
1. Find the 'data curator' fitting to your of the LRZ Project you are part of
2. Request access and wait for a confirmation email from the LRZ
3. Klick the link received in the Email and accept the terms and conditions. &rarr; Now you have to wait a couple of hours until you get the access
4. Test your access by login in via `ssh <lrz-userid>@login.ai.lrz.de` and then `cd /dss/dssfs04/<your_dir_path>`. If you are able to create files here you are good to go for uploading your data and the ML model. (Creating files: `touch filename.txt`) 

# Working on the LRZ AI System

## Basics on working on the LRZ AI System

**Important** note that after `ssh` login you are on a *login node*. This means you can use the command line to execute commands mostly meant to set up your work for later, i.e., downloading a dataset. On this *login node* you cannot perform command involving `sudo` or download packages via `apt install`.

You can see that you are on the login node because your command line looks something like this:
```
<lrz-userid>@login-04 $ >
```
The actual work is then performed on different server nodes if you use the [command line method](#work-with-command-line).

*Note* if you have access to the previously described DSS I'd recommend creating a symbolic link from your DSS storage to your `$HOME` directory for easier use. \
This can be done via
```
ln -s /dss/dssfs04/<your_dir_path> <link_name>
```

*Hint:* In terms of ease of use I was only able to get the [Jupyter Notebook on IWS](#work-with-website-interface) to work. It probably is sufficient for most ML trainings and pretty close to the known Google Colab. Hence, I would recommend using it!

### Work with YOLOv9 on the LOCO dataset
<details><summary> <b>Infos on how to use the given scripts for automatically downloading data</b> </summary>

For ease of use, and because it is necessary to always download the data again when using Google's Colab, I wrote the `get_loco.sh` and the `transform_to_yolo_format.py` script which automatically download the LOCO dataset and transform it to fit YOLO standards.

These scripts also come in handy when preparing the data for execution on the LRZ AI System.
Firstly, I would recommend to
```
git clone https://github.com/KoniHD/yolov9.git
```
to have the code available and then perform the following data transformation if needed.


To download the dataset perform the following command in the lcoation you want the dataset to be downloaded to.
```
./yolov9/scripts/get_loco.sh
```
*Hint:* If you cloned the repo you will have to make the script executable first with 
```
chmod +x ./yolov9/scripts/get_loco.sh
```

After the dataset is downloaded it is ready to be used by an object detection model using the 'MSCOCO' data anotation format. However, if needed it can be transformed using the `transform_to_yolo_format.py` (which btw can also be used if you just want to **get rid of the subdirectory structure** the LOCO dataset naturally comes with or if you only want to **convert the anotation format**) \
For parameter explanation just use 
```
python3 ./yolov9/scripts/transform_to_yolo_format.py --help
```
If you want to use it for further usage with the YOLOv9 model use these parameters
```
python3 ./yolov9/scripts/transform_to_yolo_format.py -d ./<path_to_loco_dir> -c2y -cI
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
* Need to do here: choose fitting NGC container image & mount the program plus data needed for the container

## Work with website interface

*NOTE:* Might be the easiest option for most tasks so refer to this please! :smiley:\
Also currently it is the only working way of accessing the LRZ computing resources.
1. Make sure you are connected to the Munich Scientific Network connecting to a Munich University Wifi or by using [EduVPN](https://doku.lrz.de/vpn-10333177.html?showLanguage=en_GB)
2. Login to [LRZ AI](https://login.ai.lrz.de)
3. Go to **Interactive Apps**
4. Select **Jupyter Notebook** and chose the resources needed (they are specified very well here!!) and specify the time this notebook will be up. **Careful** after the time runs up the notebook plus data aparently will be shutdown (I don't know if you also loose your data too yet)
    * **Note:** Using the IWS you do not have direct access to a GPU but rather you have access to a [MIG slice](https://www.nvidia.com/en-us/technologies/multi-instance-gpu/). This means IWS is not intended for distributed computing on multiple graphics cards.
5. You can select between 2 possible default *enroot* container images to let your Jupyter Notebook run in: One uses Tensorflow the other uses PyTorch. \
*Maybe custom images can be used here too if previously downloaded. I have not tried that so it's on you to do so*
6. Like above mount the program plus data that is needed for execution \
**DID NOT WORK FOR ME YET**
7. After that your request will be automatically queued in the to LRZ AI System and once it's the resources are free the website will automatically provide you with a link to a Jupyter Notebook.

### Work with YOLOv9 on IWS
<details><summary> <b>Infos on how to use the given Jupyter Notebook on the LRZ AI System</b> </summary>

* To avoid mounting issues I recommend creating a Linux Sym link of your `/dss/dssfs04` directory into your `$HOME` directory as this is automatically mounted into your Notebook session. Discribed [here](#working-on-the-lrz-ai-system)
* Since the AI System is not intended for testing I would recommend cloning the git repo into your `/dss/dssfs04` and follow the steps done in [working with loco on IWS](#work-with-yolov9-on-the-loco-dataset). In the execution I would recommend only to perform `git pull`.
* I put together a Jupyter Notebook meant for execution on the LRZ System: `./yolov9/LRZ-AI-Systems/train-model.ipynb`. In this script the first two code cells are meant to be performed before every training execution in oder to 1. clone the latest changes you commited from *coding on your own* machine 2. install the necessary pip extensions mentioned in the [README.md](https://github.com/WongKinYiu/yolov9/blob/main/README.md/#installation).
* After executing the first two cells reload the kernel and then start the Notebook again beginning with the third cell!

</details>