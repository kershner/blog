/**
 * hamburger-modified.js
 *
 * Mobile Menu Hamburger (modified)
 * =====================
 * A hamburger menu for mobile websites
 *
 * Created by Thomas Zinnbauer YMC AG  |  http://www.ymc.ch
 * Date: 21.05.13
 * Modified by Tyler Kershner | http://www.kershner.org
 * Date 8/7/2014
 */

jQuery(document).ready(function() {

    //Open the menu
    jQuery("#hamburger").click(function() {

        // Set the 'nav' class z-index to be above the images
		jQuery("nav").css("z-index", 21);
		
		//display a layer to disable clicking and scrolling on the content while menu is shown
        jQuery('#contentLayer').css('display', 'block');
		
		//disable all scrolling on mobile devices while menu is shown
        jQuery('#container').bind('touchmove', function(e){e.preventDefault()});

	});

    //close the menu
    jQuery("#contentLayer").click(function() {

        //enable all scrolling on mobile devices when menu is closed
        jQuery('#container').unbind('touchmove');
		
		// Set the z-index for nav back to 0 so it is hidden
		jQuery("nav").css("z-index", 0);
		
		// Hide the contentLayer so the button is clickable again
		jQuery('#contentLayer').css('display', 'none');
	});
});