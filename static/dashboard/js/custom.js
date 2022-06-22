/** @format */
"use strict";

$(document).ready(function () {
  $("form.ajax").on("submit", function (event) {
    event.preventDefault();

    swal({
      title: "Proccessing...!",
      text: "Please wait",
      icon: "info",
      button: false,
    });

    let $this = $(this);
    let url = $this.attr("action");
    let method = $this.attr("method");
    // var data = $($this).serialize();

    $.ajax({
      type: method,
      url: url,
      dataType: "json",
      contentType: false,
      processData: false,
      data: new FormData(this),

      success: function (data) {
        // console.log("success //");
        if (data["status"] == "true") {
          if (data["swal_icon"]) {
            var swal_icon = data["swal_icon"];
          } else {
            var swal_icon = "success";
          }

          if (data["swal_title"]) {
            var swal_title = data["swal_title"];
          } else {
            var swal_title = "Success !";
          }

          if (data["swal_text"]) {
            var swal_text = data["swal_text"];
          } else {
            var swal_text = "Successfully Submited";
          }

          if (data["swal_button"]) {
            var swal_button = data["swal_button"];
          } else {
            var swal_button = "OK";
          }

          swal({
            title: swal_title,
            text: swal_text,
            icon: swal_icon,
            button: swal_button,
          }).then(function () {
            if (data["redirect_url"]) {
              console.log(data["redirect_url"])
              location.href = data["redirect_url"];
            }
            if (data["reLoad"]) {
              location.reload();
            }

            if (data["click_class"]) {
              $(data["click_class"]).click();
            }
          });
        } else {
            $this.find(".ajax-form-error").text(data["error_message"]);
            swal({
              title: "Try Again !",
              text: data["error_message"],
              icon: "warning",
              button: "OK",
            });
        }
      },
      error: function (data) {
        swal({
          title: "Try Again !",
          text: "something went wrong",
          icon: "warning",
          button: "OK",
        });
      },
    });
  });

  $(".check_username").keyup(function (event) {
    let $this = $(this);
    var url = $this.attr("data-url");
    var method = "GET";
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    let value = $this.val();
    if (value.length > 5) {
      let data = "q=" + value + "&csrfmiddlewaretoken=" + csrftoken;

      $.ajax({
        type: method,
        url: url,
        dataType: "json",
        contentType: false,
        processData: false,
        data: data,

        success: function (data) {
          if (data["status"] == "true") {
            $(".check_username_msg").hide();
            $(".check_username_msg.valid-feedback").show();
          } else {
            $(".check_username_msg").hide();
            $(".check_username_msg.invalid-feedback").show();
          }
        },
        error: function (data) {
          swal({
            title: "Try Again !",
            text: "something went wrong",
            icon: "warning",
            button: "OK",
          });
        },
      });
    } else {
      $(".check_username_msg").hide();
      $(".check_username_msg.invalid-feedback").show();
    }
  });
  // $(".search_and_view select").change(function () {
  //   let $this = $(this);
  //   let path = $this.parent(".search_and_view").attr("data-path") + $this.val();
  //   window.location = path;
  // });
});

