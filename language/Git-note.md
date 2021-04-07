# git-note

## content table
- **[git initalize config](#inital-config)**  
- **[branches management](#branches-management)**  
- **[git log](#log)**  
- **[merge branch](#merge-branch)**  
- **[cherry pick](#cherry-pick)**  
- **[tagging](#tagging)**  
- **[stash](#stash)**  
- **[rebase](#rebase)**  
- **[reflog](#reflog)**  
- **[conflict](#conflict)**  
- **[remove file](#remove)**  
- **[useful command](#useful-command)**  
- **[reference](#reference)**  
- **[gitconfig](#gitconfig)**  
- **[gitmessage](#gitmessage)**  
- **[patch](#patch)**  
- **[merge-repo](#merge-repo)**  

## repo 
- **[repo intro](#repo-intro)**  
- **[forall -pvc](#forall)**  
- **[repo sync](#forall)**  
- **[repo init](#init)**  
- **[repo manifest](#manifest)**  
- **[repo status](#status)**  
- **[repo branch](#branch)**  


## inital config  
* check git current username 
```bash
  git config --list | grep -a 
```
  
* setup git user 
```bash
  git config --global user.name "Takchoi yu"
  git config --global user.emal takchoi@email.com
```

* initialize a git repo
```bash
  git init
```

* add all the file to the .git
```bash
  git add *
```

* commit to create log for .git
```bash
  git commit -m "first commit"
``` 
  `//git commit -m <"msg">`

* add remote origin on web github/ gitlab
```bash
  git remote add origin https://github.com/<username>/<project-name>.git
```

* push the changes / commit on remote 

  ** for first push -> please use > git push --set-upstream origin master
```bash
  git push -u origin master
```

## branches management  

* checkout to the branch 
```bash
  git checkout <branchname> -- <filename>
```
  
* checkout to new branch 
```bash
  git checkout -b <new branch>
```

* fetch (safely copy the new file from branch, only update git info, but not current file system)  
```bash
  git fetch origin <branch>
```

* pull (copy new file status from remote branch into current file systems)  
```bash
  git pull origin <branch>
```

* check the git history 
```bash
  git log <--stat> <commit-id>
  git log --oneline -n<num>
  git log --pretty=format:"%h%x09%an%x09%s" <branch>

  git status <commit-id>

  git diff <commit-id> <commit-id>

  git diff <branch name>
```

Output the different commits between two branches.
```bash
  git log --left-right --graph --cherry-pick --oneline @...origin/mp-agt902-3 --pretty=format:"%h%x09%an%x09%s"
```

* merge remote master branch ex. 
```bash
  git checkout <master>

  git pull origin <master>

  git checkout <test>

  git checkout master

  git merge <test>
  
```
 
 :x: avoid operation: never use rebase on public branch 
```bash
  git checkout master

  git rebase -i test<desired commit>
```

## log

```bash
  git log
  git log --oneline -n10
```

* log format

```
  git log --pretty=format:"%h%x09%an%x09%ad%x09%s"
  %h = abbreviated commit hash
  %x09 = tab (character for code 9)
  %an = author name
  %ad = author date (format respects --date= option)
  %s = subject
```

## merge branch  

* create a branch (feature-1) and merge to (develop)  
```bash
  git checkout develop
  git branch
```
  `you are now in develop branch`  
  **`develop features`**
* suppose that you have some features file  
```bash
  git checkout -b feature-1
  git add feature_file
  git commit  
```
  `should now in (feature-1) branch`
`catch up with develop branch before finishing the feature`
```bash
  git co develop
  git fetch origin develop
  git co feature-1
  gitk --all
  git merge origin/develop
```
  `merge to develop branch and delete feature branch`
```bash
  git checkout develop
  git merge --squash feature-1
  git commit
  git push
  git branch -d feature-1
```

* condition two - update a new file  
  `at local branch`    
```bash
  (local) git add {file}
  (local) git commit -m {meesage}
  (local) git fetch
  (local) git commit -m {message} -> nothing if your the most update one  
  (local) git push -u origin master -> (master)
```

## cherry-pick  

Suppose you are at the `feature-1` branch
A old branch `feature-old` have a crucial feature commit id `e123old` unused and you want to include to your branch 

```
  (master)    git checkout feature-1
  (feature-1) git cherry-pick  e123old
```

Done! it is easy but you have to fix if there is any conflict!


## tagging  

tagging is to mapping the commit ID to self-defined tag name  
[ref](https://stackoverflow.com/questions/5195859/how-do-you-push-a-tag-to-a-remote-repository-using-git/26438076#26438076)

* add tag to local  
  `at local (master)`  
```bash
  (master) git tag v1.0.0
  (master) git tag -l
          v1.0.0
```  

* checkout tag  
  `at local (master)`  
```bash
  (master) git co tags/<tagname>  
  ((tagname)) 
```  

* remove tag  
```bash
  (master) git tag --delete <tagname>  
```  

* push to remote  
  `at local (master)`  
```bash
  (master) git push origin <tagname>
```  

* remove remote tag  

```bash
  git push --delete origin <tagname>
```
## stash  

If developers are working in local feature branch but the works are not ready to commit yet.
Developers can use `git stash` to save the changes to stash list and merge with remote commit.  


```
   check at local files uncommit files
commits 
A-B-C-D-E(HEAD) (feature)
        |-changes on feature.py
```
* stash the changes  
```bash
  /* local feature branch */
  (feature) git stash  
  (feature) git stash list  
  stash@{0} WIP on (feature): sd23sx92 Test stash
```

```bash
  /* add with stash message */
  (feature) git stash save "your stash message"
```

* 2. then pull/merge with the remote feature branch
```bash
  /* pull at local feature branch */
  (feature) git pull  
```
  `stash apply the changes at stash list` `apply` - load the changes, `pop` - get and remove the stash  
```bash
  (feature) git stash apply stash@{<id>}
```

* delete stash  
```bash
  (feature) git stash drop stash@{<id>}
```

* stash unsaved untracked item  
```bash
  (feature) git stash save -u 
```

## rebase  

Rebase is to edit the commit message, includes the commit history with author info
```bash  
  commits 
  A-B-C-D-E(HEAD) (master)
    |-|-> want to edit B-C commits
```

* git rebase

```bash
  $(master) git rebase -i A
```

Change all the commit you want to edit from `pick` to `edit`  
Change all the commit sequence by edit the rows   
Fix all the commit you want to merge to previous top `pick`, `pick` to `f`     
Squash merge all the commit to previous top `pick`, from `pick` to `s`   

```bash
  /* rebase list */
```
  -pick- edit 0972sefc12 commit message B
  -pick- edit 9032988sf0 commit message C
  ...
  pick 898ysifsid commit message E

```bash  
  $(master) git commit --amend --author="Author Name <email@address.com>"
  /* edit commit message of B */
  $(master) git rebase --continue  
  $(master) git commit --amend --author="Author Name <email@address.com>"
  /* edit commit message of C */
  $(master) git rebase --continue  
  $(master) git push -f origin master  
```

Merge squash the commit in local branch
```bash
  /* rebase list */
```
  pick 0972sefc12 commit message B
  -pick- s 9032988sf0 commit message C
  ...
  -pick- s 898ysifsid commit message E

=> Edit this next page for squash rebase  

```bash
* this is the first commit message
commit message B <& C>
-* this is the second commit message-
-Commit message C-
```

## remove  

To remove unused files.  

```bash
/* check current linked files */
$ git ls-files
```  

```bash
/* remove files */
$ git rm <files>

/* remove directories */
$ git rm -f <dir>
```

## reflog  

This is very power tool. You can force tracking on any commit you make in local branch  

```
$ git reflog
```

Then it will list all recent commit record for checkout / cherry-pick  

## revert  

On Public branch, sometimes you push some failed commit. One way to do it is to use revert command, as normally you are not able to do rebase, delete a commit on public remote branch.


```bash  
  commits 
  A-B-C-D-E(HEAD) (master)
      |-fail commit
```

In this case, you can simply use to push the revert commit.

```
$ git revert commit-C
$ git push 
```

## conflict  

There may be certain conflict during merging, one method is decide the conflict part.
With conflict branch `(merge|conflict)`, the files show conflict text
You have to select one by removing the extra text.
```
|<<<<<<<<<<<<<< commit @ sdf29dkossd 
+ print('hello world')

|>>>>>>>>>>>>>> commit @ 10ds99ddfcc
- print('hellow world')
+ print('I am good, thankyou')
```

One tip is to use powerful tool `vim diff <file1> <fil2>`  

More powerful tool is to use meld <directory>   
meld helps to fix conflicts  

$ sudo apt-get install meld 

## useful command  

* check all files in the branch  
```bash
  git ls-tree --full-tree -r HEAD
```

* to check all branches info
```bash
  gitk --all
```

* to fetch certain file in the branch
```
  git fetch
  git checkout -m <revision> <yourfilepath>
  git add <yourfilepath>
  git commit
```

* to checkout certain file in some branch  
```
  git checkout <branch> -- <filepath>  
```  

* open graph tree  
```
  gitk --all
```  

* git diff
```python
  git diff <branch1> <branch2>
  git diff <branch1> -- <filepath1> <branch2> -- <filepath2> 
  
  # @: current HEAD, @^: one previous commit
  git diff @ @^ 

  # get name 
  git diff <branch1> <branch2> --name-only

  # get status only (with + and - cnt) 
  git diff <branch1> <branch2> -stat

```

* get remote  
```
  # get remote url
  git remote get-url {origin} --all
```  

## reference  

* extra.
  [emoji symbol for .md](https://gist.githubusercontent.com/AliMD/3344523/raw/6cb0a435ad52bcd7465ab786f18e511ce5089924/gistfile1.md)
 

## gitconfig  

gitconfig allow alias for git command and default control of user  
```python
# ~/.gitconfig
[filter "lfs"]
u smudge = git-lfs smudge -- %f
  process = git-lfs filter-process
  required = true
  clean = git-lfs clean -- %f
[user]
  name = Takchoi.Yu
  email = tcyu@umich.edu
[commit]
    template = ~/.gitmessage
[core]
    autocrlf = true # change to "input" if in linux
[push]
    default = simple
[alias]
    st = status
    ci = commit
    co = checkout
    br = branch
    rb = rebase
    lg = log --graph --abbrev-commit --decorate --date=relative --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)' --all -n 100
    df = difftool -y
    mg = mergetool -y
```

## gitmessage  

this is linked from gitconfig `[commit]` tag

```python
#
#
# Subject line >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
# Explain What and Why >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
# Append issue tracking information
#
#
``` 

## patch  

git patch allows to save commit to a text file and transfer to another repo without remote control.  

```
// create patch  
$ git format-patch <commit> --stdout > <filename>.patch

cd <another repo>
// apply patch
$ git am <patch>
```

## merge-repo  

reference link
https://www.vvse.com/blog/blog/2017/04/16/merge-git-repositories-into-a-new-repository-while-preserving-the-commit-history/

## repo  


## repo-intro  

repo tool is to manage multiple git projects together w.r.t. to project directories and git commit status.
The status file is stored in manifest.xml.  which also includes remote url, etc.

## forall   

common usage is as below, without proj-repo1, its default run on all repo projects

```
$ repo forall <proj-repo1> <proj-repo2> -pvc <cmd args 1 , 2 ... >
```

## sync  

repo sync with 4 jobs

```
$ repo sync j4 
```

repo sync and detach 

```
$ repo sync -d
```

## init  

init repo status

```
$ repo init -b <branch> -m <manifest path>  
```

## diff-repo  

compare difference on the repo

```
$ repo --no-pager forall -pc 'git cherry origin/release1.0 origin/feature-1' > feature-1_to_release1.0.20201015.cherry
$ cherry_diff feature-1_to_release1.0.20201015.cherry feature-1_to_release1.0.20201029.cherry > incremental.cherry
$ cherry_annotate incremental.cherry
```

## manifest  

generate manifest of current status 

```
repo manifest -r -o <snapshot file name>.xml
```

## status

Show all the repo git status 

```
$ repo status
```
## branch  

to show all branches state on the manifest

```
$ repo branch
```


