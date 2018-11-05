# git-note

## content table
- **[git initalize config](#inital-config)**
- **[branches management](#branches-management)**
- **[merge branch](#merge-branch)**
- **[tagging](#tagging)**  
- **[conflict](#conflict)**  
- **[useful command](#useful-command)**
- **[reference](#reference)**

## inital config  
* check git current username 
```bash
  git config --list | grep -a 
```
  
* setup git user 
```bash
  git config --global user.name "Alvin J. Alexander"
  git config --global user.emal addr@emal.com
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
  git checkout <branchname> -* <filename>
```
  
* checkout to new branch 
```bash
  git checkout -b <new branch> <src branch>
```

* fetch (safely copy the new file from branch)
```bash
  git fetch <branch>
```

* check the git history 
```bash
  git log <--stat> <commit-id>

  git status <commit-id>

  git diff <commit-id> <commit-id>

  git diff <branch name>
```

* merge master branch ex. 
```bash
  git checkout master

  git pull

  git checkout <test>

  git pull

  git rebase -i master

  git checkout master

  git merge <test>
```
 
 :x: avoid operatio: never use rebase on public branch 
```bash
  git checkout master

  git rebase -i test
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
  git fetch origin develop
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

## tagging  

tagging is to mapping the commit ID to self-defined tag name  
[ref](https://stackoverflow.com/questions/5195859/how-do-you-push-a-tag-to-a-remote-repository-using-git/26438076#26438076)

* add tag to local  
  `at local (master)`  
```bash
  (master) git tag v1.0.0
  (master) git tag 
          v1.0.0
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
```
  git diff <branch1> <branch2>
  git diff <branch1> -- <filepath1> <branch2> -- <filepath2> 
  git diff @ @^ # @: current HEAD, @^: one previous commit
```

## reference  

* extra.
  [emoji symbol for .md](https://gist.githubusercontent.com/AliMD/3344523/raw/6cb0a435ad52bcd7465ab786f18e511ce5089924/gistfile1.md)
 


