# markdown note

* **content table  
-- [header](#header)  
-- [link](#link)  
-- [collapse](#collapse)  
-- [font](#font)**  

## header  
```python
# header  
## header  
### header  
#### header  
* header  
** header  
**** header  
- header  
-- header  
--- header  
be reminded to have two spaces after line to prompt new line
```

# header  
## header  
### header  
#### header  
* header  
** header  
**** header  
- header  
-- header  
--- header 

## link  
```python
-- [header](#header)  
-- [link](#link)  
-- [collapse](#collapse)  
-- [font](#font)  or even topic in file path  
-- [img](../files/imagelist.md#blob)
```
- [header](#header)    
- [collapse](#collapse)  
- [font](#font)    
- [img](../files/imagelist.md#blob)  

## collapse
```python
<details><summary>CLICK ME</summary>
<p>

#### yes, even hidden code blocks!

` ``python
print("hello world!")
` ``
</p>
</details>
```
<details><summary>CLICK ME</summary>
`yes, even hidden code blocks!`  
```python
print("hello world!")
```
</details>

## font

* font style  
`**hello**`  `*hello*` `_hello_`  
**hello**  *hello* _hello_  

* coloring
```python
<p>Some Markdown text with <span style="color:blue">some <em>blue</em> text</span>.</p>
Some Markdown text with <span style="color:blue">some *blue* text</span>.
Some Markdown text with <span style="color:green">some *blue* text</span>.
Some Markdown text with <span style="color:red">some *blue* text</span>.
```
<p>Some Markdown text with <span style="color:blue">some <em>blue</em> text</span>.</p>
Some Markdown text with <span style="color:blue">some *blue* text</span>.  
Some Markdown text with <span style="color:green">some *blue* text</span>.  
Some Markdown text with <span style="color:red">some *blue* text</span>.  