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

    var testPath = location.pathname;
    if (testPath.includes("/delete/")) {
        $(".col-sm-9").css("display", "none")
    }
    if (testPath.includes("/user/")) {
        if (testPath.includes("/change/")) {
            $(".btn-outline-danger").css("display", "none");

        }
    }
    if (testPath.includes("/test/")) {
        // alert("ok")
        if (testPath.includes("/change/")) {
            // var parent = $(".col-lg-9:nth-child(1)").attr("class");
            var ht = `<div class="row">
        <div class="customer_records">
          <select name="cars" id="cityselect">
            </select>
          <input name="customer_age" type="text" placeholder="Price">
          <a class="extra-fields-customer" href="#">Add City</a>
        </div>

     <div class="customer_records_dynamic">

     </div>
      </div>`;
            // $(".card-body").append(ht);
            // $(".card-body").closest(".col-lg-9").append(ht);
            // var quantity = $(this).closest('.col-lg-9').find('.card-outline');
            // $(quantity).append(ht);
            // console.log(quantity)
        } else if (testPath.includes("/test/add")) {
            console.log("ok")
            var htt = `<div class="row">
            <div class="customer_records">
              <select name="cars" id="cityselect">
            </select>
              <input name="customer_age" type="text" placeholder="Price">
              <a class="extra-fields-customer" href="#">Add City</a>
            </div>
    
         <div class="customer_records_dynamic">
    
         </div>
          </div>`;
            // $(".card-outline").append(htt);
            // $(".card-body").closest(".col-lg-9").append(htt);
            // $(".card-body").append(htt);
        }
    } else {
        console.log("ok")
    }
    $('.extra-fields-customer').click(function() {
        $('.customer_records').clone().appendTo('.customer_records_dynamic');
        $('.customer_records_dynamic .customer_records').addClass('single remove');
        $('.single .extra-fields-customer').remove();
        $('.single').append('<a href="#" class="remove-field btn-remove-customer">Remove city</a>');
        $('.customer_records_dynamic > .single').attr("class", "remove");
        $('.customer_records_dynamic input').each(function() {
            var count = 0;
            var fieldname = $(this).attr("name");
            $(this).attr('name', fieldname + count);
        });
    });
    $(document).on('click', '.remove-field', function(e) {
        $(this).parent('.remove').remove();
        e.preventDefault();
    });
    // $.getJSON("/city", function(j) {
    //    console.log(j)
    //    $.each(j, function(i, n) {
    // console.log(i, n);
    //      optionText = i;
    //     optionValue = n;
    // $('#cityselect').append(new Option(optionValue.value, optionText));
    // $('#cityselect').append(`<option value="${optionText}">
    //                            ${optionValue}
    //                       </option>`);
    // });
    // });
});