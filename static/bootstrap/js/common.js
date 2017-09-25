/*
初始化表格
*/
$(function(){
    $("#table_id").DataTable({
    "bSort": false,
    "bAutoWidth": true,
    "language": {
        "processing": "处理中...",
        "lengthMenu": "显示 _MENU_ 项结果",
        "zeroRecords": "没有匹配结果",
        "info": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
        "infoEmpty": "显示第 0 至 0 项结果，共 0 项",
        "infoFiltered": "(由 _MAX_ 项结果过滤)",
        "infoPostFix": "",
        "search": "搜索:",
        "searchPlaceholder": "搜索...",
        "url": "",
        "emptyTable": "表中数据为空",
        "loadingRecords": "载入中...",
        "infoThousands": ",",
        "paginate": {
            "first": "首页",
            "previous": "上页",
            "next": "下页",
            "last": "末页"
        },
        "aria": {
            paginate: {
                first: '首页',
                previous: '上页',
                next: '下页',
                last: '末页'
            },
            "sortAscending": ": 以升序排列此列",
            "sortDescending": ": 以降序排列此列"
        },
        "decimal": "-",
        "thousands": "."
    }
}
    );

  })


//关闭时清空模态窗数据


$(function(){
        $("#add_apiModal").on("hidden.bs.modal", function() {
        $("#select").val("");
        $("#apiname").val("");
        $("#apidescribe").val("");
        $("#apiurl").val("");
        $("#app_sel").val("");
        $("#page_sel").val("");
        $("#add_apiForm").data('bootstrapValidator').destroy();
        $("#add_apiForm").data('bootstrapValidator',null);
        formValidator();

    });

    })

$(function(){
        $("#edit_apiModal").on("hidden.bs.modal", function() {
        $("#apiname").val("");
        $("#apidescribe").val("");
        $("#apiurl").val("");
        $("#edit_apiForm").data('bootstrapValidator').destroy();
        $("#edit_apiForm").data('bootstrapValidator',null);
        formValidator();


    });
    })

$(function(){
        $("#add_appModal").on("hidden.bs.modal", function() {
        $("#appname").val("");
        $("#add_appForm").data('bootstrapValidator').destroy();
        $("#add_appForm").data('bootstrapValidator',null);
        formValidator();

    });

    })

$(function(){
        $("#add_pageModal").on("hidden.bs.modal", function() {
        $("#pagename").val("");
        $("#app_sel").val("");
        $("#add_pageForm").data('bootstrapValidator').destroy();
        $("#add_pageForm").data('bootstrapValidator',null);
        formValidator();

    });

    })
/*
$(function(){

    })

$(function(){

    })
    */
/*
读取一行数据
*/

function show_api(obj){
      var tds= $(obj).parent().parent().find('td');
      $('#id2').val(tds.eq(0).text());

      $('#apiname2').val(tds.eq(1).text());

      $('#apidescribe2').val(tds.eq(3).text());

      $('#apiurl2').val(tds.eq(2).text());

      $('#apicount2').val(tds.eq(4).text());

      $('#appid2').val(tds.eq(8).text());

      $('#pageid2').val(tds.eq(9).text());
      var content1='<option value='+'>'+tds.eq(10).text()+'</option>';
      var content2='<option value='+'>'+tds.eq(11).text()+'</option>';
      $('#app_sel2').html(content1);
      $('#page_sel2').html(content2);

      $('#edit_apiModal').modal('show');

}

function show_case(obj){
      var tds= $(obj).parent().parent().find('td');
      $('#id2').val(tds.eq(0).text());
      $('#apiname2').val(tds.eq(1).text());
      $('#casename2').val(tds.eq(2).text());
      $('#apiurl2').val(tds.eq(7).text());
      $('#inparam2').val(tds.eq(4).text());

      $('#header2').val(tds.eq(3).text());

      $('#expect2').val(tds.eq(5).text());

      $('#edit_caseModal').modal('show');

}


function show_app(obj){
      var tds= $(obj).parent().parent().find('td');
      $('#appid2').val(tds.eq(0).text());
      $('#appname2').val(tds.eq(1).text());


      $('#edit_appModal').modal('show');

}

function show_page(obj){
      var tds= $(obj).parent().parent().find('td');
      $('#pageid2').val(tds.eq(1).text());
      $('#pagename2').val(tds.eq(3).text());


      $('#edit_pageModal').modal('show');

}

function show_response(obj){
      var tds= $(obj).parent().parent().find('td');
      //$('#id3').val(tds.eq(0).text());
      //$('#response').val(tds.eq(6).text());
      var modal = $(this)
      modal.find('.modal-body input').val('23434234')
      $('#show_responseModal').modal('show');

}

