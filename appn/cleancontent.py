def clean(content):
	listtodelete=['hideInCourse','clear hideIt','personalNoteHeader clear','noteHeaderText','hideNotesDivIcon','collapsableDivPersonalNotes','recommendedPostsDiv',]
	for i in listtodelete:
		elems=content.find('div',class_=i)
		if elems:
			elems.decompose()
	some=content.find_all('i',class_='material-icons')
	for i in some:
		i.decompose()
	banner=content.find_all('a')
	for j in banner:
		p=j.get('href')
		if p!=None and 'utm_medium=banner' in p:
			j.decompose()
	elems=content.find_all('div')
	for i in elems:
		p=i.get('id')
		if p!=None and 'AP_G4GR_' in p:
			i.decompose()
	rem=content.find(id='improvedBy')
	if rem:
		rem.decompose()
	return content
	# banner=content.find('img',{'class':'ad_course_banner'})
	# if banner:
	# 	banner.decompose()