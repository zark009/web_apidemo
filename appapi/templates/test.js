/**
 * Created by dyp on 16-5-3.
 */
$(function () {
    var form = $("#frm_add_tomcat");
    var constraints = {
        sel_site: {
            presence: true
        },
        sel_app: {
            presence: true
        },
        describe: {
            presence: true
        }
    };
    var tomcatPageJs = {
        domId: {
            tab_wrapper: $("#tab_wrapper"),
            sel_ip: $("#sel_ip"),
            sel_site: $("#sel_site"),
            sel_app: $("#sel_app"),
            sel_env: $("#sel_env"),
            add_model: $("#add_model"),
            btn_save: $("#btn_save"),
            btn_add: $("#btn_add")
        },

        init: function () {
            $(".sidebar-menu li").removeClass("active");
            $(".deploy_mag_li").addClass("active");
            $(".deploy_mag_li .deploy_mag_li_tomcat").addClass("active");
            $(".deploy_mag_ul").addClass("menu-open").show();
            tomcatPageJs.domId.sel_ip.select2(PageCommon.commonConf.select2Conf);

            tomcatPageJs.bindEvent();
            tomcatPageJs.tab.getTabData();
        },

        bindEvent: function () {
            tomcatPageJs.domId.btn_add.unbind().bind("click", function () {
                tomcatPageJs.clearForm("frm_add_tomcat");
                tomcatPageJs.domId.add_model.modal("show");
                $("#frm_add_tomcat").show();
                $("#frm_view_tomcat").hide();
                tomcatPageJs.domId.btn_save.show();
            });

            tomcatPageJs.domId.sel_site.unbind().bind("change", function () {
                PageCommon.subPageFun.loadApps(tomcatPageJs.domId.sel_app, tomcatPageJs.domId.sel_site.val());
                tomcatPageJs.domId.sel_ip.select2(PageCommon.commonConf.select2Conf);
                tomcatPageJs.loadIps();
            });

            tomcatPageJs.domId.sel_app.unbind().bind("change", function () {
                tomcatPageJs.loadIps();
            });

            tomcatPageJs.domId.sel_env.unbind().bind("change", function () {
                tomcatPageJs.loadIps();
            });

            tomcatPageJs.domId.btn_save.unbind().bind("click", function () {
                if (!tomcatPageJs.validParams()) {
                    tomcatPageJs.chgMultiSelectColor();
                    return;
                }
                var ips = tomcatPageJs.getSelectValues();
                if (ips === "") {
                    tomcatPageJs.chgMultiSelectColor();
                    return;
                }
                var describe = $("#describe").val();
                if (describe.length < 4) {
                    swal("原因字段必须大于4个字符", "", "warning");
                    return;
                }
                tomcatPageJs.domId.add_model.modal("hide");
                tomcatPageJs.opAjaxCol.add();
            });

            $(".detail_info").unbind().bind("click", function () {
                var txtId = $(this).attr("data-optId");
                tomcatPageJs.opAjaxCol.get_by_id(txtId);
                tomcatPageJs.domId.add_model.modal("show");
                $("#frm_add_tomcat").hide();
                $("#frm_view_tomcat").show();
                tomcatPageJs.domId.btn_save.hide();
            });
        },

        chgMultiSelectColor: function () {
            var ips = tomcatPageJs.getSelectValues();
            if (ips === "") {
                $("#sel_ip_warp").addClass("has-error");
                $(".select2-selection--multiple").css("border", "solid #dd4b39 1px");
            } else {
                $(".select2-selection--multiple").css("border", "solid #d2d6de 1px");
                $("#sel_ip_warp").removeClass("has-error");
            }
        },

        clearForm: function (frmId) {
            document.getElementById(frmId).reset();
            form.find(".form-group").removeClass("has-error");
            tomcatPageJs.domId.sel_ip.select2(PageCommon.commonConf.select2Conf);
        },

        dataToForm: function (dataDict) {
            $("#view_pool").val(dataDict["pool_name"]);
            $("#view_env").val(dataDict["env"]);
            $("#view_ip").val(dataDict["ips"]);
            $("#view_op_type").val(dataDict["op_type"]);
            $("#view_describe").val(dataDict["describe"]);
            $("#view_comment").val(dataDict["comment"]);
        },

        getParams: function (get_type) {
            if (get_type === 'add') {
                var ips = tomcatPageJs.getSelectValues();
                return form.serialize() + "&post_type=add" + "&ips=" + ips;
            }

        },

        validParams: function () {
            var errors = validate(form, constraints) || {};
            PageCommon.other.showErrorsForInput(errors, form);
            return !PageCommon.other.objIsEmpty(errors);

        },

        getSelectValues: function () {
            var objArr = tomcatPageJs.domId.sel_ip.select2("data");
            var retArr = [];
            for (var i = 0; i < objArr.length; ++i) {
                retArr.push(objArr[i].text);
            }
            return retArr.join();
        },

        loadIps: function () {
            var siteId = tomcatPageJs.domId.sel_site.val();
            var appId = tomcatPageJs.domId.sel_app.val();
            var env = tomcatPageJs.domId.sel_env.val();
            PageCommon.subPageFun.loadIpBySiteApp(tomcatPageJs.domId.sel_ip, siteId, appId, env);
        },

        tab: {
            tabTemplate: {
                get: function () {
                    return '<table id="table_id" class="display" style="width: 100%;">'
                        + '<thead>'
                        + '<tr role="row">'
                        + '    <th class="sorting_disabled" rowspan="1" colspan="1" style="width: 100px;">单号</th>'
                        + '    <th class="sorting_disabled" rowspan="1" colspan="1" style="width: 80px;">操作类型</th>'
                        + '    <th class="sorting_disabled" rowspan="1" colspan="1" style="width: 120px;">Pool名称</th>'
                        + '    <th class="sorting_disabled" rowspan="1" colspan="1" style="width: 60px;">环境</th>'
                        + '    <th class="sorting_disabled" rowspan="1" colspan="1" style="width: 80px;">操作人</th>'
                            //+ '    <th class="sorting_disabled" rowspan="1" colspan="1" style="width: 100px;">重启原因</th>'
                        + '    <th class="sorting_disabled" rowspan="1" colspan="1" style="width: 100px;">操作时间</th>'
                        + '    <th class="sorting_disabled" rowspan="1" colspan="1" style="width: 60px;">状态</th>'
                        + '    <th class="sorting_disabled" rowspan="1" colspan="1" style="width: 60px;">操作</th>'
                        + '</tr>'
                        + '</thead>'
                        + '</table>';
                }
            },

            getTabData: function () {
                layer.load(2, PageCommon.commonConf.loadConf);
                tomcatPageJs.domId.tab_wrapper.empty().append(tomcatPageJs.tab.tabTemplate.get());
                var table = $('#table_id').DataTable({
                    serverSide: true,
                    ajax: {
                        "url": Urls.op_tomcat(),
                        "type": "POST"
                    },
                    columns: [
                        {data: 'number'},
                        {
                            data: 'op_type', render: function (data, type, full, meta) {
                            var htmlTag = "";
                            if (data === "停止") {
                                htmlTag = PageCommon.text.getText("label-warning", data);
                            } else {
                                htmlTag = PageCommon.text.getText("label-info", data);
                            }
                            return htmlTag;
                        }
                        },
                        {data: 'pool_name'},
                        {data: 'env'},
                        {data: 'user_account'},
                        //{data: 'describe'},
                        {data: 'restart_time'},
                        {
                            data: 'status', render: function (data, type, full, meta) {
                            var htmlTag = "";
                            if (data === "成功") {
                                htmlTag = PageCommon.text.getText("label-success", data);
                            } else if (data === "失败" || data === "HC失败") {
                                htmlTag = PageCommon.text.getText("label-danger", data);
                            } else if (data === "操作中") {
                                htmlTag = PageCommon.text.getText("label-info", data);
                            }
                            return htmlTag;
                        }
                        },
                        {
                            data: 'opt', render: function (data, type, full, meta) {
                            var htmlTag = "";
                            htmlTag += PageCommon.btn.getIco("详情", "fa-file-text-o detail_info", full.id);
                            return htmlTag;
                        }
                        }
                    ],
                    language: PageCommon.dataTabConf.language,
                    ordering: false
                });
                table.on('draw', function () {
                    layer.closeAll('loading');
                    tomcatPageJs.bindEvent();
                });
                tomcatPageJs.bindEvent();
            }

        },

        opAjaxCol: {
            add: function () {
                layer.load(2, PageCommon.commonConf.loadConf);
                var params = tomcatPageJs.getParams("add");
                PageCommon.ajax.post(Urls.op_tomcat(), params, function (dataDict) {
                    layer.closeAll('loading');
                    if (dataDict["ret"] === 0) {
                        swal("保存成功", "", "success");
                        tomcatPageJs.tab.getTabData();
                    } else if (dataDict["ret"] === -1) {
                        swal("保存失败", "没有操作所选pool的权限", "error");
                    } else if (dataDict["ret"] === -2) {
                        swal("保存失败", "所选pool没有HeathCheck地址", "error");
                    } else if (dataDict["ret"] === -3) {
                        swal("保存失败", "所选pool有发布单未关闭", "error");
                    } else if (dataDict["ret"] === -4) {
                        swal("保存失败", "已存在该操作", "error");
                    } else {
                        swal("保存失败", "", "error");
                    }
                });
            },

            get_by_id: function (txtId) {
                layer.load(2, PageCommon.commonConf.loadConf);
                var params = {
                    "post_type": "get_by_id",
                    "tomcat_id": txtId
                };
                PageCommon.ajax.post(Urls.op_tomcat(), params, function (dataDict) {
                    layer.closeAll('loading');
                    if (dataDict["ret"] === 0) {
                        tomcatPageJs.dataToForm(dataDict["data"]);
                        $("#deploy_log").val(dataDict["logs"]);
                    }
                });
            }

        }

    };

    tomcatPageJs.init();
});