$(document).ready(function() {
    /*  Selects all elements matched by <input> that have a name value exactly equal to 
    username.*/
    // alert(window.location.pathname)
    // if (window.location.pathname == "/admin/app1/user/add/" || window.location.pathname == "/admin/app1/user/12/change/") {
    $(".field-description").slice(0)
    $("input[name='_addanother']").css("display", "none");
    $("input[name='_continue']").css("display", "none");
    $(".btn btn-outline-danger form-control").css("display", "none")
        // }
    $(".nav-header").text('Core Modules').css("background-color", "cornflowerblue");
    $(".btn btn-primary btn-xs").css("align", "right")
        // $(".sidebar").text('Core Modules').css("background-color", "white");
        // $(".nav-icon fas fa-circle").css("color", "cornflowerblue");

    // testPath = location.pathname;
    // if (testPath.includes("/test/")) {

    //     var ht = `<div class="row">
    //     <div class="customer_records">
    //       <input name="customer_name" id="city" type="text" placeholder="City">
    //       <input name="customer_age" type="text" placeholder="Price">
    //       <a class="extra-fields-customer" href="#">Add City</a>
    //     </div>

    //  <div class="customer_records_dynamic">

    //  </div>

    //   </div>`;
    //     $(".card-body").append(ht);


    // } else {
    //     console.log("The word Example is not in the string.");
    // }






    // $('.extra-fields-customer').click(function() {
    //     $('.customer_records').clone().appendTo('.customer_records_dynamic');
    //     $('.customer_records_dynamic .customer_records').addClass('single remove');
    //     $('.single .extra-fields-customer').remove();
    //     $('.single').append('<a href="#" class="remove-field btn-remove-customer">Remove Customer</a>');
    //     $('.customer_records_dynamic > .single').attr("class", "remove");

    //     $('.customer_records_dynamic input').each(function() {
    //         var count = 0;
    //         var fieldname = $(this).attr("name");
    //         $(this).attr('name', fieldname + count);
    //         count++;
    //     });

    // });

    // $(document).on('click', '.remove-field', function(e) {
    //     $(this).parent('.remove').remove();
    //     e.preventDefault();
    // });




});