$(document).ready(function () {

      $('#id_booked_room_formset-0-room').change(function () {
        // console.log("child leaves")
        var optionSelected = $(this);
        let parent = optionSelected.parents('.form_set_row');
    
        // console.log("optionSelected:",optionSelected)
        
        let room = parent.find(".room_input").val();
        var roomtxt= parent.find(".room_input option:selected" ).text();

        let checkin_date = $("#id_checkin_date").val();
        let checkout_date = $("#id_checkout_date").val();

        if(checkin_date < checkout_date){

          $.ajax({
            type: "GET",
            url: "check-room-availabilty-web",
            dataType: "json",
            contentType: false,
            processData: false,
            data:  "room=" + room + "&checkin=" + checkin_date + "&checkout=" + checkout_date ,
  
            success: function (data) {
              if (data["status"] == "True") {
                $("#room-availablity").addClass("hide");
                $("#room-availablity").removeClass("show");
  
                $.ajax({
                  type: "GET",
                  url: "admin/get-max-guests",
                  dataType: "json",
                  contentType: false,
                  processData: false,
                  data:  "room=" + room ,
          
                  success: function (data) {
                    var extra_bed=0;
                    if (data["status"] == "true") {
                      txt=""
                      for(i=1;i<=data["max_adult"];i++){
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
              }
              else{
                $("#room-availablity").html(roomtxt +" is not Available");
                // console.log($("#room-availablity").text());
                $("#room-availablity").removeClass("hide");
                $("#room-availablity").addClass("show");
                parent.find(".adult_input").html("");
                parent.find(".child_input").html("");
                
              }
              
            },
  
          });
        }



      });


        
});
