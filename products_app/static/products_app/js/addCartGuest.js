$(document).ready(function(){
    cart = JSON.parse(getCookie('CookieCart'));
    
    if (cart != undefined){
        cartKeys = Object.keys(cart);
    
        for (i = 0; i < cartKeys.length; i++){
            document.getElementById( parseInt(cartKeys[i])).disabled = true;  
        }
    }

    $('.add-cart').click(function(){
        var id = $(this).attr('id');
        var title =  this.parentNode.children[0].innerText;
        var cart = JSON.parse(getCookie('CookieCart'));
        
        if (cart == undefined){
            document.cookie = 'CookieCart=' + JSON.stringify(cart={}) + ";domain=;path=/";
        }
        
        cart[' '+id] = {'quantity':1};
        document.cookie = 'CookieCart=' + JSON.stringify(cart) + ";domain=;path=/";  
        document.cookie = 'CookieTitle=' + JSON.stringify({'title':title}) + ";domain=;path=/"; 
    
        const array = window.location.href.split('/');
        
        if (array[array.length-2] == 'categories'){
            window.location.replace(window.location.href);
        }

        else {
            window.location.replace('http://127.0.0.1:8000/cart/');
        }
    });

    function getCookie(name){
        // Split cookie string and get all individual name=value pairs in an array
        var cookieArr = document.cookie.split(";");
    
        // Loop through the array elements
        for(var i = 0; i < cookieArr.length; i++) {
            var cookiePair = cookieArr[i].split("=");
    
            /* Removing whitespace at the beginning of the cookie name and compare it with the given string */
            if (name == cookiePair[0].trim()) {
                // Decode the cookie value and return
                return decodeURIComponent(cookiePair[1]);
            }
        }
    
        // Return null if not found
        return null;
    }
});