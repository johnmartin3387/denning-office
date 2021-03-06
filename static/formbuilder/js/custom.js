var FormBuilder_tp = function() {

    // initialize the global values
    let mode = 0
    let edit_form_mode = 0
    var formBuilder = null
    var jsonData = null

    var jsonDataForDB = []
    var form_type = ""

    var handleDemo = function() {
        $(".edit-tool").attr("style", "display:none;")
    }

    var saveFrame = function(type){
        if(mode == 0){
            mode = 1
            $(".edit-btn").html("Save Form")
            $(".edit-tool").attr("style", "")
        }
        else{
            mode = 0
            $(".edit-btn").html("Edit Form")
            $(".edit-tool").attr("style", "display:none;")

            if(form_type != ""){
                console.log(jsonDataForDB)
                commitData(jsonDataForDB)
            }
        }
        form_type = type
    }
    
    var appendForm = function(obj, clss){
        str = '<div class="portlet box purple custom-form-item"> \
                <div class="portlet-title"> \
                    <div class="caption"> \
                         <span class="header-static" style=""></span> <input type="text" class="form-control input-sm header-edit" style="display: none"> </div> \
                    <div class="tools"> \
                        <a href="" class="collapse"> </a> \
                        <a href="" class="fullscreen edit-tool" data-original-title="" title="" onclick="FormBuilder_tp.editForm(this)"> </a> \
                        <a href="javascript:;" class="edit-form edit-tool" onclick="FormBuilder_tp.appendForm(this, \'col-md-6\')"> </a> \
                        <a href="javascript:;" class="remove-form edit-tool" data-original-title="" title="" onclick="FormBuilder_tp.removeForm(this)"> </a> \
                    </div> \
                </div> \
                <div class="portlet-body form form-horizontal"> \
                        <div class="form-body"> \
                        </div> \
                </div> \
            </div>'
        $(str).insertAfter($(obj).parent().parent().parent())
    }

    var getIDByObj = function(obj){
        return $(obj).parent().parent().next().children().eq(0).attr("for")
    }

    var editForm = function(obj, type){
        var header_static = $(obj).parent().prev().children().eq(0)
        var header_edit = $(obj).parent().prev().children().eq(1)

        if(edit_form_mode == 0){
            var id = getIDByObj(obj)
            if(id == undefined){
                randNum = genRand().toString()
                str = '<div class="row" id="myformbuilder-'+ randNum +'"> \
                    </div>'
                id = "myformbuilder-"+ randNum
            } else {
                str = '<div class="row" id="'+ id +'"> \
                    </div>'
            }
            $(obj).parent().parent().next().children().eq(0).html(str)
            $(obj).parent().parent().next().children().eq(0).attr("for", id)

            formBuilder = getFormBuilder(id);
            edit_form_mode = 1

            header_static.attr("style", "display:none;")
            header_edit.attr("style", "display:block;")
            header_edit.val(header_static.html())
        }else{
            $(obj).parent().parent().next().children().eq(0).html("")
            edit_form_mode = 0

            if(formBuilder != null){
                jsonData = formBuilder.actions.getData('json', true)
                
                jsonData = convertBJsonToRJson(jsonData)
                html = convertJsonToHtml(jsonData)

                updateData(getIDByObj(obj), header_edit.val(), jsonData)

                $(obj).parent().parent().next().children().eq(0).html(html)

                $(".form_datetime").datetimepicker({
                    autoclose: true,
                    isRTL: App.isRTL(),
                    format: "dd MM yyyy - hh:ii",
                    pickerPosition: (App.isRTL() ? "bottom-right" : "bottom-left")
                });

                $('body').removeClass("modal-open"); // fix bug when inline picker is used in modal
                // Workaround to fix datetimepicker position on window scroll
                $( document ).scroll(function(){
                    $('.form_datetime').datetimepicker('place'); //#modal is the id of the modal
                });

                $('.defaultrange_modal').daterangepicker({
                        opens: (App.isRTL() ? 'left' : 'right'),
                        format: 'Y-m-d',
                        separator: ' to ',
                        startDate: moment().subtract('days', 29),
                        endDate: moment(),
                    },
                    function (start, end) {
                        $('.defaultrange_modal input').val(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
                    }
                ); 

                header_static.attr("style", "display:block;")
                header_edit.attr("style", "display:none;")
                header_static.html(header_edit.val())
            }
        }
    }

    var removeForm = function(obj){
        if(getIDByObj(obj) != undefined){
            removeData(getIDByObj(obj))
        }

        $(obj).parent().parent().parent().remove()
    }

    var getCustomForm = function(json, values){
        var res = ""
        jsonDataForDB = json
        try { 
            values = values.replace(/&quot;/g, "\"")
            values = JSON.parse(values)
        }
        catch(err){
            values = {}
        }

        for(var i=0; i<json.length; i++){
            var str = '<div class="portlet box purple custom-form-item"> \
                        <div class="portlet-title"> \
                            <div class="caption"> \
                                 <span class="header-static" style="">'+ json[i][2] +'</span> <input type="text" class="form-control input-sm header-edit" style="display: none"> </div> \
                            <div class="tools"> \
                                <a href="" class="collapse"> </a> \
                                <a href="" class="fullscreen edit-tool" data-original-title="" title="" onclick="FormBuilder_tp.editForm(this)"> </a> \
                                <a href="javascript:;" class="edit-form edit-tool" onclick="FormBuilder_tp.appendForm(this, \'col-md-6\')"> </a> \
                                <a href="javascript:;" class="remove-form edit-tool" data-original-title="" title="" onclick="FormBuilder_tp.removeForm(this)"> </a> \
                            </div> \
                        </div> \
                        <div class="portlet-body form form-horizontal"> \
                                <div class="form-body" for="'+json[i][0]+'"> ' +
                                convertJsonToHtml(json[i][1], values)
                                + ' \
                                </div> \
                        </div> \
                    </div>'
            res += str
        }
        return res
    }

    var setMode = function(param){
        mode = param
        if(mode == 0){
            mode = 1
            $(".edit-btn").html("Save Form")
            $(".edit-tool").attr("style", "")
        }
        else{
            mode = 0
            $(".edit-btn").html("Edit Form")
            $(".edit-tool").attr("style", "display:none;")
        }
    }

    var getFormBuilder = function(indicator){
        var options = {
          disabledAttrs: ["value", "className", "access", "help", 
                    "inline", "other", "style", "toggle", "required"],
          disabledActionButtons: ['data', 'clear', 'save'],
          disableFields: ['button'],
          typeUserAttrs: {
            autocomplete: {
              className: {
                label: 'Type',
                options: {
                  'single': 'single',
                  'multiple': 'multiple'
                }
              }
            },
            date: {
              className: {
                label: 'Type',
                options: {
                  'single': 'Single',
                  'range': 'Range'
                }
              }
            },
            
          }
        };

        var data = getData(indicator);
        if(data != undefined){
            options["defaultFields"] = data
        }

        return $("#" + indicator).formBuilder(options);
    }

    var genRand = function() {
      return Math.floor(Math.random()*89999+10000);
    }

    var slugify = function(string) {
      return string
        .toString()
        .trim()
        .toLowerCase()
        .replace(/\s+/g, "-")
        .replace(/[^\w\-]+/g, "")
        .replace(/\-\-+/g, "-")
        .replace(/^-+/, "")
        .replace(/-+$/, "");
    }

    // convert FormBuilder Json into the json data for metronics form
    var convertBJsonToRJson = function(jsonData){
        jsonData = JSON.parse(jsonData)
        for(var idx=0; idx<jsonData.length; idx++){
            if(jsonData[idx]["name"] == undefined){
                jsonData[idx]["name"] = "name-" + genRand().toString()
            }
        }
        return jsonData
    }

    var getInputStr = function(element, placeholder, value){
        var type = element["subtype"]
        if(type == undefined)
            type = element["type"]
        if(value == undefined)
            value = ""

        var html = '<div class="form-group form-md-line-input has-success"> \
            <label class="col-md-4 control-label">'+ element["label"] +'</label> \
            <div class="col-md-8"> \
                <input type="' + type + '" class="form-control" placeholder="'+ placeholder +'" name="'+ element['name'] +'" value="'+ value +'"> \
                <div class="form-control-focus"> </div> \
            </div> \
        </div>'

        return html
    }

    var getButtonStr = function(element, placeholder){
        var html = '<a href="javascript:;" class="btn default"> Link </a>'
    }

    var getDateStr = function(element, placeholder, value){
        if(value == undefined)
            value = ""
        var html = '<div class="form-group form-md-line-input has-success"> \
                        <label class="col-md-4 control-label">'+ element["label"] +'</label> \
                        <div class="col-md-8">\
                            <input type="text" placeholder="'+ placeholder +'" name="'+ element['name'] +'" class="form-control date-set date-picker" value="'+ value +'"> \
                        </div> \
                    </div>'

        return html
    }

    var getDateRangeStr = function(element, placeholder, value){
        if(value == undefined)
            value = ""
        var html = '<div class="form-group form-md-line-input has-success"> \
                        <label class="col-md-4 control-label">'+ element["label"] +'</label> \
                        <div class="col-md-8"> \
                            <div class="input-group input-large defaultrange_modal"> \
                                <input type="text" class="form-control" name="'+ element['name'] +'" value="'+ value +'"> \
                                <span class="input-group-btn"> \
                                    <button class="btn default date-range-toggle" type="button"> \
                                        <i class="fa fa-calendar"></i> \
                                    </button> \
                                </span> \
                            </div> \
                        </div> \
                    </div>'

        return html
    }

    var getTextareaStr = function(element, placeholder, value){
        if(value == undefined)
            value = ""

        var html = '<div class="form-group form-md-line-input has-success"> \
                        <label class="col-md-4 control-label">'+ element["label"] +'</label> \
                        <div class="col-md-8"> \
                            <textarea class="form-control" rows="3" placeholder="'+ placeholder +'" name="'+ element['name'] +'">'+ value +'</textarea> \
                        </div> \
                    </div>'

        return html
    }

    var getCheckboxStr = function(element, placeholder, value){
        if(value == "on")
            value = "checked"
        else
            value = ""
        var html = '<div class="form-group form-md-line-input has-success"> \
                        <label class="col-md-4 control-label">'+ element["label"] +'</label> \
                        <div class="col-md-8"> \
                            <div class="md-checkbox-inline"> \
                                <div class="md-checkbox col-md-8" style="margin-left:15%;"> \
                                    <input type="checkbox" id="checkbox" placeholder="'+ placeholder +'" name="'+ element['name'] +'" class="md-check" '+ value +'> \
                                    <label for="checkbox"> \
                                        <span></span> \
                                        <span class="check"></span> \
                                        <span class="box"></span>  </label> \
                                </div> \
                            </div> \
                        </div> \
                    </div>'

        return html
    }

    var getAutoCompleteStr = function(element, placeholder, value){
        var result = $.ajax({
            type: "GET",
            url: '/api/contact/?format=json',
            dataType: 'json',
            contentType: 'application/json; charset=UTF-8',
            async: false
        }).responseText;
        result = JSON.parse(result)
        contacts = ""
        if(value == undefined)
            value = []
        else if(element["className"] == "multiple")
            value = value.split(",")
        else
            value = [value]


        for(var i=0; i<result["objects"].length; i++){
            var selected = "", href = "javascript:;"
            if(result["objects"][i]["id"] == value[0]){
                selected = "selected"
                href = "/contact/update?id=" + value[0]
            }
            contacts += '<option value="'+result["objects"][i]["id"]+'" '+selected+'>'+result["objects"][i]["name"]+' &nbsp;&nbsp;&nbsp;&nbsp; ('+result["objects"][i]["id_value"]+')</option>'
        }
        var html = '<div class="form-group form-md-line-input has-success"> \
                        <label class="col-md-4 control-label" for="director">'+ element["label"] +'</label> \
                        <div class="col-md-8 input-group-control"> \
                            <div class="input-group input-group-sm"> \
                                <div class="input-group-control"> \
                                    <select class="form-control select2" name="'+ element['name'] +'" onchange="choose_contact(this)"> \
                                        <option value=""></option> '+ contacts +' \
                                    </select> \
                                    <div class="form-control-focus"> </div> \
                                </div> \
                                <span class="input-group-btn btn-right"> \
                                    <a href="/contact/update" class="btn btn-xs blue" style="margin-left: 2px;" target="_blank"> \
                                        <i class="fa fa-plus"></i> </a> \
                                    <a href="'+href+'" class="btn btn-icon-only purple" target="_blank" style="margin-left: 2px;"> \
                                        <i class="fa fa-search"></i> \
                                    </a> \
                                </span> \
                            </div> \
                        </div> \
                    </div>'

        for(var idx=1; idx<value.length; idx++){
            contacts = ""
            for(var i=0; i<result["objects"].length; i++){
                var selected = "", href = "javascript:;"
                if(result["objects"][i]["id"] == value[idx]){
                    selected = "selected"
                    href = "/contact/update?id=" + value[idx]
                }
                contacts += '<option value="'+result["objects"][i]["id"]+'" '+selected+'>'+result["objects"][i]["name"]+' &nbsp;&nbsp;&nbsp;&nbsp; ('+result["objects"][i]["id_value"]+')</option>'
            }
            html += '<div class="form-group form-md-line-input has-success"> \
                            <label class="col-md-4 control-label" for="director">'+ element["label"] +'</label> \
                            <div class="col-md-8 input-group-control"> \
                                <div class="input-group input-group-sm"> \
                                    <div class="input-group-control"> \
                                        <select class="form-control select2" name="'+ element['name'] +'" onchange="choose_contact(this)"> \
                                            <option value=""></option> '+ contacts +' \
                                        </select> \
                                        <div class="form-control-focus"> </div> \
                                    </div> \
                                    <span class="input-group-btn btn-right"> \
                                        <a href="/contact/update" class="btn btn-xs blue" style="margin-left: 2px;" target="_blank"> \
                                            <i class="fa fa-plus"></i> </a> \
                                        <a href="'+href+'" class="btn btn-icon-only purple" target="_blank" style="margin-left: 2px;"> \
                                            <i class="fa fa-search"></i> \
                                        </a> \
                                    </span> \
                                </div> \
                            </div> \
                        </div>'
        }

        if(element["className"] == "multiple"){
            html += '<div class="form-group form-md-line-input has-success"> \
                        <label class="col-md-8 control-label" for="marital_status"></label> \
                        <div class="col-md-4"> \
                            <a href="javascript:;" class="btn btn-xs default"><i class="fa fa-plus" onclick="addContact(this, \''+ element["label"] +'\', \''+ element["name"] +'\')"></i> </a> \
                            <a href="javascript:;" class="btn btn-xs default"><i class="fa fa-minus" onclick="removeContact(this)"></i> </a> \
                        </div> \
                    </div>'
        }
        return html
    }

    var getSelectStr = function(element, placeholder, value){
        var options = ""
        if(value == undefined)
            value = ""

        if(element["values"] != undefined){
            for(var index=0; index<element["values"].length; index++){
                if(element["values"][index]["value"] == value)
                    options += '<option value="'+ element["values"][index]["value"] 
                        +'" selected>'+ element["values"][index]["label"] +'</option>'
                else
                    options += '<option value="'+ element["values"][index]["value"] 
                        +'">'+ element["values"][index]["label"] +'</option>'
            }
        }

        var html = '<div class="form-group form-md-line-input has-success"> \
                        <label class="col-md-4 control-label">'+ element["label"] +'</label> \
                        <div class="col-md-8"> \
                            <select class="form-control" name="'+ element['name'] +'"> \
                                '+ options +' \
                            </select> \
                        </div> \
                    </div>'
                    
        return html
    }

    // convert json data into html string
    var convertJsonToHtml = function(jsonData, values){
        var html = ""
        if(values == undefined)
            values = {}
        for(var idx=0; idx<jsonData.length; idx++){
            
            element = jsonData[idx]
            var placeholder = element["placeholder"]
            if(placeholder == undefined)
                placeholder = ""

            // for input element
            if(element["type"] == "text" || element["type"] == "number"){
                html += getInputStr(element, placeholder, values[element['name']])
            } else if(element["type"] == "date" && element["className"] == "single"){
                html += getDateStr(element, placeholder, values[element['name']])
            } else if(element["type"] == "date" && element["className"] == "range"){
                html += getDateRangeStr(element, placeholder, values[element['name']])
            } else if(element["type"] == "textarea"){
                html += getTextareaStr(element, placeholder, values[element['name']])
            } else if(element["type"] == "checkbox-group"){
                html += getCheckboxStr(element, placeholder, values[element['name']])
            } else if(element["type"] == "autocomplete"){
                html += getAutoCompleteStr(element, placeholder, values[element['name']])
            } else if(element["type"] == "select"){
                html += getSelectStr(element, placeholder, values[element['name']])
            }
                
        }
        return html
    }

    var updateData = function(key, header, data){
        var flag = 0, i = 0;

        if(data.length == 0)
            return

        for(i=0; i<jsonDataForDB.length; i++){
            if(jsonDataForDB[i][0] == key){
                flag = 1
                break
            }
        }

        if(flag == 1){
            jsonDataForDB.splice(i, 1, [key, data, header]);
        } else {
            console.log(jsonDataForDB)
            jsonDataForDB.push([key, data, header]);
        }
    }

    var commitData = function(json){
        // commit json data into server
        if(form_type == "contact"){
            if($("#type").val() == "new"){
                var name = $("#new_type").val()
                if(name == "")
                    return

                $.ajax({
                    type: 'post',
                    url: '/api/contact_template/',
                    data: JSON.stringify({"type": name, "json": JSON.stringify(json)}),
                    contentType: 'application/json; charset=UTF-8',
                    dataType: 'json',
                    success: function(data) {
                      
                    }
                });
            } else {
                $.ajax({
                    type: 'put',
                    url: '/api/contact_template/'+$("#type").val()+'/?format=json',
                    contentType: 'application/json; charset=UTF-8',
                    data: JSON.stringify({"json": JSON.stringify(json)}),
                    dataType: 'json',
                    success: function(data) {
                        
                    }
                });
            }
        } else if(form_type == "matter"){
            $("#additional_info").val(JSON.stringify(json))
        } else if(form_type == "property"){
            $.ajax({
                type: 'get',
                url: '/api/update_property_template/?json=' + JSON.stringify(json),
                success: function(data) {
                    
                }
            });
        }
    }

    var removeData = function(key){
        for(var i=0; i<jsonDataForDB.length; i++){
            if(jsonDataForDB[i][0] == key){
                jsonDataForDB.splice(i, 1);
                break
            }
        }
    }

    var getData = function(key){
        for(var i=0; i<jsonDataForDB.length; i++){
            if(jsonDataForDB[i][0] == key){
                return jsonDataForDB[i][1]
            }
        }
    }

    return {
        //main function to initiate the module
        init: function() {
            handleDemo();
        },
        appendForm: function(obj, clss) {
            appendForm(obj, clss);
        },
        editForm: function(obj, type) {
            editForm(obj, type);
        },
        removeForm: function(obj) {
            removeForm(obj);
        },
        saveFrame: function(type) {
            saveFrame(type);
        },
        commitData: function(json) {
            commitData(json);
        },
        getCustomForm: function(json, values){
            return getCustomForm(json, values)
        },
        setMode: function(param){
            setMode(param)
        },
        slugify_p: function(param){
            return slugify(param)
        }
    };

}();

var addNew = function(type){
    $(".modal-title").html("Add New " + type)
    $("#list-type").val(type)
    $("#list-value").val("")
}
var commitNewAttr = function(){
    var type = $("#list-type").val()
    var value = $("#list-value").val()
    if(value == "")
        return

    $.ajax({
        type: 'post',
        url: '/api/attribute/?format=json',
        data: JSON.stringify({"type": type, "value": value}),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        success: function(data) {
        },
        error: function() {
            $.ajax({
                type: 'get',
                url: '/api/attribute/?format=json&type=' + type,
                data: JSON.stringify({"type": type, "value": value}),
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                success: function(data) {
                    var indicator = FormBuilder_tp.slugify_p($("#list-type").val())

                    var str = ""
                    for(var i=0; i<data["objects"].length-1; i++){
                        str += '<option value="'+data["objects"][i]['id']+'">'+data["objects"][i]['value']+'</option>'
                    }
                    if(data["objects"].length != 0)
                        str += '<option value="'+data["objects"][data["objects"].length-1]['id']+'" selected>'+data["objects"][data["objects"].length-1]['value']+'</option>'
                    
                    $("#"+indicator).html(str)

                    $(".select2, .select2-multiple").select2({
                        placeholder: "",
                        width: null
                    });
                    checkValidation("#defaultForm")
                }
            });
        }
    });
}

var checkValidation = function(indicator, rule){
    if(rule == undefined){
        rule = {
                password: {
                    minlength: 5,
                    required: true
                },
                confirm: {
                    minlength: 5,
                    required: true,
                    equalTo: "#password"
                }
            }
    }
    $(indicator).validate({
        rules: rule,
        highlight: function (element) { // hightlight error inputs

            $(element)
                .closest('.form-group').addClass('has-error'); // set error class to the control group
        },

        unhighlight: function (element) { // revert the change done by hightlight
            $(element)
                .closest('.form-group').removeClass('has-error'); // set error class to the control group
        },

        success: function (label) {
            label
                .closest('.form-group').removeClass('has-error'); // set success class to the control group
        },
        submitHandler: function (form) {
            var temp = $("#customForm").serializeArray()
            var custom = {}

            for(var i=0; i<temp.length; i++){
                if(custom[temp[i]["name"]] == undefined)
                    custom[temp[i]["name"]] = temp[i]["value"]
                else
                    custom[temp[i]["name"]] += "," + temp[i]["value"]
            }
            custom = JSON.stringify(custom)

            $(".custom_data").val(custom)

            if($("#phone_home").val() != undefined){
                valid = 1
                if($("#phone_home").val() != "" && $("#phone_home").intlTelInput("isValidNumber") == false){
                    $("#phone_home").parent().parent().parent().addClass("has-error");
                    $("#phone_home_val").val("")
                    valid = 0
                } else {
                    $("#phone_home").parent().parent().parent().removeClass("has-error");
                    $("#phone_home_val").val($("#phone_home").intlTelInput("getNumber"))
                }
                if($("#phone_office").val() != "" && $("#phone_office").intlTelInput("isValidNumber") == false){
                    $("#phone_office").parent().parent().parent().addClass("has-error");
                    $("#phone_office_val").val("")
                    valid = 0
                } else {
                    $("#phone_office").parent().parent().parent().removeClass("has-error");
                    $("#phone_office_val").val($("#phone_office").intlTelInput("getNumber"))
                }
                if($("#phone_mobile").val() != "" && $("#phone_mobile").intlTelInput("isValidNumber") == false){
                    $("#phone_mobile").parent().parent().parent().addClass("has-error");
                    $("#phone_mobile_val").val("")
                    valid = 0
                } else {
                    $("#phone_mobile").parent().parent().parent().removeClass("has-error");
                    $("#phone_mobile_val").val($("#phone_mobile").intlTelInput("getNumber"))
                }

                if(valid == 0)
                    return
            }

            if($("#phone_personal").val() != undefined){
                valid = 1
                if($("#phone_personal").val() != "" && $("#phone_personal").intlTelInput("isValidNumber") == false){
                    $("#phone_personal").parent().parent().parent().addClass("has-error");
                    $("#phone_personal_val").val("")
                    valid = 0
                } else {
                    $("#phone_personal").parent().parent().parent().removeClass("has-error");
                    $("#phone_personal_val").val($("#phone_personal").intlTelInput("getNumber"))
                }
                
                if(valid == 0)
                    return
            }

            if($("#fax").val() != undefined){
                valid = 1
                if($("#fax").val() != "" && $("#fax").intlTelInput("isValidNumber") == false){
                    $("#fax").parent().parent().parent().addClass("has-error");
                    $("#fax_val").val("")
                    valid = 0
                } else {
                    $("#fax").parent().parent().parent().removeClass("has-error");
                    $("#fax_val").val($("#fax").intlTelInput("getNumber"))
                }
                if($("#fax2").val() != undefined && $("#fax2").val() != "" && $("#fax2").intlTelInput("isValidNumber") == false){
                    $("#fax2").parent().parent().parent().addClass("has-error");
                    $("#fax2_val").val("")
                    valid = 0
                } else {
                    $("#fax2").parent().parent().parent().removeClass("has-error");
                    $("#fax2_val").val($("#fax2").intlTelInput("getNumber"))
                }
                if(valid == 0)
                    return
            }

            

            form[0].submit(); // submit the form
        }
    })
}

var datatables = function(indicator){
    // begin first table
        $(indicator).dataTable({

            // Internationalisation. For more info refer to http://datatables.net/manual/i18n
            "language": {
                "aria": {
                    "sortAscending": ": activate to sort column ascending",
                    "sortDescending": ": activate to sort column descending"
                },
                "emptyTable": "No data available in table",
                "info": "Showing _START_ to _END_ of _TOTAL_ records",
                "infoEmpty": "No records found",
                "infoFiltered": "(filtered1 from _MAX_ total records)",
                "lengthMenu": "Show _MENU_",
                "search": "Search:",
                "zeroRecords": "No matching records found",
                "paginate": {
                    "previous":"Prev",
                    "next": "Next",
                    "last": "Last",
                    "first": "First"
                }
            },

            // Or you can use remote translation file
            //"language": {
            //   url: '//cdn.datatables.net/plug-ins/3cfcc339e89/i18n/Portuguese.json'
            //},

            // Uncomment below line("dom" parameter) to fix the dropdown overflow issue in the datatable cells. The default datatable layout
            // setup uses scrollable div(table-scrollable) with overflow:auto to enable vertical scroll(see: assets/global/plugins/datatables/plugins/bootstrap/dataTables.bootstrap.js). 
            // So when dropdowns used the scrollable div should be removed. 
            //"dom": "<'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r>t<'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>",

            "bStateSave": true, // save datatable state(pagination, sort, etc) in cookie.

            "lengthMenu": [
                [5, 15, 20, -1],
                [5, 15, 20, "All"] // change per page values here
            ],
            // set the initial value
            "pageLength": 5,            
            "pagingType": "bootstrap_full_number",
            "columnDefs": [
                {
                    "className": "dt-right", 
                    //"targets": [2]
                }
            ],
            "order": [
                [0, "asc"]
            ] // set first column as a default sort by asc
        });
}

var initDateControl = function(){
    /*$(".form_datetime").datetimepicker({
        autoclose: true,
        isRTL: App.isRTL(),
        format: "yyyy-mm-dd hh:ii",
        pickerPosition: (App.isRTL() ? "bottom-right" : "bottom-left")
    });*/

    if (jQuery().datepicker) {
        $('.date-picker').datepicker({
            // rtl: App.isRTL(),
            changeMonth: true,
            changeYear: true,
            autoclose: true,
            dateFormat: "yy-mm-dd"
        });
        //$('body').removeClass("modal-open"); // fix bug when inline picker is used in modal
    }

    // $('body').removeClass("modal-open"); // fix bug when inline picker is used in modal
    // Workaround to fix datetimepicker position on window scroll
    $( document ).scroll(function(){
        $('.form_datetime').datetimepicker('place'); //#modal is the id of the modal
    });
}

var initPhoneControl = function(){
    $(".phone").intlTelInput(
        {
            geoIpLookup: function(callback) {
            $.get("http://ipinfo.io", function() {}, "jsonp").always(function(resp) {
                var countryCode = (resp && resp.country) ? resp.country : "";
                callback(countryCode);
            });
        },
        initialCountry: "auto"})
}

var getFormatString = function(){
    $('.address').each(function(index, item) {
        
    });
}

var choose_contact = function(obj, type="contact"){
    var id = $(obj).val()
    $(obj).parent().next().children().eq(1).attr('href', "/"+type+"/update?id="+id)
}

if (App.isAngularJsApp() === false) {
    jQuery(document).ready(function() {
        FormBuilder_tp.init();
    });
}

var capital = function(obj){
    var s = $(obj).val().split(' ');
    for(var i=0; i<s.length; i++) {
        s[i] = s[i].substring(0,1).toUpperCase() + s[i].substring(1);
    }
    s = s.join(' ');

    $(obj).val(s);
}