# lowcarbonresearchmethods
An energy efficient design for the website of the Low Carbon Research Methods group

This code based is not managed by Anne Pasek -> https://github.com/aepasek/lowcarbonresearchmethods

## Updating Pages

<p>
	<strong>Edits to the content of HTML and CSS pages should be made on the files in the templates directory.</strong> When the static site generator updates the data on the page it takes the template pages, updates the variables, and outputs them into the root directory. Edits made to the files in the root directory will be overwritten when the page data is updated.
</p>

<p>
	Most normal updates will likely happen between the `<!-- UPDATE TO HERE-->` and `<!-- UPDATE TO HERE-->`
</p>

### Prominent CSS Elements

`<div class="contentItem">`
* This is primary design element used in the content of the pages.
* A big block of content with a grey background. 
* h2 elements within a contentItem class are underlined.

`<div class="profile">`
* All profiles are placed within a profile container

`<video controls preload="none">
    <source src="assets/Johan.mp4" type="video/mp4">
    Sorry, your browser doesn't support embedded videos, but you can <a href="assets/Johan.mp4">download it here.</a>
</video>`
* Use this video syntax to avoid preloading/ autoloading


## Installation

<p>
	Navigate to lowcarbonmethods direction (cd local/www from the pi interface) and run this code to pull latest directory:
	`git pull origin main`
