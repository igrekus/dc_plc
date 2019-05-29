### Feats
1. <s>add internal number field</s>
2. <s>add 'status' and 'model' select fields</s>
3. <s>add dict field BKVP chip number</s> -- added, needs refinement
4. <s>add economy note field</s>
5. <s>add tech note field</s>
6. add reference to device cost when costing is complete
7. add design documentation data field

### Bugs
1. report data request query fires second time after ~1 min, main page is not generated before then (does not reproduce consistently). 

### UI
1. fit table rows
2. <s>draw title on link type fields</s>
3. forbid file attachment if not explicitly allowed
4. <s>forbid sharing if not allowed</s>
5. implement titles in link fields:
   https://gist.github.com/paurosello/da635c831b0c5560c74ea8ab2a2906ad
   https://github.com/mxmo-co/title_links
6. <s>fix translation for link field title hack</s>

### Misc
1. <s>disable chat in prod</s>
2. import live data

# Low priority
1. write install scripts to create appropriate employee groups, roles and permissions

### Guidelines
1. Strip users of most hand-entry possibilities to avoid inconsistencies
