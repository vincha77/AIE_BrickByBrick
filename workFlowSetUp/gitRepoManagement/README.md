
# Steps to Set Up a Git Repo Locally
1. cd into the directory that contains the files/folders to be made into a repo.  For example, if AIE_BrickByBrick is the folder whose contents will be in a single repo, then run `cd AIE_BrickByBrick` on your terminal.

2. Run `git init` to instantiate a local git repository (note - this command will set up a `.git` directory).

3. Optionally, you can create a `.gitignore` file into which you can add a list of files and folders that should be ignored by git.  Note that the `.gitignore` file should be in the same directory.

4. If you run `git status` at any time, you will be able to see the state of the local repository.  e.g., if you have modified files that have not yet been staged or committed, you will see a listing of the files/folders that have been modified since your last commit.

5. To stage all the modified files/folders to be committed to the repo, run `git add .`  You can check that all the files/folders you expect to be staged have been by running `git status`.  You should see a full list of files/folders that have been modified since your last commit.

6. Finally, commit the changes to the local repo by running the following command:
        `git commit -m <message>`
   Here, `<message>` is a short message that documents the main changes in this commit.  If you run `git status` now, you will see a message confirming that the local repo is up to date.

7. Optionally, now or at any time later, you can add some useful documentation in the top-level folder in your repo or any other sub-folder by creating README.md file(s).  Note that the README.md file should be in Markdown format to be rendered cleanly on your GitHub repo.


# Steps to Set Up a GitHub Repo
1. If you are new to GitHub, you'll need to set up an account on GitHub.

2. Log in to Github

3. Select the option to create a new repo.

4. Enter the name of the repo and other details as requested.  Note - leave the README file option unchecked.  You can create a README file in your local repo and upload it as needed.

5. Go to Settings on Main Github (note - not the settings for this particular repo but general settings).  Go to Developer Tools and then to Personal Access Tokens, and then to Tokens (classic) to set up a secure personal access token.

6. Optionally, you can also set up an SSH Key to have secure access to the repo.  This involves generating a public key that you will save on your local machine as well as on the GitHub repo.  While setting up the SSH Key, you should also instantiate a secure `PassPhrase`.  Note this passphrase somewhere secure to use in lieu of the personal access token.

6. Make sure to copy and save the token in a secure place on your local machine.  You'll only see this token once on GitHub, so be sure to copy and save it right away!

7. To save the local repo created earlier on to Github, go to your local repository and run the following commands:
        Step a: `git remote add origin https://github.com/<USERNAME>/<REPONAME>.git` 
        [Note that this format should be used with a minor change to update the repo using the personal access token]
        Instead, for SSH access, use `git remote add origin git@github.com:<USERNAME>/<REPONAME>.git`

        Step b: `git branch -M main`

        Step c: `git push -u origin main`

   This sequence of steps will push changes from the local repository to the remote repository on GitHub; verify that all files are saved on github!!!

8. Other very useful git commands to remember.
        Setting up global configuration:
                `git config --global user.email "<YOUR EMAIL ADDRESS>"`
                `git config --global user.name "YOUR NAME`

        There are several more git commands in the git section of the following page that you may find useful:
                https://github.com/AI-Maker-Space/Interactive-Dev-Environment-for-LLM-Development
