## ToDo

### Immediate tasks
- resize table div to fit in the browser window without scroll
- stats page: developer filtered queries
- remove modal notice ~~fix guest's access to relevance in queries~~
- fix sorting by column
- highlight columns for roles

- fix permission problems from the .xlsx
- fix permission problems in the table controls
- reset cache when selecting different reports
- fix checkmarks appear unchecked when scrolling the report table

### Feats
- ~~completeness stats~~
- ~~add relevance flags to the form~~
- ~~add relevance stats and controls to the stat queries~~
- ~~new fields~~
- ~~new roles and revisit field perms~~
- ~~adjust perms for new roles and updated field perms~~
- ~~add internal number field~~
- ~~add 'status' and 'model' select fields~~
- ~~add dict field BKVP chip number~~ -- added, needs refinement
- ~~add economy note field~
- ~~add tech note field~~
- ~~add relevance stats to dashboard~~
- ~~translate filter table headers~~
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
- ~~hide module settings from unauthorised roles~~
- ~~access filters from dict screen > add a list of dict-filters~~
- consider using pulsarnpp mails for registering users
- re-number rows in query reports
- allow empty selection fields in query filter
- ~~process specialist = спец по тд~~
- check translations

### Bugs
- report data request query fires second time after ~1 min, main page is not generated before then (does not reproduce consistently). 
- ~~fix translations for moduleview headers~~

### Data
- ~~import all prepared products~~
- ~~import all employees~~
- ~~fix devs-cons import error, switch categories~~
- create users for all employees, use pulsar mail

### Low priority
- write install scripts to create appropriate employee groups, roles and permissions
- fix frappe table bugs (resizing not working, visual bug with the border higlight)
- make desktop-moduleview use categories from the database instead of hard-coded ones
- make fetch from work for all field types, not just Link
- make desktop-moduleview in-site editor
- implement correct Link field control (show data in the field, write ID)
- fix HACK with permission based on role name, use API bool function
- 