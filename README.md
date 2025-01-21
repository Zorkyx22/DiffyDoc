# DiffyDoc
DiffyDoc is an assistant for Microsoft Word documents. Its goal is to comment on the content of the document without breaking it. To do so, the agent inserts MSWord comments and exports the new file.

## Clone this repository
You need GIT in order to clone this repository. If you do not have GIT installed, you can download a ZIP archive of the repository and safely skip this step.
In order to clone this repository, open a command prompt and navigate to a path where you wish to download the folder to. Then, run the following command:
`git clone https://github.com/Zorkyx22/DiffyDoc.git`

## Requirements
This project is written in Python as that is the most easy to start with. If I work more on this in order to make a public release, I will most likely write it in a compilable language like rust or c++. I think rust has the better support for Ollama usage, but tbd.

Make sure you have python installed. I advise the use of virtual environments when running python projects as to not break your global python configuration.
### How to create a virtual environment with Python
You can safely skip this skep as it is optional, however it is advised to go through these steps.
1. From your command prompt, navigate to the root of this repository and run the following command: `python -m venv <name of folder>`. I usually use `.venv` as the name of the folder. The next steps will assume that `.venv` was used.
2. Wait for the command to complete. This can take a minute.
3. Activate the virtual environment. You can do this by running the activation script (windows) or sourcing the activation file (unix).
    **Windows Powershell**: `.\.venv\Scripts\activate`
    **Windows bash**: `.\.venv\Scripts\activate.bat`
    **Unix**: `source ./.venv/bin/activate`
4. Now you environment is activated, so any python packages that you install will only be installed here. Repeat step 3 whenever you need to run this tool.

### Python Requirements
The python requirements are listed in the `requirements.txt` file at the root of the repository. You can download them all automatically using python. From your command prompt, navigate to the root of the repository and execute the following command:
`python -m pip install -r requirements.txt`

### Ollama Requirements
This project currenlty only uses a locally-run LLM with Ollama. In order to set this up, first install Ollama. See their repo for more instructions on how to do that: [Github.com/Ollama/Ollama](https://github.com/ollama/ollama)

You will need a model to run this. You can select one from [Ollama.com/Library](https://ollama.com/library)
In order to select the model best suited for you, as I have a pretty basic machine, I usually stick to 1B or 3B models. If I go any higher, The tasks take many minutes (sometimes hours). I currently use `llama3.2:3b-instruct-Q5_K_M`. This is set as the default in the script, so installing this model is the simplest to setup.

## Running
Once you're setup, you can run the application using the following syntax:
`python document_parser.py [-h] [--model MODEL] file`
```bash
positional arguments:
  file                  The docx file you wish to translate

options:
  -h, --help            show this help message and exit
  --model MODEL, -m MODEL
                        The model to use with the local ollama server. The
                        default is llama3.2:3b-instruct-q5_K_M
```

## Modifying the prompt
The prompt used is located in the `constants.py` file. Feel free to play with it.
