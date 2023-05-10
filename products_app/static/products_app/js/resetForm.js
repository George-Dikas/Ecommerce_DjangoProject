// When User closes Profile and Password Forms without submitting

$(document).ready(function(){
    $('.btn-close').click(function(){
        $('#updateProfile').trigger('reset');
        $('#updatePassword').trigger('reset');
    });
});