$(function () {
  function get_weather(e) {
    $.getJSON($SCRIPT_ROOT + '/user/weather',{
        province: $('input[name="province"]').val(),
        city: $('input[name="city"]').val()
    },
      function (data) {
        var body = data[0]
        var tips = data[1]
        $('#degree').text(body.degree),
        $('#humidity').text(body.humidity),
        $('#weather').text(body.weather),
        $('#pressure').text(body.pressure),
        $('#tip1').text(tips.observe['1']),
        $('#tip2').text(tips.observe['0']);
      });
  };
  // 绑定click事件
  $('#wbtn').bind('click', get_weather);
});
$(document).ready(function() {
  $.getJSON($SCRIPT_ROOT + '/user/weather',{
        province: '浙江',
        city: '杭州'
    },
    function (data) {
        var body = data[0]
        var tips = data[1]
        $('input[name="province"]').val('浙江'),
        $('input[name="city"]').val('杭州'),
        $('#degree').text(body.degree),
        $('#humidity').text(body.humidity),
        $('#weather').text(body.weather),
        $('#pressure').text(body.pressure),
        $('#tip1').text(tips.observe['1']),
        $('#tip2').text(tips.observe['0']);
      });
 });   