function show_response2(obj){
      var id= $(obj).attr('id');
      alert(id);
     $('#caseid').val(id);
     $('#apiname').val($(obj).find('td').eq(6).text());
      //a=$('#response').val($(obj).find('td').eq(6).text());
     // a=a+$('#response').val($(obj).find('td').eq(4).text());


      $('#show_response2Modal').modal('show');

}




//绑定change事件，当下拉框内容发生变化时启动事件
$("#app_sel").bind("change",function(){
        var sel = $(this).find("option:selected").val();
        //alert(sel);
        //向input输入框中赋值
        $("#appid").val(sel);

    });

$("#app_sel2").bind("change",function(){
        var sel = $(this).find("option:selected").val();

        alert(sel);
        //向input输入框中赋值
        $("#appid2").val(sel);

    });

$("#page_sel").bind("change",function(){
        var sel = $(this).find("option:selected").val();
        //向input输入框中赋值

        $("#pageid").val(sel);
    });


$("#page_sel2").bind("change",function(){
        var sel = $(this).find("option:selected").val();
        //向input输入框中赋值
        alert(sel);
        $("#pageid2").val(sel);
    });

$("#app_sel").bind("click",function(){
        var id = $('#app_sel').find("option:selected").val();
        var content='<option selected value="">请选择位置</option>';
        $('#page_sel').html(content);
        $.getJSON("/get_page_data/"+id+"/", function(data,textStatus){
        $.each(data, function(i, item){
           content+='<option value='+item.pk+'>'+item.fields.page_name+'</option>'
                });
           $('#page_sel').html(content);
         });
    });


$("#app_sel2").bind("click",function(){
        var id = $('#appid2').val();
        content1='<option value="">请选择APP</option>';
        $.getJSON("/get_app_data/", function(data,textStatus){
        $.each(data, function(i, item){
           content1+='<option value='+item.pk+'>'+item.fields.app_name+'</option>'
                });
              //alert(content1);
              $('#app_sel2').html(content1);
         });
        content2='<option value="">请选择位置</option>';
        $.getJSON("/get_page_data/"+id+"/", function(data,textStatus){
        $.each(data, function(i, item){
           content2+='<option value='+item.pk+'>'+item.fields.page_name+'</option>'
                });
           $('#page_sel2').html(content2);
         });
    });


$("#select").bind("change",function(){
        var sel = $(this).find("option:selected").val();
        //向input输入框中赋值
        $("#apiid").val(sel);
    });