$(document).ready(function () {

  
  var rooms;
  $("#create-customer-button").click(function () {
    $(".modal , .modal-backdrop").addClass("show");
    $(".modal , .modal-backdrop").removeClass("hide");
  });

  $(".check-room-availability").click(function () {
    // let room = $("#id_room").val();
    let checkin_date = $("#id_checkin_date").val();
    let checkout_date = $("#id_checkout_date").val();
    let $this = $(this);
    var url = $this.attr("data-url");
    
    var method = "GET";
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
    if (checkout_date >= checkin_date) {
      // let data = "room=" + room + "checkin=" + checkin_date + "checkout=" + checkout_date + "&csrfmiddlewaretoken=" + csrftoken;
      let data =
        "checkin=" +
        checkin_date +
        "&checkout=" +
        checkout_date +
        "&csrfmiddlewaretoken=" +
        csrftoken;
      $.ajax({
        type: method,
        url: url,
        dataType: "json",
        contentType: false,
        processData: false,
        data: data,

        success: function (data) {
          if (data["status"] == "true") {
            rooms = data["rooms"];
            let availableroom = 0 
            $("p.avail").removeClass("hide");
            $("table.avail ").removeClass("hide");
            let txt = ""
            $.each(data["rooms"], function(i, item) {
              // txt += item["room_type_title"] +"₹"+ item["price"] + "   : " + item["available_rooms"] + "<br />";
              if(item["available_rooms"]>0){
                      txt += "<tr class='text-success'> <td>"+item["room_type_title"]+"</td><td><b>"+"₹"+item["price"]+"</b></td><td>"+"   : "+item["available_rooms"]+"</td></tr>"
              }
              else{
                txt += "<tr class='text-muted'> <td>"+item["room_type_title"]+"</td><td><b>"+"₹"+item["price"]+"</b></td><td>"+"   : "+item["available_rooms"]+"</td></tr>"
                
              }
                    });
            $("#room-num").html(txt);
            

            // console.log(data["rooms"][0]["room_type_title"])
          } else {
            $(".check_username_msg").hide();
            $(".check_username_msg.invalid-feedback").show();
          }

  
        },
        error: function (data) {
          swal({
            title: "Try Again !",
            text: "something went wrong",
            icon: "warning",
            button: "OK",
          });
        },
      });
      // console.log(room,checkin_date,checkout_date)
    } else {
      swal({
        title: "Try Again !",
        text: "something went wrong",
        icon: "warning",
        button: "OK",
      });
    }



   

  });
  
  $(".modal .close").click(function () {
    $(".modal , .modal-backdrop").removeClass("show");
    $(".modal , .modal-backdrop").addClass("hide");
  });

  //checking room availablity
  $('#id_booked_room_formset-0-room').click(function () {
    var optionSelected = $(this);
    var valueSelected = optionSelected.val();

    console.log("valueSelected:",valueSelected)
      // console.log(rooms)
      $.each(rooms, function(i, item) {

        if (item["available_rooms"]>0){
          console.log("room available:",item["room_type_title"])
          if(valueSelected == item["room_type"]){
            item["available_rooms"]--;
            // console.log(valueSelected)
            // console.log(item["available_rooms"])
          }
        }
        else{
          // if rooms where not available
          var val =item["room_type"];
          $(`.selDiv option[value=${val}]`).hide();
        }
    });
  });
  
  //getting the extra bed
  $('.form_set_row input').change(function () {
    // console.log("child leaves")
    var optionSelected = $(this);
    let parent = optionSelected.parents('.form_set_row');

    // console.log("optionSelected:",optionSelected)

    let room = parent.find(".room_input").val();
    let adult = parent.find(".adult_input").val();
    let child = parent.find(".child_input").val();
    var url = "get-extra-bed";
    var method = "GET";
    let csrftoken = $("input[name='csrfmiddlewaretoken']").val();
   let data =
        "room=" +
        room +
        "&adult=" +
        adult +
        "&child=" +
        child +
        "&csrfmiddlewaretoken=" +
        csrftoken;
      $.ajax({
        type: method,
        url: url,
        dataType: "json",
        contentType: false,
        processData: false,
        data: data,

        success: function (data) {
          var extra_bed=0;
          if (data["status"] == "true") {
            extra_bed = data["extra_bed"];
            // $("p.avail").removeClass("hide");
            // $("p.avail ").addClass("show");
            // let txt = ""
            // console.log(extra_bed)
            parent.find(".extrabed_input").val(extra_bed);
            // console.log(data["rooms"][0]["room_type_title"])
          } else {

            extra_bed=0;
            parent.find(".extrabed_input").val(extra_bed);


          }

  
        },
        error: function (data) {
          swal({
            title: "Try Again !",
            text: "something went wrong",
            icon: "warning",
            button: "OK",
          });
        },
      });
      // console.log(room,checkin_date,checkout_date)
  });

  //get maximum no adults and children allowed
  
  $('#id_booked_room_formset-0-room').change(function () {
    // console.log("child leaves")
    var optionSelected = $(this);
    let parent = optionSelected.parents('.form_set_row');

    let room = parent.find(".room_input").val();

    var url = "admin/get-max-guests";

    var method = "GET";


   let data =
        "room=" +
        room 

      $.ajax({
        type: method,
        url: url,
        dataType: "json",
        contentType: false,
        processData: false,
        data: data,

        success: function (data) {
          var extra_bed=0;
          if (data["status"] == "true") {
            txt=""
            for(i=0;i<=data["max_adult"];i++){
              txt+=`<option>${i}</option>`
            }
            parent.find(".adult_input").html(txt);

            txt=""
            for(i=0;i<=data["max_child"];i++){
              txt+=`<option>${i}</option>`
            }
            parent.find(".child_input").html(txt);
            
          } else {
            // extra_bed=0;
            // parent.find(".extrabed_input").val(extra_bed);
          }
        },
      });
  });

  $(".printMe").click(function(){
    window.print();
  });
});
