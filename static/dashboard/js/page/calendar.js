
var today = new Date();
year = today.getFullYear();
month = today.getMonth();
day = today.getDate();

$(document).ready(function () {
  let data =
   
  $.ajax({
    type: "get",
    url: "dashboard-calender",
    dataType: "json",
    contentType: false,
    processData: false,
    data: "month=" + month +"&year=" + year ,

  });

});
var calendar = $('#myEvent').fullCalendar({
  height: 'auto',
  defaultView: 'month',
  editable: true,
  selectable: true,
  header: {
    left: 'prev,next today',
    center: 'title',
    right: 'month,agendaWeek,agendaDay,listMonth'
  },
  events: [{
    title: "Palak Janisssssssssssss",
    start: new Date(year, month, 01),
    end: new Date(year, month, 02),
    backgroundColor: "#00bcd4",
    url: 'http://google.com/'
  },{
    title: "Palak 0002",
    start: new Date(year, month, 02, 11, 30),
    end: new Date(year, month, 02, 12, 00),
    backgroundColor: "#00bcd4"
  }, {
    title: "Priya Sarma",
    start: new Date(year, month, day, 13, 30),
    end: new Date(year, month, day, 14, 00),
    backgroundColor: "#fe9701"
  }, ]
});

/*$("#myEvent").fullCalendar({
  height: 'auto',
  header: {
    left: 'prev,next today',
    center: 'title',
    right: 'month,agendaWeek,agendaDay,listWeek'
  },
  editable: true,
  events: [
    {
      title: 'Conference',
      start: '2018-01-9',
      end: '2018-01-11',
      backgroundColor: "#fff",
      borderColor: "#fff",
      textColor: '#000'
    },
    {
      title: "John's Birthday",
      start: '2018-01-14',
      backgroundColor: "#007bff",
      borderColor: "#007bff",
      textColor: '#fff'
    },
    {
      title: 'Reporting',
      start: '2018-01-10T11:30:00',
      backgroundColor: "#f56954",
      borderColor: "#f56954",
      textColor: '#fff'
    },
    {
      title: 'Starting New Project',
      start: '2018-01-11',
      backgroundColor: "#ffc107",
      borderColor: "#ffc107",
      textColor: '#fff'
    },
    {
      title: 'Social Distortion Concert',
      start: '2018-01-24',
      end: '2018-01-27',
      backgroundColor: "#000",
      borderColor: "#000",
      textColor: '#fff'
    },
    {
      title: 'Lunch',
      start: '2018-01-24T13:15:00',
      backgroundColor: "#fff",
      borderColor: "#fff",
      textColor: '#000',
    },
    {
      title: 'Company Trip',
      start: '2018-01-28',
      end: '2018-01-31',
      backgroundColor: "#fff",
      borderColor: "#fff",
      textColor: '#000',
    },
  ]

});
*/