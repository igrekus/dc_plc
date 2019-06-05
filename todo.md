## ToDo

### Feats
- ~~add internal number field~~
- ~~add 'status' and 'model' select fields~~
- ~~add dict field BKVP chip number~~ -- added, needs refinement
- ~~add economy note field~
- ~~add tech note field~~
- add reference to device cost when costing is complete
- ~~add design documentation data field~~
- fit table rows
- ~~draw title on link type fields~~
- forbid file attachment if not explicitly allowed
- ~~forbid sharing if not allowed~~
- implement titles in link fields:
   https://gist.github.com/paurosello/da635c831b0c5560c74ea8ab2a2906ad
   https://github.com/mxmo-co/title_links
- ~~fix translation for link field title hack~~
- ~~disable chat in prod~~
- ~~import live data~~
- hide module settings from unauthorised roles
- ~~access filters from dict screen > add a list of dict-filters~~
- consider using pulsarnpp mails for registering users
- re-number rows in query reports
- allow empty selection fields in query filter

### Bugs
- report data request query fires second time after ~1 min, main page is not generated before then (does not reproduce consistently). 

### Low priority
- write install scripts to create appropriate employee groups, roles and permissions
- fix frappe table bugs (resizing not working, visual bug with the border higlight)
- make desktop-moduleview use categories from the database instead of hard-coded ones
- make desktop-moduleview in-site editor
- 