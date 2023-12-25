import pywikibot

# Define the site
site = pywikibot.Site()

# Define generator for all pages in the namespace 0 (main articles)
gen = site.allpages(namespace=0, filterredir=False)

def is_human(item):
    # Define the property for 'instance of' and the item for 'human'
    instance_of_property = 'P31'
    human_item = 'Q5'

    # Check if the item has 'instance of' property and if it's set to 'human'
    return item.claims.get(instance_of_property, [])[0].getTarget().id == human_item

def process_page(page):
    # Skip pages with a databox or bio template
    if "{{databox" in page.text or "{{bio" in page.text:
        return

    # Check if the page is linked to Wikidata
    item = pywikibot.ItemPage.fromPage(page)
    if not item.exists():
        return

    # Check if the subject is human and add the respective template
    if is_human(item):
        tag = "{{bio}}\n"
        
    else:
        tag = "{{databox}}\n"
        
    page.text = tag + page.text

    # Save changes
    print(f"adding {tag} to {page.title()}")
    page.save(summary="Adding bio/databox template based on Wikidata")
    

# Iterate over all pages and process them
for page in gen:
    try:
        process_page(page)
    except Exception as e:
        print(f"Error processing page {page.title()}: {e}")
