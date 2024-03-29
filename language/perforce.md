## Perforce

Perforce is a version control tool which differ to git.
Perforce use centralized server to hold the file history and branch. While user only keeps files without any file history.
Instead, client(user) query all information from server side. Example.
Checkout code, Checkin code, shelve files, view files history, etc.

* check out

* sync

`p4 sync`

* create change list

`p4 change`

* edit change list

`p4 change -u <cl>`

* shelve

`p4 shelve -c <cl>`

* re-shelve

similar to git stash

`p4 shelve -r -c <cl>`

* unshelve

`p4 unshelve -s <cl>`

* list shelve in client

`p4 changes --me -s shelved`

* rm repo

```
p4 clients -u <user>
p4 client -d <client>
rm -rf repo
```

* publish to reviewboard

```
# publish and create review id
rbt post --target-people="<name>,<name>,..." --target-groups="XXXX" -p <cl>

# update cl to review id
rbt post --target-people="<name>,<name>,..." --target-groups="XXXX" -r <review id> -p <cl>
```

* check in

`p4ci -dft -partial <ccr> -cr <reviewid> -cl <changelist> [-reg dft.series]`

* update flie in the changelist

```
# reopen all edited files
p4 reopen -c <cl> -Si //...
 
# reopen for specific files
p4 reopen -c <cl> -Si <file1> <file2>
```
* patch

reference : https://stackoverflow.com/questions/9429589/how-to-apply-a-perforce-patch

```
unsetenv P4DIFF
p4 diff <f0> <f1> ... > patch.diff
sed -Ee 's|==== (//.*)#[0-9]+(.*)|+++ \1\n--- \1|' < patch.diff > patch
patch -p4 -l < patch
setenv P4DIFF vimdiff
```

* edit p4 client info

```
# output client info to stdout
p4 client -o > a.spec

# edit the info
vi a.spec

# input client info to stdin
p4 client -i < a.spec
```