$(function () {

        $('form').bootstrapValidator({
            message: 'This value is not valid',
            feedbackIcons: {
                valid: 'glyphicon',
                invalid: 'glyphicon glyphicon-remove',
                validating: 'glyphicon glyphicon-refresh'
            },
            fields: {
                apiname: {
                    message: '验证失败',
                    validators: {
                        notEmpty: {
                            message: '不能为空'
                        },
                        stringLength: {
                            min: 4,

                            message: '长度必须大于4个字符'
                        },

                    }
                },
                apidescribe: {
                    validators: {
                        notEmpty: {
                            message: '描述不能为空'
                        },
                        stringLength: {
                            min: 4,
                            message: '长度必须大于4个字符'
                        },
                    }
                },
                apiurl: {
                    message: '验证失败',
                    validators: {
                        notEmpty: {
                            message: '不能为空'
                        },
                        stringLength: {
                            min: 4,
                            message: '长度必须大于4个字符'
                        },
                        regexp: {
                            regexp: /^((ht|f)tps?):\/\/[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&:\/~\+#]*[\w\-\@?^=%&\/~\+#])?$/,
                            message: '请以http://或https://开头'
                        }
                    }
                },
                select: {
                    message: '验证失败',
                    validators: {
                        notEmpty: {
                            message: '不能为空'
                        }

                    }
                },

                select2: {
                    message: '验证失败',
                    validators: {
                        notEmpty: {
                            message: '不能为空'
                        }

                    }
                },


                casename: {
                    message: '验证失败',
                    validators: {
                        notEmpty: {
                            message: '不能为空'
                        }

                    },
                        stringLength: {
                            min: 4,
                            message: '长度必须大于4个字符'
                        }
                },

                appname: {
                    message: '验证失败',
                    validators: {
                        notEmpty: {
                            message: '不能为空'
                        }

                    },
                        stringLength: {
                            min: 4,
                            message: '长度必须大于4个字符'
                        }
                },
                pagename: {
                    message: '验证失败',
                    validators: {
                        notEmpty: {
                            message: '不能为空'
                        }

                    },
                        stringLength: {
                            min: 4,
                            message: '长度必须大于4个字符'
                        }
                },


            },

            submitHandler: function (validator, form, submitButton) {
                alert("submit");
            }
        });
    })



$(".case_run").click(function(){
        var id = $(this).attr("case_id");
           $.ajax({
            type: "POST",
            url: "/run_api_case/",
            async: false,
            dataType:"json",
            data:{id:id},
            beforeSend: function (xhr, settings) {
            var csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {xhr.setRequestHeader("X-CSRFToken", csrftoken);}},
            success: function(data) {
                swal("执行完成！", "", "success");
                t=$("#apicase_"+id);
                if(data["status"]==0){
                t.children('td').eq(8).html("<span class=\"label label-danger\">失败</span>");
                 }
                else{
                t.children('td').eq(8).html("<span class=\"label label-success\">通过</span>");
                }

                t.children('td').eq(9).html(data["eltime"]+"ms");
                t.children('td').eq(10).html(data["extime"]);

                 }
        });
        });
$(".cases_run").click(function(){
        var id = $(this).attr("api_id");
            $.ajax({
            type: "POST",
            url: "/run_api/",
            async: false,
            dataType:"json",
            data:{id:id},
            beforeSend: function (xhr, settings) {
            var csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {xhr.setRequestHeader("X-CSRFToken", csrftoken);}},
            success: function(data) {
                swal("执行完成！", "", "success");
                t=$("#api_"+id);
                if(data["status"]==0){
                t.children('td').eq(5).html("<span class=\"label label-danger\">失败</span>");
                 }
                else{
                t.children('td').eq(5).html("<span class=\"label label-success\">通过</span>");
                }

                t.children('td').eq(6).html(data["eltime"]+"ms");
                t.children('td').eq(7).html(data["extime"]);

                 }
        });
        });
$("#edit_api").click(function (){
        var id = $('#id2').val();
        var apiname = $('#apiname2').val();
        var apidescribe = $('#apidescribe2').val();
        var apiurl = $('#apiurl2').val();
        var appid = $('#appid2').val();
        //alert(appid);
        var pageid= $('#pageid2').val();
        //alert(pageid);
        $.ajax({
            type: "post",
            url: "/edit_api/",
            async: false,
            data:{id:id,apiname:apiname,apidescribe:apidescribe,apiurl:apiurl,appid:appid,pageid:pageid},
            dataType: 'json',
            beforeSend: function (xhr, settings) {
            var csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {xhr.setRequestHeader("X-CSRFToken", csrftoken);}},
            success: function(data) {
    }
});
});

$("#edit_case").click(function () {
      var id=$('#id2').val();
      var name = $('#casename2').val();
      var inparam = $('#inparam2').val();
      var header=$('#header2').val();
      var expect = $('#expect2').val();


      $.ajax({
        url: "/edit_api_case/",
        async: false,
        type: "POST",
        data: {id:id,casename:name,inparam:inparam,header:header,expect:expect},
        dataType: "json",
        beforeSend: function (xhr, settings) {
            var csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {xhr.setRequestHeader("X-CSRFToken", csrftoken);}},
        success: function (data) {
         // swal("修改完成！", "", "success");
        }
    });

    });

$(".cases_report").click(function(){
        var id = $(this).attr("id");
        alert(id);
           $.ajax({
            type: "POST",
            url: "/run_task/",
            async: false,
            dataType:"json",
            data:{id:id},
            beforeSend: function (xhr, settings) {
            var csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {xhr.setRequestHeader("X-CSRFToken", csrftoken);}},
            success: function(data) {
                swal("执行完成！", "", "success");
                t=$("#task_"+id);
                t.children('td').eq(2).html(data["ccount"]);
                t.children('td').eq(3).html(data["pcount"]);
                t.children('td').eq(4).html(data["fcount"]);
                t.children('td').eq(5).html(data["eltime"]+"s");
                t.children('td').eq(6).html(data["extime"]);
                t.children('td').eq(8).find('a').attr({class:"glyphicon glyphicon-edit",href:"/taskreport/"+id+".html",target:"_blank"});
                //t.children('td').eq(8).find('a').attr("",);
}


        });
        });


$("#add_caseModal").on("hidden.bs.modal", function() {
        $("#select").val("");
        $("#casename").val("");
        $("#apiurl").val("");
        $("#inparam").val("");
        $("#header").val("");
        $("#expect").val("");
        $("#add_caseForm").data('bootstrapValidator').destroy();
        $("#add_caseForm").data('bootstrapValidator',null);
        formValidator();
    });
$("#edit_caseModal").on("hidden.bs.modal", function() {
        $("#casename").val("");
        $("#apiurl").val("");
        $("#inparam").val("");
        $("#header").val("");
        $("#expect").val("");
        $("#edit_caseForm").data('bootstrapValidator').destroy();
        $("#edit_caseForm").data('bootstrapValidator',null);
        formValidator();
    });

$(document).ready(function () {





});



