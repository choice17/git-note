# git-note

- initialize a git repo

git init

- add all the file to the .git

git add *

- commit to create log for .git\n
git commit -m "first commit" \n
//git commit -m <"msg">

- add remote origin on web github/ gitlab\n
git remote add origin https://github.com/<username>/<project-name>.git

- push the changes / commit on remote 
git push -u origin master

- checkout to the branch
git checkout <branchname> -- <filename>
-- checkout to new branch
git checkout -b <new branch> <src branch>

- fetch (safely copy the new file from branch)
git fetch <branch>

- check the git history
git log <--stat> <commit-id>
git status <commit-id>
git diff <commit-id> <commit-id>
git diff <branch name>

- merge master branch ex.
git checkout master
git pull
git checkout <test>
git pull
git rebase -i master
git checkout master
git merge <test>
  
X avoid operatio: never use rebase on public branch 
git checkout master
git rebase -i test

