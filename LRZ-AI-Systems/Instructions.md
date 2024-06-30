# Disclaimer

Currently (June 26th, 2024) this works but as this is cutting edge technology it might not work in 6 months. \
It is a personal guidance including tips and tricks of how I got access and used the LRZ AI System.
This is by no means perfect and probably error prone so don't hold me responsible if anything goes wrong :smiley:.
In case of questions please refer to the official [documentation](https://doku.lrz.de/lrz-ai-systems-11484278.html) provided by the LRZ or directly ask the [LRZ service desk](https://servicedesk.lrz.de/en/selfservice#). \
Also the links of the documentation page of LRZ seem to change quite regularly so if one of these links doesn't work please google it yourself, I suspect the keywords given here to remain unchanged.

# Contents

1. [Prerequisits](#prerequisits)
    * [Access to LRZ AI Systems](#access-to-lrz-ai-systems)
    * [Nvidia NGC Containers](#nvidia-ngc-containers)
        * [Pull and Customize NGC Container](#pull-and-customize-ngc-container-for-the-lrz-ai-system)
    * [Access to AI Systems DSS](#access-to-ai-systems-dss)
2. [Working on the LRZ AI System](#working-on-the-lrz-ai-system)
   * [Basics on working on the LRZ AI System](#basics-on-working-on-the-lrz-ai-system)
       * [Working with YOLOv9 on the LOCO dataset](#work-with-yolov9-on-the-loco-dataset) 
    * [Interactive command line execution](#work-with-command-line-for-interactive-job-execution)
    * [Batch Job execution](#work-with-batch-jobs)
    * [Working with website interface](#work-with-website-interface)
        * [Work with YOLOv9 on IWS](#work-with-yolov9-on-iws)


# Prerequisits

* **Access to LRZ Linux Cluster** &rarr; can only be granted by Master User of your institution
  (at TUM probably every chair has one Master User so just ask around :smiley: *Hint:* `it-helpdesk@\<yourchair>.tum.de` is probably a good start for this).
    * By getting access to the Linux Cluster you obtain a new "LRZ-Kennung"/`<lrz-userid>` (something like `go42tum`) from your respective Master User, which you will have to use going further.
    * Your account / "LRZ-Kennung" is also tied to a project. Like the "LRZ-Kennung" this project has a rather cryptic name (like `t7121`) and is also important for some of the following steps, as well as issues submited to the [LRZ service desk](https://servicedesk.lrz.de/en/selfservice#). You can find out your project name on the [IDM Portal](https://idmportal2.lrz.de).
    * **IMPORTANT** Access to Linux Cluster and its services already falls under [German export regulations](https://www.lrz.de/wir/regelwerk/exportkontrollverordnungen_en/) so you will have to add your citizenship to the account in question. And probably sign somehting. At least you will have to agree to these regulations the first time you access the [IDM Portal](https://idmportal2.lrz.de).
* [Access to LRZ AI Systems](#access-to-lrz-ai-systems) &rarr; at the current state of writing this you need to request it yourself by submitting a request at [LRZ service desk](https://servicedesk.lrz.de/en/selfservice#). However, I was told this might change in the future such that the master user can give you access directly. So if you cannot request the access yourself anymore ask you master user.
* *Optional* [Nvidia NGC](#nvidia-ngc-containers) account to pull desired NCG container images. This is usefull/necessary for batch jobs or command line jobs.
* *Optional* (but probably makes sense): [Access to AI Systems DSS](#access-to-ai-systems-dss) (Data Science Storage)

## Access to LRZ AI Systems

**HINT**: the official LRZ documentation for this step can be found [here](https://doku.lrz.de/3-access-and-getting-started-10746642.html).

Currently you need submit a reuqest at [LRZ service desk](https://servicedesk.lrz.de/en/selfservice#) for
access:
1. Login in with the "LRZ-Kennung" that already has Linux Cluster permission. *Note:* It doesn't work with your regular old "TUM-Kennung" or whatever you have. Hence the need for Linux Cluster permissions.
2. Click **create new incident**.
3. Under **High performance computing** select **AI Systems**.
4. Select something along the lines of **Access AI Systems**.
5. Describe the usecase briefly so that they can approve your need of GPU resources. (Don't worry if you need more resources later on I was given all possible graphics resources eventough I never asked for the best. :grinning:.)
6. Once you access is granted you are free login to the LRZ AI node via `ssh <lrz-userid>@login.ai.lrz.de` and jump to section [Working on the LRZ AI Systems](#working-on-the-lrz-ai-system).

*Optional:* If you don't like the default shell you can switch that in the [IDM Portal](https://idmportal2.lrz.de) and select
a different shell (I'm using zsh :smiley:).

## Nvidia NGC Containers

**DISCLAIMER** The LRZ AI System provides a default NGC Container image for the PyTorch and Tensorflow framework on the [Website Interface](#work-with-website-interface) which are quite up-to-date. So if there is no need for [batch jobs](#work-with-batch-jobs), [command line execution](#work-with-command-line-for-interactive-job-execution) or different NGC images on the [Website Interface](#work-with-website-interface) this section of the [Prerequisits](#prerequisits) can be skiped (I strongly recommend to skip if you can as it is quite a complicated process).

**HINT**: the official LRZ documentation for this step can be found [here](https://doku.lrz.de/5-using-nvidia-ngc-containers-on-the-lrz-ai-systems-10746648.html).

Also NGC container are Docker images and enroot is based on Docker as well, in case of resulting errors you might also want to consider a Docker problem (but then you messed up bad).

Finally, in order to later pull the desired NGC container image you need a Nvidia account. To do this:
1. Visit [NGC Container](https://catalog.ngc.nvidia.com).
2. Create an account and sign in.
3. On your account badge go to **Setup**.
4. At the state of this instruction you need to **Generate Personal Key**.
    * *Note* the official LRZ documentation uses **Generate API Key** for this step. However, the Nvidia NGC page recommends the **Personal Keys** if you just want to pull container images. Additionally, you can deactivate or change **Personal Keys** while **API Keys**, once generated, cannot be changed or deleted which might be a securtiy risk (at least I think but I'm not an expert :grin:). For the following options both options work fine though.
5. Copy the key value.
6. On the LRZ AI system (inside your personal `$HOME` directory) create a `enroot` directory containing a `.credentials` file.
7. Inside the `.credentials` file copy the following lines where `<KEY>` is substituted with the previously copied key.
```
machine nvcr.io login $oauthtoken password <KEY>
machine authn.nvidia.com login $oauthtoken password <KEY>
```
### Pull and Customize NGC Container for the LRZ AI System

**HINT**: the official LRZ documentation closest to this step can be found [here](https://doku.lrz.de/9-creating-and-reusing-a-custom-enroot-container-image-10746637.html).

After you set up your **Personal Key** you can now perfomr `enroot import` to get the desired NGC container from the [NGC Container Catalog](https://catalog.ngc.nvidia.com). For this to work you need to:
1. Change from the login node described in the [basics part](#basics-on-working-on-the-lrz-ai-system) to a gpu node because the `enroot` command does not work on login nodes. To do this choose the fitting GPU you intend to use later from the available [resources](https://doku.lrz.de/1-general-description-and-resources-10746641.html). Then perform the following, where `<slurm_partition_name>` refers to the partition picked from the [resources](https://doku.lrz.de/1-general-description-and-resources-10746641.html) (e.g. `lrz-v100x2`). This allocates a gpu instance for 30min in order to set up our NGC container image.
```
salloc --partition=<slurm_partition_name> -N 1 --time=00:30:00 --gres=gpu:1
```
2. After this your job is queued. For a successful queueing you get a job ID. Once you get another confimation, that the job allocation worked you can perform the following to access the gpu node:
```
srun --pty bash
```
3. Now your terminal should look something like this:
```
<lrz-userid>@gpu-003:~$
```
4. On this gpu instance now you can now use `enroot`. For the import you now need the container tag found in the [NGC Container Catalog](https://catalog.ngc.nvidia.com). (e.g. `nvcr.io/nvidia/pytorch:24.03-py3`). The import command relies on a correctly set up **Personal Key** for authentication and is:
```
enroot import docker://<container_tag>
```
5. The container image then is imported to your `$HOME` directory which you can access from a login node. **IMPORTANT** If you want to use a base image you can stop here! \
Continuing: Use another terminal via `ssh` to check and find out the image name. To create the `enroot` container now you need the image file name and execute:
```
enroot create --name MyContainerName <image-file-name>.sqsh
```
6. Now the container is created and needs to be started as `root` in order to download additional packages. This is done with:
```
enroot start --root MyContainerName
```
7. If the terminal now say the following you're on the right track:
```
root@gpu-003:/#
```
8. Now in the container download the desired packeges
9. In order to save and reuse the set up container now there is one last step to perform:
```
exit
enroot export --output <desired_image_name>.sqsh MyContainerName
```

&rarr; By default this newly prepared container image is in your `$HOME` directory, accessible on the login node. It can now be used by its path (find out the path using `pwd` command) for a [batch execution](), [interactive command line execution](#work-with-command-line-for-interactive-job-execution) or even on the [Website Interface](#work-with-website-interface).

## Access to AI Systems DSS

According to Storage on LRZ AI Systems (official LRZ [documentation](https://doku.lrz.de/2-storage-on-the-lrz-ai-systems-10746646.html)) you should use the DSS to store your dataset which offers quicker access than your standard `$HOME` directory on the login nodes since it uses SSD for storage. The Data Science Storage (DSS) provided by LRZ has a seperate [documentation page](https://doku.lrz.de/data-science-storage-10745685.html) which you should briefly checkout before going further. At least the [user documentation](https://doku.lrz.de/dss-documentation-for-users-11476038.html) is helpful to know. \
To get access you need to contact a so-called 'data curator', which likely (at most TUM chairs) is also the master user of your project. Or at least he/she is part of the `it-helpdesk@\<yourchair>.tum.de` as DSS access is also related to the LRZ project you are assigned to.
This is because you personally don't have permissions to create a directory in `/dss/dssfs04`. 

So the steps are:
1. Find the 'data curator' responsibe for the LRZ Project you are part of.
2. Request access and wait for a confirmation email from the LRZ.
3. Klick the link received in the Email and accept the terms and conditions. &rarr; Now you have to wait a couple of hours until you get the access.
4. Test your access by login in via `ssh <lrz-userid>@login.ai.lrz.de` and then `cd /dss/dssfs04/<your_dir_path>`. If you are able to create files here you are good to go for uploading your data and the ML model. (Creating files: `touch filename.txt`).

*Nice-to-know:* Somewhere in `<your_dir_path>` you should be able to find your project name as mentioned in the [Prerequisits](#prerequisits).

# Working on the LRZ AI System

## Basics on working on the LRZ AI System

In order to use the LRZ AI Systems make sure you are connected to the Munich Scientific Network. This means you are either connected to a Munich University Wifi or by use [EduVPN](https://doku.lrz.de/vpn-10333177.html?showLanguage=en_GB). Only then can you `ssh` into the system or access [login.ai.lrz.de](https://login.ai.lrz.de) for the [Website Interface](#work-with-website-interface).

**Important** note that after `ssh` login via:
```
ssh <lrz-userid>@login.ai.lrz.de
```
you are on a *login node*. This means you can use the command line to execute commands mostly meant to set up your work for later, i.e., downloading a dataset. On this *login node* you cannot perform command involving `sudo` or download packages via `apt install`.

You can see that you are on the login node because your command line looks something like this:
```
<lrz-userid>@login-04 $ >
```
The actual work is then performed on different server nodes if you use the [command line execution](#work-with-command-line-for-interactive-job-execution).

*Note:* if you have access to the previously described DSS I'd recommend creating a symbolic link from your DSS storage to your `$HOME` directory for easier use. \
This can be done via:
```
ln -s /dss/dssfs04/<your_dir_path> <link_name>
```

*Hint:* In terms of ease of running a [Jupyter Notebook on IWS](#work-with-website-interface) the best option. It probably is sufficient for most ML trainings and pretty close to the known Google Colab. Hence, I would recommend using it!

### Work with YOLOv9 on the LOCO dataset
<details><summary> <b>Infos on how to use the given scripts for automatically downloading data</b> </summary>

For ease of use, and because it is necessary to always download the data again when using Google's Colab, I wrote the `get_loco.sh` and the `transform_to_yolo_format.py` script which automatically download the LOCO dataset and transform it to fit YOLO standards.

These scripts also come in handy when preparing the data for execution on the LRZ AI System.
Firstly, I would recommend to:
```
git clone https://github.com/KoniHD/yolov9.git
```
to have the code available and then perform the following data transformation if needed.


To download the dataset perform the following command in the lcoation you want the dataset to be downloaded to.
```
./scripts/get_loco.sh
```
*Hint:* If you cloned the repo you will have to make the script executable first with:
```
chmod +x ./scripts/get_loco.sh
```

After the dataset is downloaded it is ready to be used by an object detection model using the 'MSCOCO' data anotation format. However, if needed it can be transformed using the `transform_to_yolo_format.py` (which btw can also be used if you just want to **get rid of the subdirectory structure** the LOCO dataset naturally comes with or if you only want to **convert the anotation format**). \
For parameter explanation just use:
```
python3 ./scripts/transform_to_yolo_format.py --help
```
If you want to use it for further usage with the YOLOv9 model use these parameters:
```
python3 ./scripts/transform_to_yolo_format.py -d ./<path_to_loco_dir> --convert-annotations --convert-images
```

Both these scripts are already included in the Jupyter Notebook `train-yolov9.ipynb` which is meant for use with Google Colab. \
If you want to train the model on the LRZ Systems I'd recommend to execute both of these scripts once on a login node and then copy the resulting `./loco` directory into your DSS for training purposes later. After that you can use a different Jupyter Notebook written for [LRZ Website Interface](#work-with-website-interface) found under `LRZ-AI-Systems/train-model.ipynb`.

</details>

## Work with command line for interactive job execution

**DISCLAIMER** The prefered way by LRZ is submitting a [batch job](#work-with-batch-jobs).

**HINT**: the official LRZ documentation for this step can be found [here](https://doku.lrz.de/6-running-applications-as-interactive-jobs-on-the-lrz-ai-systems-10746640.html).

For this method you might want to get familiar with slurm for job scheduling (Documentation can be found here: [SLURM Doc](https://slurm.schedmd.com/documentation.html) with the most important commands and options being here: [SLURM Commands](https://slurm.schedmd.com/pdfs/summary.pdf).

The steps to get an interactive job running are essentially the same as discribed in [Pull and Customize NGC Container](#pull-and-customize-ngc-container-for-the-lrz-ai-system) with some minor changes:
* If you already have a configured container image ready there is no need for step 4. Instead you can continue with step 5, 6, 7.
* Instead of step 8 you perform your training here and then finish the same way.

**NOTE** I have yet to test mounting data into the container so this execution method is still pretty useless :grin:.

## Work with Batch jobs
**HINT**: the official LRZ documentation for this step can be found [here](https://doku.lrz.de/7-running-applications-as-batch-jobs-on-the-lrz-ai-systems-10746643.html).

An example batch script can be found under: `./LRZ-AI-Systems/lrz-execution.sbatch` or `./LRZ-AI-Systems/lrz-distributed-execution.sbatch`.

For this script to work however there are a few comments about the structure first of `#SBATCH` instructions I want to highlight:

* The name you give the job is important because you can later use it to get a status on said job via:
```
squeue --name=<your-job-name>
```
* Eventhough I suspect that if you select more than one gpu (e.g.: `--gres=gpu:2`) that these GPUs will be on the same node. However I am unsure of that so I would still specify `--nodes=1` to be sure to avoid the hustle with multiple nodes.
* The batch script has to provide an error as well as an output path. In order to name them consistently SLURM offers some [options](https://slurm.schedmd.com/sbatch.html#SECTION_FILENAME-PATTERN) for a filename patter.
* The notification via email is *optional*, however I found it very useful. Options for notifications can also be found in the [sbatch documentation](https://slurm.schedmd.com/sbatch.html). **Important:** LRZ requires a vaild email address to be specified for this process, otherwise email notifications will be blocked for your account &rarr; double check the address! :smiley:
* If your script can be started without modifications after an interuptions you can leave out the SBATCH `--no-requeue` option.
* To avoid having surprising env variables from your login config it is helpful to use the `--export=NONE` option and set env variables later on in the script.

Now the real computing then should be performed by passing the script `srun` command. (Currently I am unsure if more than one `srun` command is valid in a single `.sbatch` script so there might be a limitation to the compute you can do.) \
However, before the `srun` command you can perform short bash commands to setup the job like setting your own env variables. Just make sure to also pass these variables to `srun` using the `--export=<your-vars>` option because env vars set in the `.sbatch` script before this point are not valid in the `srun` command and hence your script otherwise.


### Mutli-GPU process via Batch job

If you really need this, this manual is probably not for you :grin:! Sorry but I tried really hard to get my script to work in a distributed fashion but it is **HARD!!**

## Work with website interface

**HINT**: the official LRZ documentation for this step can be found [here](https://doku.lrz.de/10-interactive-web-servers-on-the-lrz-ai-systems-10746644.html).

*NOTE:* Definetly the easiest option for most tasks so refer to this please! (Also this option is closest to Google's Colab if you are looking for that) :smiley:\
Also currently it is the only working way of accessing the LRZ computing resources.
1. Make sure you are connected to the Munich Scientific Network meaning you are connected to a Munich University Wifi or by using [EduVPN](https://doku.lrz.de/vpn-10333177.html?showLanguage=en_GB).
2. Login to [LRZ AI](https://login.ai.lrz.de).
3. Go to **Interactive Apps**.
4. Select **Jupyter Notebook** and chose the resources needed (they are specified very well here!!) and specify the time this notebook will be up. **Careful** the notebook shuts down automatically after the time runs up so make sure to schedule enough time or regularly save your training progress.
    * **Note:** Using the IWS gives you access only to a single GPU. Hence, distributed computing over multiple GPUs for more VRAM is not possible via this method. Once you maxed out the VRAM of a single GPU you might need to look at options.
    * The A100 (and if LRZ gets them later the H100) cards are set upt using a technology caleld [MIG slice](https://www.nvidia.com/en-us/technologies/multi-instance-gpu/). This means you don't even get access to a full GPU but rather a slice. In practice this should not affect your training.
5. You can select between 2 possible default *enroot* container images to let your Jupyter Notebook run in: One uses Tensorflow the other uses PyTorch. \
However, if you set up the credentials for NGC containers as discribed [previously](#nvidia-ngc-containers) you can also select **custom** and past the NGC container tag from the [NGC Container Catalog](https://catalog.ngc.nvidia.com) into the field.
6. For some reason I was unable to find the correct mounting point on the AI System. Failed attempts were: `/dss/dssfs04/my-data:/jupyter_session` &rarr; crashed notebook before start; `/dss/dssfs04/my-data:/data` and `/dss/dssfs04/my-data:/mnt/data` both just did not work. Talking to the support, I was affirmd, that the current best sollution is to have a symlink as described [here](#working-on-the-lrz-ai-system).
7. After that your request will be automatically queued in the to LRZ AI System and once it's the resources are free the website will automatically provide you with a link to a Jupyter Notebook.
8. Most Python libraries are already included if you chose the right *enroot* container from step 5. However, you might want to use different packages. In this case I'd recommend pip installing them right at the beginning. To be sure they are installed you should then reload the Notebook kernel.

&rarr; If anything goes wrong or the Notebook is stuck (happend to me) you can see an output log of the session: \
Go to the IWS portal where you can also always check the remaining time and click on **Session ID**. There are multiple files automatically created for you related to the job you submitted. If your job was started there will be a file called `output.log`. Here you can check for errors that might have occurred.
If your Notebook is frozen I would recommend checking this `output.log` and maybe start again if an actual error occurred.

### Work with YOLOv9 on IWS
<details><summary> <b>Infos on how to use the given Jupyter Notebook on the LRZ AI System</b> </summary>

* Like mentioned above first create a Linux symlink for your data and model stored on `/dss/dssfs04/<your_dir_path>` to `$HOME` as described in the [basics chapter](#working-on-the-lrz-ai-system).
* Since the AI System is not intended for testing I would recommend cloning the git repo into your `/dss/dssfs04` and follow the steps done in [working with loco on IWS](#work-with-yolov9-on-the-loco-dataset). In the execution I would recommend only to perform `git pull`.
* I put together a Jupyter Notebook meant for execution on the LRZ System: `./LRZ-AI-Systems/train-model.ipynb`. In this script the first two code cells are meant to be performed before every training execution in oder to 1. clone the latest changes you commited from *coding on your own* machine 2. install the necessary pip extensions mentioned in the [README.md](https://github.com/WongKinYiu/yolov9/blob/main/README.md#installation).
* After executing the first two cells reload the kernel and then start the Notebook again beginning with the third cell!
* Also the Notebook automatically **deletes** data from previous runs in the sixth cell because the intented use is to `scp` the `./yolov9/runs` directory a different storage place (like your own machine). If you do not want this feel free to modify said cell.

</details>