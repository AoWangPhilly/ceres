/** Credit to webdevtrick ( https://webdevtrick.com ) **/
/**
 * Latest Update: Added documentation
 * Name: function.js
 * Purpose: Allow dark mode to be toggled.
 * Version: 1.1 (Resetting name attributes) | quarter.week (git commit message)
 * Date: June 3, 2020
 * Contributors: Hung Do
**/

 var checkbox = document.querySelector('input[name=mode]');
 
        checkbox.addEventListener('change', function() {
            if(this.checked) {
                trans()
                document.documentElement.setAttribute('data-theme', 'dartheme')
            } else {
                trans()
                document.documentElement.setAttribute('data-theme', 'lighttheme')
            }
        })
 
        let trans = () => {
            document.documentElement.classList.add('transition');
            window.setTimeout(() => {
                document.documentElement.classList.remove('transition');
            }, 1000)
        }