# Steps to setup the image_processor

# Git clone the image_processor repo.
git clone https://github.com/impala97/image_processor.git

# Create a folder where you can keep your all virtual environments for all projects
mkdir ~/virt

# Now create a virtual environment for image_processor with python3.7
virtualenv ~/virt/imgage_processor -p python3.7

# Once it's crated now we have to activate it & install all requirements to run this project.
pip install -r ~/image_processor/requirements.txt

# Now all you have to do is run the start_app.sh to start the image_processor app
cd ~/image_processor; ./start_app.sh

# Now open a browser and enter the below link to access our project.
http://localhost:2525/
