# Python project template

A simple project scaffold for Python projects. Includes a basic project structure, environment configuration, formatter, linter, Jupyter Notebook configuration and Git filter, and VS Code configuration.

# Setup

Make sure to rename the environment to what you want (the default name is `python-template`). You can do this by changing the `name` field in the `environment.yml` file. Similarly rename the folder `python-template` to the name of your project. After doing so, delete the `.git` folder and run `git init -b main` to start a new git repository.

Once you are ready to push to an empty remote repository, you can run the following commands:

```sh
# Add origin
git remote add origin <url-of-repo>
# Push to the upstream branch
git branch -M main
git push -u origin main
```

Prerequisites:

- Mamba (or Conda) ; you can check out my installation instructions [here](https://github.com/RobertBarachini/how2dev/blob/main/src/md/dev-environment/python.md#mamba)

Create a new environment (make sure you renamed it to what you want):

```bash
# Create a new environment using the environment.yml file
mamba env create -f environment.yml
# Activate the environment (this usually happens automatically once you configure VS Code or other IDE and open a new terminal)
mamba activate <environment-name>
# Deactivate the environment
mamba deactivate
```

If you are prompted to select an interpreter, you can select the Python interpreter from the newly created environment. If it is not listed, you can add it from the `~/mambaforge/envs/<environment-name>/bin/python` path.

## Post-setup

To make sure you don't commit the Jupyter Notebook outputs, execution count, and metadata, you can set up a custom filter using `nbstripout`. This will remove the outputs and metadata from the notebooks before committing them while keeping the local notebook files intact.

```bash
# Run in the root of the repository
nbstripout --install --attributes .gitattributes
```
