### git-note

- check git current username 
'''
  git config --list | grep -a 
'''
  
- setup git user
'''
  git config --global user.name "Alvin J. Alexander"
  git config --global user.emal addr@emal.com
'''

- initialize a git repo
'''
  git init
'''

- add all the file to the .git
'''
  git add *
'''

- commit to create log for .git
'''
  git commit -m "first commit"
'''  
  '//git commit -m \<"msg">'

- add remote origin on web github/ gitlab
'''
  git remote add origin https://github.com/\<username>/\<project-name>.git
'''

- push the changes / commit on remote 

  ** for first push -> please use > git push --set-upstream origin master
'''
  git push -u origin master
'''

- checkout to the branch
'''
  git checkout \<branchname> -- \<filename>
'''
  
-- checkout to new branch
'''
  git checkout -b \<new branch> \<src branch>
'''

- fetch (safely copy the new file from branch)
'''
  git fetch \<branch>
'''

- check the git history
'''
  git log <--stat> \<commit-id>

  git status \<commit-id>

  git diff \<commit-id> \<commit-id>

  git diff \<branch name>
'''

- merge master branch ex.
'''
  git checkout master

  git pull

  git checkout \<test>

  git pull

  git rebase -i master

  git checkout master

  git merge \<test>
'''
 
 :x: avoid operatio: never use rebase on public branch 
'''
  git checkout master

  git rebase -i test
'''

- extra.

  [emoji symbol for .md](https://gist.githubusercontent.com/AliMD/3344523/raw/6cb0a435ad52bcd7465ab786f18e511ce5089924/gistfile1.md)

