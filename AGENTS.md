Fix the github workflow: 

When we push to release/0.2.0  with commits such as "fix: this is a fix" , it should update the version using semantic versioning and then create a new release tag, however currently this is not working. The github action raw log output is as shown below.
Make sure that symantic versions works and that a new release candidate tag is created and release candidate is updated. 

Here is the latest raw output:

2025-05-25T15:33:28.9539432Z Current runner version: '2.324.0'
2025-05-25T15:33:28.9561054Z ##[group]Runner Image Provisioner
2025-05-25T15:33:28.9562044Z Hosted Compute Agent
2025-05-25T15:33:28.9562613Z Version: 20250508.323
2025-05-25T15:33:28.9563314Z Commit: 81b259f29879f73b4213d199e42d8c3465dae986
2025-05-25T15:33:28.9564036Z Build Date: 2025-05-08T19:40:08Z
2025-05-25T15:33:28.9564684Z ##[endgroup]
2025-05-25T15:33:28.9565322Z ##[group]Operating System
2025-05-25T15:33:28.9565915Z Ubuntu
2025-05-25T15:33:28.9566383Z 24.04.2
2025-05-25T15:33:28.9566969Z LTS
2025-05-25T15:33:28.9567686Z ##[endgroup]
2025-05-25T15:33:28.9568236Z ##[group]Runner Image
2025-05-25T15:33:28.9568926Z Image: ubuntu-24.04
2025-05-25T15:33:28.9569471Z Version: 20250511.1.0
2025-05-25T15:33:28.9570569Z Included Software: https://github.com/actions/runner-images/blob/ubuntu24/20250511.1/images/ubuntu/Ubuntu2404-Readme.md
2025-05-25T15:33:28.9572095Z Image Release: https://github.com/actions/runner-images/releases/tag/ubuntu24%2F20250511.1
2025-05-25T15:33:28.9573252Z ##[endgroup]
2025-05-25T15:33:28.9574420Z ##[group]GITHUB_TOKEN Permissions
2025-05-25T15:33:28.9576613Z Contents: write
2025-05-25T15:33:28.9577529Z Metadata: read
2025-05-25T15:33:28.9578097Z PullRequests: write
2025-05-25T15:33:28.9578764Z ##[endgroup]
2025-05-25T15:33:28.9581845Z Secret source: Actions
2025-05-25T15:33:28.9582882Z Prepare workflow directory
2025-05-25T15:33:28.9903899Z Prepare all required actions
2025-05-25T15:33:28.9948288Z Getting action download info
2025-05-25T15:33:29.1913073Z ##[group]Download immutable action package 'actions/checkout@v4'
2025-05-25T15:33:29.1914271Z Version: 4.2.2
2025-05-25T15:33:29.1915401Z Digest: sha256:ccb2698953eaebd21c7bf6268a94f9c26518a7e38e27e0b83c1fe1ad049819b1
2025-05-25T15:33:29.1916624Z Source commit SHA: 11bd71901bbe5b1630ceea73d27597364c9af683
2025-05-25T15:33:29.1917764Z ##[endgroup]
2025-05-25T15:33:29.2598892Z ##[group]Download immutable action package 'actions/setup-python@v5'
2025-05-25T15:33:29.2599762Z Version: 5.6.0
2025-05-25T15:33:29.2600570Z Digest: sha256:0b35a0c11c97499e4e0576589036d450b9f5f9da74b7774225b3614b57324404
2025-05-25T15:33:29.2681648Z Source commit SHA: a26af69be951a213d495a4c3e4e4022e16d87065
2025-05-25T15:33:29.2682325Z ##[endgroup]
2025-05-25T15:33:29.4949127Z Download action repository 'snok/install-poetry@v1' (SHA:76e04a911780d5b312d89783f7b1cd627778900a)
2025-05-25T15:33:29.7593018Z Complete job name: semantic-release
2025-05-25T15:33:29.8301527Z ##[group]Run actions/checkout@v4
2025-05-25T15:33:29.8302466Z with:
2025-05-25T15:33:29.8302879Z   fetch-depth: 0
2025-05-25T15:33:29.8303331Z   fetch-tags: true
2025-05-25T15:33:29.8303759Z   ref: release/0.2.0
2025-05-25T15:33:29.8304424Z   token: ***
2025-05-25T15:33:29.8304864Z   persist-credentials: true
2025-05-25T15:33:29.8305405Z   repository: vilosource/pyeasycmdline
2025-05-25T15:33:29.8305940Z   ssh-strict: true
2025-05-25T15:33:29.8306367Z   ssh-user: git
2025-05-25T15:33:29.8306787Z   clean: true
2025-05-25T15:33:29.8307375Z   sparse-checkout-cone-mode: true
2025-05-25T15:33:29.8307905Z   show-progress: true
2025-05-25T15:33:29.8308349Z   lfs: false
2025-05-25T15:33:29.8308755Z   submodules: false
2025-05-25T15:33:29.8309196Z   set-safe-directory: true
2025-05-25T15:33:29.8309912Z ##[endgroup]
2025-05-25T15:33:29.9420243Z Syncing repository: vilosource/pyeasycmdline
2025-05-25T15:33:29.9423183Z ##[group]Getting Git version info
2025-05-25T15:33:29.9424444Z Working directory is '/home/runner/work/pyeasycmdline/pyeasycmdline'
2025-05-25T15:33:29.9425908Z [command]/usr/bin/git version
2025-05-25T15:33:29.9447899Z git version 2.49.0
2025-05-25T15:33:29.9474452Z ##[endgroup]
2025-05-25T15:33:29.9489795Z Temporarily overriding HOME='/home/runner/work/_temp/8d685840-03af-4488-82a2-8268ef382d04' before making global git config changes
2025-05-25T15:33:29.9492202Z Adding repository directory to the temporary git global config as a safe directory
2025-05-25T15:33:29.9504304Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/pyeasycmdline/pyeasycmdline
2025-05-25T15:33:29.9537998Z Deleting the contents of '/home/runner/work/pyeasycmdline/pyeasycmdline'
2025-05-25T15:33:29.9541823Z ##[group]Initializing the repository
2025-05-25T15:33:29.9546424Z [command]/usr/bin/git init /home/runner/work/pyeasycmdline/pyeasycmdline
2025-05-25T15:33:29.9610049Z hint: Using 'master' as the name for the initial branch. This default branch name
2025-05-25T15:33:29.9611941Z hint: is subject to change. To configure the initial branch name to use in all
2025-05-25T15:33:29.9616930Z hint: of your new repositories, which will suppress this warning, call:
2025-05-25T15:33:29.9618622Z hint:
2025-05-25T15:33:29.9619530Z hint: 	git config --global init.defaultBranch <name>
2025-05-25T15:33:29.9620601Z hint:
2025-05-25T15:33:29.9621592Z hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
2025-05-25T15:33:29.9623187Z hint: 'development'. The just-created branch can be renamed via this command:
2025-05-25T15:33:29.9624476Z hint:
2025-05-25T15:33:29.9625215Z hint: 	git branch -m <name>
2025-05-25T15:33:29.9626667Z Initialized empty Git repository in /home/runner/work/pyeasycmdline/pyeasycmdline/.git/
2025-05-25T15:33:29.9633392Z [command]/usr/bin/git remote add origin https://github.com/vilosource/pyeasycmdline
2025-05-25T15:33:29.9667840Z ##[endgroup]
2025-05-25T15:33:29.9669061Z ##[group]Disabling automatic garbage collection
2025-05-25T15:33:29.9674267Z [command]/usr/bin/git config --local gc.auto 0
2025-05-25T15:33:29.9706568Z ##[endgroup]
2025-05-25T15:33:29.9707962Z ##[group]Setting up auth
2025-05-25T15:33:29.9717492Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2025-05-25T15:33:29.9751616Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2025-05-25T15:33:30.0036767Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2025-05-25T15:33:30.0070557Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2025-05-25T15:33:30.0309713Z [command]/usr/bin/git config --local http.https://github.com/.extraheader AUTHORIZATION: basic ***
2025-05-25T15:33:30.0343158Z ##[endgroup]
2025-05-25T15:33:30.0344841Z ##[group]Fetching the repository
2025-05-25T15:33:30.0361206Z [command]/usr/bin/git -c protocol.version=2 fetch --prune --no-recurse-submodules origin +refs/heads/*:refs/remotes/origin/* +refs/tags/*:refs/tags/*
2025-05-25T15:33:30.3984050Z From https://github.com/vilosource/pyeasycmdline
2025-05-25T15:33:30.3986483Z  * [new branch]      codex/fix-semantic-versioning-in-github-workflows -> origin/codex/fix-semantic-versioning-in-github-workflows
2025-05-25T15:33:30.3989191Z  * [new branch]      develop                -> origin/develop
2025-05-25T15:33:30.3990788Z  * [new branch]      feature/github_actions -> origin/feature/github_actions
2025-05-25T15:33:30.3992714Z  * [new branch]      feature/github_actions_improvements -> origin/feature/github_actions_improvements
2025-05-25T15:33:30.3994543Z  * [new branch]      release/0.2.0          -> origin/release/0.2.0
2025-05-25T15:33:30.3998694Z  * [new branch]      release/testing_gitlab_release_pipeline -> origin/release/testing_gitlab_release_pipeline
2025-05-25T15:33:30.4000545Z  * [new tag]         v0.2.0                 -> v0.2.0
2025-05-25T15:33:30.4001716Z  * [new tag]         v0.2.1-rc.1            -> v0.2.1-rc.1
2025-05-25T15:33:30.4005380Z  * [new tag]         v0.2.1-rc.2            -> v0.2.1-rc.2
2025-05-25T15:33:30.4035952Z ##[endgroup]
2025-05-25T15:33:30.4042976Z ##[group]Determining the checkout info
2025-05-25T15:33:30.4135028Z [command]/usr/bin/git branch --list --remote origin/release/0.2.0
2025-05-25T15:33:30.4136729Z   origin/release/0.2.0
2025-05-25T15:33:30.4139344Z ##[endgroup]
2025-05-25T15:33:30.4140328Z [command]/usr/bin/git sparse-checkout disable
2025-05-25T15:33:30.4143155Z [command]/usr/bin/git config --local --unset-all extensions.worktreeConfig
2025-05-25T15:33:30.4154479Z ##[group]Checking out the ref
2025-05-25T15:33:30.4158261Z [command]/usr/bin/git checkout --progress --force -B release/0.2.0 refs/remotes/origin/release/0.2.0
2025-05-25T15:33:30.4224627Z Switched to a new branch 'release/0.2.0'
2025-05-25T15:33:30.4227744Z branch 'release/0.2.0' set up to track 'origin/release/0.2.0'.
2025-05-25T15:33:30.4233788Z ##[endgroup]
2025-05-25T15:33:30.4267544Z [command]/usr/bin/git log -1 --format=%H
2025-05-25T15:33:30.4288736Z d15db4111527725236cd23b9b4285be8a4b27899
2025-05-25T15:33:30.4470722Z ##[group]Run git fetch --prune --force --tags
2025-05-25T15:33:30.4471575Z [36;1mgit fetch --prune --force --tags[0m
2025-05-25T15:33:30.4659125Z shell: /usr/bin/bash -e {0}
2025-05-25T15:33:30.4659732Z ##[endgroup]
2025-05-25T15:33:30.7485162Z ##[group]Run actions/setup-python@v5
2025-05-25T15:33:30.7486426Z with:
2025-05-25T15:33:30.7487508Z   python-version: 3.12
2025-05-25T15:33:30.7488538Z   check-latest: false
2025-05-25T15:33:30.7489798Z   token: ***
2025-05-25T15:33:30.7490741Z   update-environment: true
2025-05-25T15:33:30.7491838Z   allow-prereleases: false
2025-05-25T15:33:30.7492908Z   freethreaded: false
2025-05-25T15:33:30.7493907Z ##[endgroup]
2025-05-25T15:33:30.9161360Z ##[group]Installed versions
2025-05-25T15:33:30.9278211Z Successfully set up CPython (3.12.10)
2025-05-25T15:33:30.9280808Z ##[endgroup]
2025-05-25T15:33:30.9499807Z ##[group]Run snok/install-poetry@v1
2025-05-25T15:33:30.9500907Z with:
2025-05-25T15:33:30.9501682Z   version: 1.7.1
2025-05-25T15:33:30.9502561Z   virtualenvs-create: true
2025-05-25T15:33:30.9503575Z   virtualenvs-in-project: true
2025-05-25T15:33:30.9504685Z   virtualenvs-path: {cache-dir}/virtualenvs
2025-05-25T15:33:30.9505833Z   installer-parallel: true
2025-05-25T15:33:30.9506764Z env:
2025-05-25T15:33:30.9507933Z   pythonLocation: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:30.9509637Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.10/x64/lib/pkgconfig
2025-05-25T15:33:30.9511309Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:30.9512816Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:30.9514328Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:30.9515844Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.10/x64/lib
2025-05-25T15:33:30.9517361Z ##[endgroup]
2025-05-25T15:33:30.9607509Z ##[group]Run $GITHUB_ACTION_PATH/main.sh
2025-05-25T15:33:30.9608714Z [36;1m$GITHUB_ACTION_PATH/main.sh[0m
2025-05-25T15:33:30.9784119Z shell: /usr/bin/bash --noprofile --norc -e -o pipefail {0}
2025-05-25T15:33:30.9785407Z env:
2025-05-25T15:33:30.9786405Z   pythonLocation: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:30.9788208Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.10/x64/lib/pkgconfig
2025-05-25T15:33:30.9789835Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:30.9791308Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:30.9792777Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:30.9794262Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.10/x64/lib
2025-05-25T15:33:30.9795501Z   VERSION: 1.7.1
2025-05-25T15:33:30.9796357Z   VIRTUALENVS_CREATE: true
2025-05-25T15:33:30.9797569Z   VIRTUALENVS_IN_PROJECT: true
2025-05-25T15:33:30.9798640Z   VIRTUALENVS_PATH: {cache-dir}/virtualenvs
2025-05-25T15:33:30.9799754Z   INSTALLER_PARALLEL: true
2025-05-25T15:33:30.9800691Z   INSTALLATION_ARGUMENTS: 
2025-05-25T15:33:30.9801618Z   POETRY_PLUGINS: 
2025-05-25T15:33:30.9802414Z ##[endgroup]
2025-05-25T15:33:33.5274062Z 
2025-05-25T15:33:33.5275140Z [33mSetting Poetry installation path as /home/runner/.local[0m
2025-05-25T15:33:33.5275787Z 
2025-05-25T15:33:33.5276166Z [33mInstalling Poetry 👷[0m
2025-05-25T15:33:33.5276538Z 
2025-05-25T15:33:45.4305674Z Retrieving Poetry metadata
2025-05-25T15:33:45.4306587Z 
2025-05-25T15:33:45.4306782Z # Welcome to Poetry!
2025-05-25T15:33:45.4307251Z 
2025-05-25T15:33:45.4307537Z This will download and install the latest version of Poetry,
2025-05-25T15:33:45.4308167Z a dependency and package manager for Python.
2025-05-25T15:33:45.4308485Z 
2025-05-25T15:33:45.4308798Z It will add the `poetry` command to Poetry's bin directory, located at:
2025-05-25T15:33:45.4309267Z 
2025-05-25T15:33:45.4309411Z /home/runner/.local/bin
2025-05-25T15:33:45.4309666Z 
2025-05-25T15:33:45.4310039Z You can uninstall at any time by executing this script with the --uninstall option,
2025-05-25T15:33:45.4310666Z and these changes will be reverted.
2025-05-25T15:33:45.4310929Z 
2025-05-25T15:33:45.4311082Z Installing Poetry (1.7.1)
2025-05-25T15:33:45.4311553Z Installing Poetry (1.7.1): Creating environment
2025-05-25T15:33:45.4312099Z Installing Poetry (1.7.1): Installing Poetry
2025-05-25T15:33:45.4312619Z Installing Poetry (1.7.1): Creating script
2025-05-25T15:33:45.4313104Z Installing Poetry (1.7.1): Done
2025-05-25T15:33:45.4313384Z 
2025-05-25T15:33:45.4313549Z Poetry (1.7.1) is installed now. Great!
2025-05-25T15:33:45.4313844Z 
2025-05-25T15:33:45.4314068Z You can test that everything is set up by executing:
2025-05-25T15:33:45.4314453Z 
2025-05-25T15:33:45.4314639Z `poetry --version`
2025-05-25T15:33:45.4314873Z 
2025-05-25T15:33:48.0355578Z 
2025-05-25T15:33:48.0356469Z [33mInstallation completed. Configuring settings 🛠[0m
2025-05-25T15:33:48.0356923Z 
2025-05-25T15:33:48.0357606Z [33mDone ✅[0m
2025-05-25T15:33:48.0357825Z 
2025-05-25T15:33:48.0358847Z [33mIf you are creating a venv in your project, you can activate it by running 'source .venv/bin/activate'. If you're running this in an OS matrix, you can use 'source $VENV' instead, as an OS agnostic option[0m
2025-05-25T15:33:48.0403598Z ##[group]Run make dev-install
2025-05-25T15:33:48.0403877Z [36;1mmake dev-install[0m
2025-05-25T15:33:48.0456563Z shell: /usr/bin/bash -e {0}
2025-05-25T15:33:48.0456790Z env:
2025-05-25T15:33:48.0457293Z   pythonLocation: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:48.0457728Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.10/x64/lib/pkgconfig
2025-05-25T15:33:48.0458140Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:48.0458495Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:48.0458854Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:48.0459209Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.10/x64/lib
2025-05-25T15:33:48.0459513Z   VENV: .venv/bin/activate
2025-05-25T15:33:48.0459716Z ##[endgroup]
2025-05-25T15:33:48.0550046Z poetry install --with dev
2025-05-25T15:33:48.4245846Z Creating virtualenv pyeasycmdline in /home/runner/work/pyeasycmdline/pyeasycmdline/.venv
2025-05-25T15:33:48.4932765Z The --no-wheel and --wheel options are deprecated. They have no effect for Python > 3.8 as wheel is no longer bundled in virtualenv.
2025-05-25T15:33:49.0490887Z Updating dependencies
2025-05-25T15:33:49.0493104Z Resolving dependencies...
2025-05-25T15:33:51.3341134Z 
2025-05-25T15:33:51.3341850Z Package operations: 49 installs, 0 updates, 0 removals
2025-05-25T15:33:51.3342363Z 
2025-05-25T15:33:51.3346814Z   • Installing certifi (2025.4.26)
2025-05-25T15:33:51.3357567Z   • Installing charset-normalizer (3.4.2)
2025-05-25T15:33:51.3368415Z   • Installing idna (3.10)
2025-05-25T15:33:51.3377180Z   • Installing urllib3 (2.4.0)
2025-05-25T15:33:51.5033648Z   • Installing mdurl (0.1.2)
2025-05-25T15:33:51.5039124Z   • Installing requests (2.32.3)
2025-05-25T15:33:51.5043990Z   • Installing smmap (5.0.2)
2025-05-25T15:33:51.5081619Z   • Installing typing-extensions (4.13.2)
2025-05-25T15:33:51.5496699Z   • Installing annotated-types (0.7.0)
2025-05-25T15:33:51.5502496Z   • Installing gitdb (4.0.12)
2025-05-25T15:33:51.5507527Z   • Installing iniconfig (2.1.0)
2025-05-25T15:33:51.5512992Z   • Installing markdown-it-py (3.0.0)
2025-05-25T15:33:51.5557488Z   • Installing markupsafe (3.0.2)
2025-05-25T15:33:51.5588252Z   • Installing pluggy (1.6.0)
2025-05-25T15:33:51.5594906Z   • Installing pydantic-core (2.33.2)
2025-05-25T15:33:51.5693188Z   • Installing packaging (25.0)
2025-05-25T15:33:51.6486656Z   • Installing pygments (2.19.1)
2025-05-25T15:33:51.6520434Z   • Installing requests-toolbelt (1.0.0)
2025-05-25T15:33:51.6550513Z   • Installing typing-inspection (0.4.1)
2025-05-25T15:33:51.8973181Z   • Installing astroid (3.3.10)
2025-05-25T15:33:51.8978149Z   • Installing click (8.1.8)
2025-05-25T15:33:51.8979834Z   • Installing coverage (7.8.2)
2025-05-25T15:33:51.8984849Z   • Installing dill (0.4.0)
2025-05-25T15:33:51.8992922Z   • Installing dotty-dict (1.3.1)
2025-05-25T15:33:51.8997492Z   • Installing gitpython (3.1.44)
2025-05-25T15:33:51.9003145Z   • Installing importlib-resources (6.5.2)
2025-05-25T15:33:51.9016425Z   • Installing isort (6.0.1)
2025-05-25T15:33:51.9817461Z   • Installing jinja2 (3.1.6)
2025-05-25T15:33:52.0414305Z   • Installing mccabe (0.7.0)
2025-05-25T15:33:52.0472443Z   • Installing mypy-extensions (1.1.0)
2025-05-25T15:33:52.0938878Z   • Installing pathspec (0.12.1)
2025-05-25T15:33:52.1026562Z   • Installing platformdirs (4.3.8)
2025-05-25T15:33:52.1181949Z   • Installing pycodestyle (2.13.0)
2025-05-25T15:33:52.1346223Z   • Installing pydantic (2.11.5)
2025-05-25T15:33:52.1480982Z   • Installing pyflakes (3.3.2)
2025-05-25T15:33:52.1638867Z   • Installing pytest (7.4.4)
2025-05-25T15:33:52.1915928Z   • Installing python-gitlab (4.13.0)
2025-05-25T15:33:52.1933850Z   • Installing rich (14.0.0)
2025-05-25T15:33:52.2723984Z   • Installing shellingham (1.5.4)
2025-05-25T15:33:52.2976765Z   • Installing tomlkit (0.13.2)
2025-05-25T15:33:52.4925257Z   • Installing black (25.1.0)
2025-05-25T15:33:52.4931038Z   • Installing flake8 (7.2.0)
2025-05-25T15:33:52.4936461Z   • Installing mypy (1.15.0)
2025-05-25T15:33:52.4946039Z   • Installing pylint (3.3.7)
2025-05-25T15:33:52.4959065Z   • Installing pytest-cov (6.1.1)
2025-05-25T15:33:52.4963559Z   • Installing pytest-mock (3.14.0)
2025-05-25T15:33:52.4971979Z   • Installing python-semantic-release (8.7.0)
2025-05-25T15:33:52.4981269Z   • Installing pyyaml (6.0.2)
2025-05-25T15:33:52.5768371Z   • Installing types-pyyaml (6.0.12.20250516)
2025-05-25T15:33:53.5123701Z 
2025-05-25T15:33:53.5124184Z Writing lock file
2025-05-25T15:33:53.5124787Z 
2025-05-25T15:33:53.5125182Z Installing the current project: pyeasycmdline (0.2.1-rc.2)
2025-05-25T15:33:53.6727590Z ##[group]Run poetry add --group dev python-semantic-release@^8.0.0
2025-05-25T15:33:53.6728111Z [36;1mpoetry add --group dev python-semantic-release@^8.0.0[0m
2025-05-25T15:33:53.6779638Z shell: /usr/bin/bash -e {0}
2025-05-25T15:33:53.6779884Z env:
2025-05-25T15:33:53.6780140Z   pythonLocation: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:53.6780553Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.10/x64/lib/pkgconfig
2025-05-25T15:33:53.6780969Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:53.6781330Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:53.6781709Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:53.6782062Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.10/x64/lib
2025-05-25T15:33:53.6782369Z   VENV: .venv/bin/activate
2025-05-25T15:33:53.6782581Z ##[endgroup]
2025-05-25T15:33:54.3597611Z 
2025-05-25T15:33:54.4325905Z Updating dependencies
2025-05-25T15:33:54.4335621Z Resolving dependencies...
2025-05-25T15:33:54.9045798Z 
2025-05-25T15:33:54.9046135Z No dependencies to install or update
2025-05-25T15:33:55.0781826Z ##[group]Run git config --global user.name "GitHub Action"
2025-05-25T15:33:55.0782251Z [36;1mgit config --global user.name "GitHub Action"[0m
2025-05-25T15:33:55.0782609Z [36;1mgit config --global user.email "action@github.com"[0m
2025-05-25T15:33:55.0782954Z [36;1mpoetry run semantic-release publish[0m
2025-05-25T15:33:55.0832766Z shell: /usr/bin/bash -e {0}
2025-05-25T15:33:55.0833002Z env:
2025-05-25T15:33:55.0833245Z   pythonLocation: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:55.0833841Z   PKG_CONFIG_PATH: /opt/hostedtoolcache/Python/3.12.10/x64/lib/pkgconfig
2025-05-25T15:33:55.0834246Z   Python_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:55.0834608Z   Python2_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:55.0834964Z   Python3_ROOT_DIR: /opt/hostedtoolcache/Python/3.12.10/x64
2025-05-25T15:33:55.0835317Z   LD_LIBRARY_PATH: /opt/hostedtoolcache/Python/3.12.10/x64/lib
2025-05-25T15:33:55.0835651Z   VENV: .venv/bin/activate
2025-05-25T15:33:55.0836058Z   GH_TOKEN: ***
2025-05-25T15:33:55.0836338Z   GITHUB_TOKEN: ***
2025-05-25T15:33:55.0836527Z ##[endgroup]
2025-05-25T15:33:56.8078355Z [15:33:56] WARNING  [semantic_release.hvcs.github] WARNING         github.py:252
2025-05-25T15:33:56.8079338Z                     github.upload_dists: No release corresponds to              
2025-05-25T15:33:56.8080139Z                     tag v0.2.1-rc.2, can't upload dists                         
2025-05-25T15:33:56.8623999Z Post job cleanup.
2025-05-25T15:33:57.0219100Z Post job cleanup.
2025-05-25T15:33:57.1141638Z [command]/usr/bin/git version
2025-05-25T15:33:57.1176963Z git version 2.49.0
2025-05-25T15:33:57.1213596Z Copying '/home/runner/.gitconfig' to '/home/runner/work/_temp/b4c1da9a-5503-4eb3-aeae-0ef72c898971/.gitconfig'
2025-05-25T15:33:57.1223947Z Temporarily overriding HOME='/home/runner/work/_temp/b4c1da9a-5503-4eb3-aeae-0ef72c898971' before making global git config changes
2025-05-25T15:33:57.1224980Z Adding repository directory to the temporary git global config as a safe directory
2025-05-25T15:33:57.1236237Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/pyeasycmdline/pyeasycmdline
2025-05-25T15:33:57.1269092Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
2025-05-25T15:33:57.1300629Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
2025-05-25T15:33:57.1523689Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
2025-05-25T15:33:57.1542962Z http.https://github.com/.extraheader
2025-05-25T15:33:57.1555313Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
2025-05-25T15:33:57.1585523Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
2025-05-25T15:33:57.1899497Z Cleaning up orphan processes
