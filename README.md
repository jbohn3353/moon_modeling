### Current Model, v3
Adapted from https://github.com/johnowagon/lunar-surface-temperature <br>
As I wasn't focused on temperature, I believe that there might still need to be work done for modeleing properties on the dark side but this wasn't an issue for irradiance. In addition to the 3D model, this will create a plot of your desired function over the period of a whole day at a specific latitude, specified at the top of model.py

### How to run
Make sure to have pip installed on your machine. Clone the repo, cd in and run 
```sh
pip install -r requirements.txt
```
From there you can run
```sh
python3 model.py [latitude] [model_func]
```
and the plot will open in your default browser.

You can easily add functions to model_funcs.py and/or change the value of MODEL_FUNC at the top of model.py to change what is being modeled. 

### TODO
- Add abstracted framework for modeling the dark side easily
