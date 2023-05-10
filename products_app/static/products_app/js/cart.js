$(document).ready(function(){
    $('.minus-quantinty').click(function(){
        var id = $(this).attr('pid');
        var qty = this.parentNode.children[1];
        var total_cost = this.parentNode.nextElementSibling;
        var amount_bef = $('.amount').text().replace(' €','');

        $.ajax({
            type:'GET',
            url: '/cart/minusQuantity',
            data:{cartbook_id:id, amount_bef:amount_bef},

            success:function(data){ 
                if (Object.keys(data).length){
                    qty.innerText = data.quantity;
                    total_cost.innerText = data.total_cost + ' €';
                    $('.amount').text(data.amount + ' €');
                    $('.total_amount').text(data.total_amount + ' €');  

                    if(data.user == 'anonymous'){
                        cart = JSON.parse(getCookie('CookieCart'));
                        cart[id]['quantity'] -=1;
                        document.cookie ='CookieCart=' + JSON.stringify(cart) + ";domain=;path=/";
                    }
                }
            }
        })
    });

    $('.plus-quantity').click(function(){
        var id = $(this).attr('pid');
        var qty = this.parentNode.children[1];
        var total_cost = this.parentNode.nextElementSibling;
        var amount_bef = $('.amount').text().replace(' €','');

        $.ajax({
            type:'GET',
            url: '/cart/plusQuantity',
            data:{cartbook_id:id, amount_bef:amount_bef},
            
            success:function(data){ 
                qty.innerText = data.quantity;
                total_cost.innerText = data.total_cost + ' €';
                $('.amount').text(data.amount + ' €');
                $('.total_amount').text(data.total_amount + ' €');  
                
                if(data.user == 'anonymous'){
                    cart = JSON.parse(getCookie('CookieCart'));
                    cart[id]['quantity'] +=1;
                    document.cookie ='CookieCart=' + JSON.stringify(cart) + ";domain=;path=/";
                }
            }
        }) 
    });

    $('.remove-cart').click(function(){
        var id = $(this).attr('id');
        var qty = this.parentNode.children[1].innerText;
        var del_btn = this;
        var amount_bef = $('.amount').text().replace(' €','');
        
        $.ajax({
            type:'GET',
            url: '/cart/removeCart',
            data:{cartbook_id:id, amount_bef:amount_bef, quantity:qty},
            
            success:function(data){ 
                if(data.user == 'anonymous'){
                    cart = JSON.parse(getCookie('CookieCart'));
                    delete cart[id];
                    document.cookie ='CookieCart=' + JSON.stringify(cart) + ";domain=;path=/";
                }
                
                $('.cartNum').text(data.cartnum);
                $('.amount').text(data.amount + ' €');

                if (data.amount == 0){
                    $('.amount').text(0 + ' €');
                    $('.shipping').text(0 + ' €');
                    $('.checkout').addClass('disabled');
                }

                $('.total_amount').text(data.total_amount + ' €');   
                del_btn.parentNode.parentNode.remove();
                
                $('div').filter('#warning').remove();
                $('div').filter('#success').remove();

                $('.content').prepend('<div class="alert alert-warning alert-dismissible fade show" id="warning" role="alert">' +
                data.message +
                '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
                
                $('div').filter('#warning').fadeOut(10000);
            }
        }) 
    });

    function getCookie(name) {
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