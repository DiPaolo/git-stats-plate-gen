# Git Stats Plate Generator
CLI & GUI tool to generate image plate for your GitHub repositories.

### Features
- Collect lines of code (LOC) over all repos of a GitHub user:
  - private repos are taken into account
  - forked repos are NOT taken into account
- The both CLI & GUI variants are available
- Use cache to do not recalculate all the 
- It's safe & secure:
  - no cloud used 
  - no token stored
  - repos deleted locally after cloned & processed

### Screenshots
![](https://github.com/DiPaolo/git-stats-plate-gen/blob/main/assets/images/screenshot_2023_08_28_v1.0.0.png)

### Download
Pre-built binaries for **Windows**, **Linux**, and **MacOS** are available on [Release](https://github.com/DiPaolo/git-stats-plate-gen/releases) page.

### Usage

##### CLI
The easiest command line you would probably like to go first is the following:
```commandline
git_stats_plate_gen_cli -u <your_username>
```

That's it! You'll be securely asked for token then. Once your repos processed, an output image will be generated.

Here is the full list of available options.

```commandline
Usage: git_stats_plate_gen_cli [OPTIONS]

Options:
  -v, --version             Print version
  -u, --user <name>         GitHub username
  -t, --token <token>       GitHub token (just google 'GitHub Creating a
                            personal access token'); you need only to grant
                            access to Repository permissions: Read access to
                            code, commit statuses, and metadata
  -o, --output <filename>   Output image filename where the graph will be
                            written  [default:
                            github_lang_stats-%Y_%m_%d-%H_%M_%S.png]
  --cache / --no-cache      Use cached data to plot graphics  [default: cache]
  -mp, --min-percent FLOAT  Lower boundary (%) that language must have to be
                            shown
  --help                    Show this message and exit.
```

#### GUI

Launch the binary, paste your token, and press **Collect Statistics**. NOTE: your GitHub username will be set based on
current system account name. Please change it manually if it doesn't match your GitHub account.  

> #### IMPORTANT
> 
> Unfortunately, macOS binaries are not signed yet. So you won't be able to launch the binaries. To do so, please refer 
> to this article **Open a Mac app from an unidentified developer** 
> (https://support.apple.com/en-ke/guide/mac-help/mh40616/mac).

### Run Python script
You can run the tool as a regular Python script instead of using pre-built binaries. To do so:

1. Clone the repo
2. (optional) Create virtual environment & activate it
```commandline
python -m virtualenv .venv
```
**Windows**
```commandline
.venv\Scripts\activate
```
**Linux**/**macOS**
```commandline
source .venv/bin/activate
```
3. Install dependencies
```commandline
python -m pip install -r requirements.txt
```
4. Run binaries:

CLI:
```commandline
python -m git_stats_plate_gen.cli [options]
```
GUI:
```commandline
python -m git_stats_plate_gen.gui
```

### License
MIT License

Copyright (c) 2023 Pavel Dittenbier

Please refer to [License page](https://github.com/DiPaolo/git-stats-plate-gen/blob/main/LICENSE) for details.

### Contact
Please feel free to contact me: [pavel.ditenbir@gmail.com](mailto:pavel.ditenbir@gmail.com). 
